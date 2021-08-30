import json
import os

import github

from src.add_reviewers import add_reviewers
from src.block_offensive_lanague import block_offensive_language
from src.labels_by_user_input import labels_by_user_input
from src.merge_status_label import merge_status_label
from src.remove_merge_checks import remove_merge_checks
from src.size_label_prs import size_label_prs
from src.upload_to_pypi import upload_to_pypi
from src.utils import get_commit_from_data, get_pull_from_data


if __name__ == "__main__":
    token = os.environ["INPUT_TOKEN"]
    action = os.environ["INPUT_ACTION"]
    github = github.Github(token)
    repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
    commit = repo.get_commit(os.environ["GITHUB_SHA"])

    with open(os.environ["GITHUB_EVENT_PATH"], "r") as fd:
        data = json.load(fd)

    pull = get_pull_from_data(event_data=data, repo=repo)

    if action == "remove_merge_checks":
        remove_merge_checks(pull=pull)

    if action == "labels_by_user_input":
        labels_by_user_input(data=data, pull=pull)

    if action == "add_reviewers":
        reviewers = os.environ["INPUT_REVIEWERS"]
        add_reviewers(pull=pull, reviewers=reviewers)

    if action == "size_label_prs":
        size_label_prs(pull=pull)

    if action == "block_offensive_language":
        block_offensive_language(pull=pull)

    if action == "upload_to_pypi":
        upload_to_pypi()

    if action == "merge_status_label":
        commit = get_commit_from_data(event_data=data, repo=repo)
        merge_status_label(pull=pull, commit=commit)
