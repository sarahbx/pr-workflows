import re

import yaml

from src.constants import (
    BLOCK_MERGE_SEMVER_CONTEXT,
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_SEMVER_PREFIX,
    LABELS_SEMVER_MAJOR,
    LABELS_SEMVER_MINOR,
    LABELS_SEMVER_PATCH,
    NEEDS_MAINTAINERS_APPROVE,
)


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


def set_commit_status_success_semver(commit):
    commit.create_status(
        state="success",
        description="Semver label exists",
        context=BLOCK_MERGE_SEMVER_CONTEXT,
    )


def set_commit_status_pending_no_semver(commit):
    commit.create_status(
        state="pending",
        description="Missing Semver label",
        context=BLOCK_MERGE_SEMVER_CONTEXT,
    )


def check_body_for_semver_labels(body):
    new_labels = []
    remove_labels = []
    if re.match(r"^.*\B/major\b.*$", body):
        new_labels = LABELS_SEMVER_MAJOR
        remove_labels = LABELS_SEMVER_MINOR + LABELS_SEMVER_PATCH
    elif re.match(r"^.*\B/minor\b.*$", body):
        new_labels = LABELS_SEMVER_MINOR
        remove_labels = LABELS_SEMVER_MAJOR + LABELS_SEMVER_PATCH
    elif re.match(r"^.*\B/patch\b.*$", body):
        new_labels = LABELS_SEMVER_PATCH
        remove_labels = LABELS_SEMVER_MAJOR + LABELS_SEMVER_MINOR

    return new_labels, remove_labels


def semver_labels_exist_in_pr(pull):
    current_labels = get_labels(pull=pull)
    for label in current_labels:
        if label.startswith(f"{LABEL_SEMVER_PREFIX}/"):
            return True


def add_remove_labels(pull, new_labels, remove_labels):
    found_existing_label = False
    new_label_added = False

    current_labels = get_labels(pull=pull)
    for label in current_labels:
        if label in remove_labels:
            print(f"Remove {label} from {pull.title}")
            pull.remove_from_labels(label)
        elif label in new_labels:
            print(f"Label {label} already exists in {pull.title}")
            new_labels = list(set(new_labels) - {label})
            found_existing_label = True

    for new_label in new_labels:
        add_label(pull=pull, label=new_label)
        new_label_added = True

    return found_existing_label or new_label_added
