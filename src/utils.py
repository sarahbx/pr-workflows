import contextlib
import os
import re

import yaml
from github.GithubException import UnknownObjectException

from src.constants import (
    LABEL_KEY_MAJOR,
    LABEL_KEY_MINOR,
    LABEL_KEY_PATCH,
    SEMVER,
    SEMVER_LABELS_LIST,
    SEMVER_USER_INPUT_LABELS_MAP,
    STATE_PENDING,
    STATE_SUCCESS,
    STATUS_DESCRIPTION_SEMVER_LABELS_EXIST,
    STATUS_DESCRIPTION_SEMVER_LABELS_MISSING,
)


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


def get_semver_user_input(body):
    match = re.match(
        rf".*\B/(?P<{SEMVER}>{LABEL_KEY_MAJOR}|{LABEL_KEY_MINOR}|{LABEL_KEY_PATCH})\b",
        body,
        re.IGNORECASE,
    )
    if match:
        return match.group(SEMVER).lower()


def semver_labels_in_pull_labels(pull):
    return [
        label in SEMVER_LABELS_LIST
        for label in get_labels(pull=pull)
        if label in SEMVER_LABELS_LIST
    ]


def add_remove_labels(pull, labels_to_add, labels_to_remove):
    label_removed = False
    new_labels_to_add = labels_to_add.copy()
    labels_from_pull = get_labels(pull=pull)

    for label in labels_from_pull:
        if label in labels_to_remove:
            remove_label(pull=pull, label=label)
            label_removed = True
        elif label in new_labels_to_add:
            print(f"Label {label} already exists in {pull.title}")
            new_labels_to_add.remove(label)

    for label in new_labels_to_add:
        add_label(pull=pull, label=label)

    return new_labels_to_add or label_removed


def get_semver_label_data(pull, body):
    labels_to_add = []
    labels_to_remove = []
    semver_key = get_semver_user_input(body=body)
    existing_semver_labels = semver_labels_in_pull_labels(pull=pull)

    if semver_key or existing_semver_labels:
        if (
            semver_key
            and SEMVER_USER_INPUT_LABELS_MAP[semver_key] not in existing_semver_labels
        ):
            labels_to_add = [SEMVER_USER_INPUT_LABELS_MAP[semver_key]]
            labels_to_remove = list(
                SEMVER_LABELS_LIST - {SEMVER_USER_INPUT_LABELS_MAP[semver_key]}
            )
        status_state = STATE_SUCCESS
        status_description = STATUS_DESCRIPTION_SEMVER_LABELS_EXIST
    else:
        status_state = STATE_PENDING
        status_description = STATUS_DESCRIPTION_SEMVER_LABELS_MISSING

    return status_state, status_description, labels_to_add, labels_to_remove
