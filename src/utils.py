import contextlib
import os

import yaml
from github.GithubException import UnknownObjectException


def get_pull_from_data(event_data, repo):
    pull_number = event_data.get("number")
    if not pull_number:
        pull_number = event_data.get("issue", {}).get("number")

    if not pull_number:
        pull_number = event_data.get("pull_request", {}).get("number")

    if pull_number:
        print(f"pull number is {pull_number}")
        with contextlib.suppress(UnknownObjectException):
            return repo.get_pull(number=pull_number)

    else:
        _pull, _ = get_pull_and_commit_by_commit_sha(event_data=event_data, repo=repo)
        return _pull


def get_pull_and_commit_by_commit_sha(event_data, repo):
    try:
        commit_sha = event_data["commits"][-1]["id"]
    except KeyError:
        commit_sha = event_data.get("commit", {}).get("sha")

    if commit_sha:
        print(f"Current commit sha is: {commit_sha}")
        for pull in repo.get_pulls():
            for commit in pull.get_commits():
                if commit.sha == commit_sha:
                    return pull, commit

    print(f"commit sha not found in {event_data}")
    return None, None


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def set_commit_status(commit, state, description, context):
    commit.create_status(
        state=state,
        description=description,
        context=context,
    )


def remove_label(pull, label):
    labels = get_labels(pull=pull)
    if label in labels:
        print(f"Remove {label} from {pull.title}")
        pull.remove_from_labels(label=label)


def add_label(pull, label):
    print(f"Adding {label} to {pull.title}")
    pull.add_to_labels(label)


def get_repo_approvers():
    with open("OWNERS", "r") as fd:
        data = yaml.load(stream=fd.read(), Loader=yaml.SafeLoader)

    return data["approvers"]


def print_os_environment():
    """
    Utility function for debugging.
    """
    for key, val in os.environ.items():
        print(f"{key}: {val}")
