import os

import yaml

from src.constants import BLOCK_MERGE_VERIFY_CONTEXT, NEEDS_MAINTAINERS_APPROVE


def get_pull_from_data(event_data, repo):
    pull_number = event_data.get("number")
    if not pull_number:
        pull_number = event_data.get("issue", {}).get("number")

    if not pull_number:
        pull_number = event_data.get("pull_request", {}).get("number")

    if pull_number:
        return repo.get_pull(pull_number)

    else:
        return get_pull_from_commit(event_data=event_data, repo=repo)


def get_pull_from_commit(event_data, repo):
    print_os_environment()
    print(event_data)
    commit_sha = event_data.get("commit", {}).get("sha")
    if commit_sha:
        print(f"Current commit sha is: {commit_sha}")
        for pull in repo.get_pulls():
            for commit in pull.get_commits():
                if commit.sha == commit_sha:
                    return pull

    print(f"commit sha not found in {event_data}")


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def set_commit_status_success_verify(commit):
    commit.create_status(
        state="success",
        description="Verified label exists",
        context=BLOCK_MERGE_VERIFY_CONTEXT,
    )


def set_commit_status_pending_no_verify(commit):
    commit.create_status(
        state="pending",
        description="Missing Verified",
        context=BLOCK_MERGE_VERIFY_CONTEXT,
    )


def set_commit_status_pending_no_approve(commit):
    commit.create_status(
        state="pending",
        description="Needs approve from maintainers",
        context=NEEDS_MAINTAINERS_APPROVE,
    )


def set_commit_status_success_approve(commit):
    commit.create_status(
        state="success",
        description="Approved by maintainers",
        context=NEEDS_MAINTAINERS_APPROVE,
    )


def remove_label(pull, label):
    labels = get_labels(pull=pull)
    if label in labels:
        print(f"Remove {label} from {pull.title}")
        pull.remove_from_labels(label)


def add_label(pull, label):
    print(f"Adding {label} to {pull.title}")
    pull.add_to_labels(label)


def get_repo_approvers():
    with open("OWNERS", "r") as fd:
        data = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    return data["approvers"]


def print_os_environment():
    """
    Utility function for debugging.
    """
    for key, val in os.environ.items():
        print(f"{key}: {val}")
