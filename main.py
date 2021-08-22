import json
import os

import github

from src.add_reviewers import add_reviewers
from src.block_offensive_lanague import block_offensive_language
from src.constants import LABEL_APPROVE, LABEL_VERIFIED
from src.labels_by_user_input import labels_by_user_input
from src.size_label_prs import size_label_prs
from src.upload_to_pypi import upload_to_pypi
from src.utils import (
    remove_label,
    set_commit_status_pending_no_approve,
    set_commit_status_pending_no_verify,
)


def _get_pull_from_data(event_data):
    pull_number = event_data.get("number")
    if not pull_number:
        pull_number = event_data.get("issue", {}).get("number")

    if not pull_number:
        pull_number = event_data.get("pull_request", {}).get("number")

    if pull_number:
        return repo.get_pull(pull_number)


if __name__ == "__main__":
    token = os.environ["INPUT_TOKEN"]
    action = os.environ["INPUT_ACTION"]
    github = github.Github(token)
    repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
    commit = repo.get_commit(os.environ["GITHUB_SHA"])

    with open(os.environ["GITHUB_EVENT_PATH"], "r") as fd:
        data = json.load(fd)

    pull = _get_pull_from_data(event_data=data)

    if action == "remove_merge_checks":
        last_commit = list(pull.get_commits())[-1]
        remove_label(pull=pull, label=LABEL_VERIFIED)
        remove_label(pull=pull, label=LABEL_APPROVE)
        set_commit_status_pending_no_verify(commit=last_commit)
        set_commit_status_pending_no_approve(commit=last_commit)

    if action == "labels_by_user_input":
        print(data)
        labels_by_user_input(data=data, pull=pull)

    if action == "add_reviewers":
        reviewers = os.environ["INPUT_REVIEWERS"]
        add_reviewers(data=data, pull=pull, reviewers=reviewers)

    if action == "size_label_prs":
        size_label_prs(data=data, pull=pull)

    if action == "block_offensive_language":
        block_offensive_language(pull=pull)

    if action == "upload to pypi":
        upload_to_pypi(data=data)
