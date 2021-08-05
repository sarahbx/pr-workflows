import json
import os

import github

from src.add_reviewers import add_reviewers
from src.labels_by_user_input import labels_by_user_input
from src.size_label_prs import size_label_prs

ACTIONS = {
    "labels_by_user_input": labels_by_user_input,
    "add_reviewers": add_reviewers,
    "size_label_prs": size_label_prs,
}


if __name__ == "__main__":
    token = os.environ["INPUT_TOKEN"]
    reviewers = os.environ["INPUT_REVIEWERS"]
    action = os.environ["INPUT_ACTION"]
    with open(os.environ.get("GITHUB_EVENT_PATH"), "r") as fd:
        data = json.load(fd)

    github = github.Github(token)
    repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
    commit = repo.get_commit(os.environ.get("GITHUB_SHA"))
    try:
        issue_number = data["number"]
    except KeyError:
        issue_number = data["issue"]["number"]

    pull = repo.get_pull(issue_number)

    ACTIONS[action](data=data, pull=pull, reviewers=reviewers)
