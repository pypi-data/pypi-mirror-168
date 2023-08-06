import logging
import json
import os
import requests
import sys
import yaml
import git
import xxhash
from dataclasses import dataclass
from typing import Optional, Dict
from metricflow.cli.main import _print_issues
from metricflow.model.parsing.config_linter import ConfigLinter
from metricflow.model.parsing.dir_to_model import collect_yaml_config_file_paths
from metricflow.model.validations.validator_helpers import ModelValidationResults

EXPECTED_TF_CONFIG_FILE_NAMES = [
    "tdfconfig.yml",
    "tdfconfig.yaml",
    "validate_configs.yaml",
    "commit_configs.yaml",
    "bitbucket-pipelines.yml",
    ".gitlab-ci.yml",  # this should be ignored by collect_yaml_config_file_paths() but it's not
]
TRANSFORM_API_URL = "https://api.transformdata.io"
UPLOAD_MODE_VALIDATE = "validate"
UPLOAD_MODE_COMMIT = "commit"
LOCAL_DIR_DEFAULT = "."
# TODO: Return error response so this constant doesn't have to be passed to the CLI
ERROR_RESPONSE_PREFIX = "Error response: "


@dataclass
class RequiredModelDetails:
    """Class Object for Required model details, pulled from the source control provider"""

    # Set as "Optional" to work with linter, as it is not guaranteed that ther environment variables exist
    REPO: Optional[str]
    BRANCH: Optional[str]
    COMMIT: Optional[str]


logger = logging.getLogger(__name__)


def parse_github() -> RequiredModelDetails:
    """Pull environment variables from Github"""
    REPO: Optional[str]
    if os.getenv("REPO"):
        REPO = os.getenv("REPO")
    else:
        REPO = os.getenv("GITHUB_REPOSITORY")

    # Remove Github org from repo
    if REPO:
        REPO = "/".join(REPO.split("/")[1:])

    BRANCH: Optional[str]
    if os.getenv("GITHUB_HEAD_REF") == "":
        github_ref = os.getenv("GITHUB_REF")
        if github_ref:
            BRANCH = github_ref.lstrip("/refs/heads/")
    else:
        BRANCH = os.getenv("GITHUB_HEAD_REF")

    COMMIT = os.getenv("GITHUB_SHA")

    return RequiredModelDetails(REPO=REPO, BRANCH=BRANCH, COMMIT=COMMIT)


def parse_gitlab() -> RequiredModelDetails:
    """Pull environment variables from Gitlab"""
    REPO: Optional[str]
    if os.getenv("REPO"):
        REPO = os.getenv("REPO")
    else:
        REPO = os.getenv("CI_PROJECT_PATH")

    # Remove Gitlab org from repo
    if REPO:
        REPO = "/".join(REPO.split("/")[1:])

    BRANCH = os.getenv("CI_COMMIT_REF_NAME")

    COMMIT = os.getenv("CI_COMMIT_SHA")

    return RequiredModelDetails(REPO=REPO, BRANCH=BRANCH, COMMIT=COMMIT)


def parse_bitbucket() -> RequiredModelDetails:
    """Pull environment variables from Bitbucket"""
    REPO: Optional[str]
    if os.getenv("REPO"):
        REPO = os.getenv("REPO")
    else:
        REPO = os.getenv("BITBUCKET_REPO_FULL_NAME")

    # Remove Gitlab org from repo
    if REPO:
        REPO = "/".join(REPO.split("/")[1:])

    BRANCH = os.getenv("BITBUCKET_BRANCH")

    COMMIT = os.getenv("BITBUCKET_COMMIT")

    return RequiredModelDetails(REPO=REPO, BRANCH=BRANCH, COMMIT=COMMIT)


def _err_msg_from_err_response(r: requests.Response) -> str:
    # Typically I'm against exceptions for control flow, but meh it's readable
    # in this case
    try:
        error_dict = json.loads(r.text)["error"]
        err_msg = f"{error_dict['error_type']}: {error_dict['message']}"
    except:  # noqa: E722
        err_msg = r.text

    return err_msg


def read_config_files(config_dir: str) -> Dict:  # noqa: D
    """Read yaml files from config_dir. Returns (file path, file contents) per file in dir"""
    assert os.path.exists(config_dir), f"User-specified config dir ({config_dir}) does not exist"

    relative_file_paths = collect_yaml_config_file_paths(directory=config_dir)
    try:
        git_repo = git.Repo(config_dir, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        git_repo = None

    results = {}
    for relative_file_path in relative_file_paths:
        # skip EXPECTED_TF_CONFIG_FILE_NAMES
        if os.path.split(relative_file_path)[1] in EXPECTED_TF_CONFIG_FILE_NAMES:
            continue

        with open(relative_file_path, "r") as f:
            filepath = os.path.abspath(relative_file_path)
            if git_repo is not None:
                filepath = filepath.split(git_repo.working_tree_dir)[-1]
            results[filepath] = f.read()
            try:
                yaml.safe_load_all(results[filepath])
            except yaml.parser.ParserError as e:
                raise yaml.parser.ParserError(f"Invalid yaml in config file at path: {filepath}. {e}")
            except Exception as e:
                raise Exception(f"Failed loading yaml config file. {e}")

    return results


def hash_file(path: str, content: str) -> str:  # noqa: D
    file_hash = xxhash.xxh3_128()
    file_hash.update(path.encode())
    file_hash.update(content.encode())
    return file_hash.hexdigest()


def hash_config_files(yaml_files: Dict[str, str]) -> Dict[str, str]:  # noqa: D
    hash_to_filename = {}
    for filename, contents in yaml_files.items():
        hashed_file = hash_file(filename, contents)
        hash_to_filename[hashed_file] = filename
    return hash_to_filename


def commit_configs(
    auth_header: Dict[str, str],
    repo: str,
    branch: str,
    commit: str,
    config_dir: str = LOCAL_DIR_DEFAULT,  # default to local dir
    is_validation: bool = False,
    api_url: str = TRANSFORM_API_URL,  # default to prod api
    return_issues: bool = False,
) -> requests.Response:
    """Creates either a validated or validation model based on `is_validation`

    Parses configs, runs semantic validations, and creates a validation or validated
    model based on `is_validation`
    """
    # Sometimes people accidentally override their local TRANSFORM_API_URL
    # environment variable with an empty string instead of UNSET-ing it.
    # And then an empty string propagates all the way here. So if api_url
    # is empty, default it. It's worth noting that in python "" evaluates to
    # false, which is why this oneliner works.
    api_url = api_url or TRANSFORM_API_URL

    # get the config files
    yaml_files = read_config_files(config_dir)
    hash_to_filename = hash_config_files(yaml_files)
    yaml_hashes = list(hash_to_filename.keys())

    compare_hashes_body = {"hashes": yaml_hashes}

    headers = {**{"Content-Type": "application/json"}, **auth_header}
    verify = api_url.startswith("https")

    compare_hashes_url = f"{api_url}/api/v1/model/{repo}/{branch}/{commit}/compare_yaml_hashes"
    logger.info("Uploading config file hashes")
    r = requests.post(
        compare_hashes_url, data=json.dumps(compare_hashes_body).encode("utf-8"), headers=headers, verify=verify
    )
    if r.status_code != 200:
        err_msg = _err_msg_from_err_response(r)
        raise Exception(err_msg)

    results = r.json()

    unmatched_hashes = yaml_hashes
    if results["unmatched"] is not None:
        unmatched_hashes = results["unmatched"]

    matched_hashes = results["matched"]

    upload_files = {}
    for yaml_hash in unmatched_hashes:
        yaml_file = hash_to_filename[yaml_hash]
        upload_files[yaml_file] = yaml_files[yaml_file]

    logger.info(f"Files to upload: {upload_files.keys()}")

    add_model_files_body = {
        "yaml_files": upload_files,
        "yaml_hashes": matched_hashes,
    }

    # Add the config files to backend file storage
    add_files_url = f"{api_url}/api/v1/model/{repo}/{branch}/{commit}/add_model_files"
    logger.info(f"add_files_url: {add_files_url}")
    logger.info("Uploading config files")
    r = requests.post(
        add_files_url, data=json.dumps(add_model_files_body).encode("utf-8"), headers=headers, verify=verify
    )
    if r.status_code != 200:
        raise Exception(f"Failed uploading config yaml files. {r.text}")

    # This route validates the configs for files we just pushed and, if there are no
    # errors it then creates a semantic model from those configs in the backend database
    commit_url = f"{api_url}/api/v1/model/{repo}/{branch}/{commit}/commit_model"
    logger.info(f"commit_url: {commit_url}")
    logger.info("Committing model")
    r = requests.post(
        commit_url,
        headers=headers,
        verify=verify,
        json=json.dumps({"is_current": False, "is_validation": is_validation, "return_issues": return_issues}),
    )
    if r.status_code != 200:
        err_msg = _err_msg_from_err_response(r)
        raise Exception(err_msg)
    logger.info("Successfully committed configs")

    return r


def commit_configs_as_primary(
    auth_header: Dict[str, str],
    repo: str,
    branch: str,
    commit: str,
    config_dir: str = LOCAL_DIR_DEFAULT,  # default to local dir
    api_url: str = TRANSFORM_API_URL,  # default to prod api
    return_issues: bool = False,
) -> requests.Response:
    """Creates a model from the configs and makes it the primary model

    Parses configs, runs semantic validations, and creates a validated model
    configswhich is immediately made primary for the organization if it doesn't
    have blocking validation issues
    """

    # if return_issues == False, the http response will be an error if there
    # are blocking issues
    # if return_issues == True, the http response will be json and include
    # issues
    response = commit_configs(
        auth_header=auth_header,
        repo=repo,
        branch=branch,
        commit=commit,
        config_dir=config_dir,
        is_validation=False,
        api_url=api_url,
        return_issues=return_issues,
    )

    json_resp = response.json()
    # the only case where the resp wont have an "issues" key is if
    # return_issues == False AND there are blocking issues during validation
    # because in that case, the backend returns and http error response
    if "issues" in json_resp:
        results = ModelValidationResults.parse_raw(json_resp["issues"])

        # only promote the model if there aren't blocking issues
        if not results.has_blocking_issues:
            promote_model(
                auth_header=auth_header,
                repo=repo,
                branch=branch,
                commit=commit,
                api_url=api_url,
            )

    return response


def validate_configs(
    auth_header: Dict[str, str],
    repo: str,
    branch: str,
    commit: str,
    config_dir: str = LOCAL_DIR_DEFAULT,  # default to local dir
    api_url: str = TRANSFORM_API_URL,  # default to prod api
    return_issues: bool = False,
) -> requests.Response:
    """Parses configs, runs semantic validations, and creates a validation model"""
    return commit_configs(
        auth_header=auth_header,
        repo=repo,
        branch=branch,
        commit=commit,
        config_dir=config_dir,
        is_validation=True,
        api_url=api_url,
        return_issues=return_issues,
    )


def promote_model(
    auth_header: Dict[str, str],
    repo: str,
    branch: str,
    commit: str,
    api_url: str = TRANSFORM_API_URL,  # default to prod api
) -> requests.Response:
    """Promotes an existing model to be the primary model for an organization"""
    verify = api_url.startswith("https")
    promote_url = f"{api_url}/api/v1/model/{repo}/{branch}/{commit}/promote"

    logger.info(f"promote_url: {promote_url}")
    logger.info("Promoting model")
    r = requests.post(promote_url, headers=auth_header, verify=verify)
    if r.status_code != 200:
        err_msg = _err_msg_from_err_response(r)
        raise Exception(err_msg)

    logger.info("Successfully promoted model")
    return r


if __name__ == "__main__":
    mode = sys.argv[1]
    IS_CURRENT = None
    IS_VALIDATION = False
    if mode != UPLOAD_MODE_VALIDATE and mode != UPLOAD_MODE_COMMIT:
        raise ValueError(f"Invalid upload mode ({mode}) passed via args.")

    model_details: RequiredModelDetails
    if os.getenv("SOURCE_CONTROL") == "GITLAB":
        model_details = parse_gitlab()
    elif os.getenv("SOURCE_CONTROL") == "BITBUCKET":
        model_details = parse_bitbucket()
    elif os.getenv("SOURCE_CONTROL") == "GITHUB":
        model_details = parse_github()
    else:
        # default: use Github
        model_details = parse_github()

    API_URL = os.getenv("TRANSFORM_API_URL", TRANSFORM_API_URL)

    TRANSFORM_CONFIG_DIR = os.getenv("TRANSFORM_CONFIG_DIR")
    if TRANSFORM_CONFIG_DIR:
        TRANSFORM_CONFIG_DIR = TRANSFORM_CONFIG_DIR.lstrip().rstrip()
    TRANSFORM_API_KEY = os.environ["TRANSFORM_API_KEY"].lstrip().rstrip()  # fail if TRANSFORM_API_KEY not present
    auth_header = {"Authorization": f"X-Api-Key {TRANSFORM_API_KEY}"}

    # This protects againsts the case where the varaible is None, making it "None"
    # In practice we've only seen this in our own org, and way back in March of 2021,
    # but I'd rather be safe than sorry
    REPO = f"{model_details.REPO}"
    BRANCH = f"{model_details.BRANCH}"
    COMMIT = f"{model_details.COMMIT}"

    # Clean up branch name because people like to put slashes in their branch names
    if "/" in BRANCH:
        BRANCH = BRANCH.replace("/", "__")  # dunder, for readability... to the extent it matters

    if "/" in REPO:
        REPO = REPO.replace("/", "__")

    lint_results = ConfigLinter().lint_dir(TRANSFORM_CONFIG_DIR or LOCAL_DIR_DEFAULT)
    if lint_results.has_blocking_issues:
        _print_issues(lint_results)
        sys.exit(1)

    try:
        if mode == UPLOAD_MODE_VALIDATE:
            validate_configs(
                auth_header=auth_header,
                repo=REPO,
                branch=BRANCH,
                commit=COMMIT,
                config_dir=TRANSFORM_CONFIG_DIR or LOCAL_DIR_DEFAULT,
                api_url=API_URL,
            )
        else:  # mode == UPLOAD_MODE_COMMIT
            commit_configs_as_primary(
                auth_header=auth_header,
                repo=REPO,
                branch=BRANCH,
                commit=COMMIT,
                config_dir=TRANSFORM_CONFIG_DIR or LOCAL_DIR_DEFAULT,
                api_url=API_URL,
            )
    except Exception as e:
        print(e)
        sys.exit(1)

    print("success")
