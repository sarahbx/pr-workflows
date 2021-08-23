from src.constants import LABEL_APPROVE, LABEL_VERIFIED
from src.utils import (
    add_label,
    add_remove_labels,
    check_body_for_semver_labels,
    get_labels,
    get_repo_approvers,
    remove_label,
    semver_labels_exist_in_pr,
    set_commit_status_pending_no_approve,
    set_commit_status_pending_no_semver,
    set_commit_status_pending_no_verify,
    set_commit_status_success_approve,
    set_commit_status_success_semver,
    set_commit_status_success_verify,
)


def labels_by_user_input(data, pull, commented_user):
    body = data["comment"]["body"]
    last_commit = list(pull.get_commits())[-1]
    if f"/{LABEL_VERIFIED}".lower() in body and LABEL_VERIFIED not in get_labels(
        pull=pull
    ):
        add_label(pull=pull, label=LABEL_VERIFIED)
        set_commit_status_success_verify(commit=last_commit)

    if f"/un{LABEL_VERIFIED}".lower() in body:
        remove_label(pull=pull, label=LABEL_VERIFIED)
        set_commit_status_pending_no_verify(commit=last_commit)

    if commented_user in get_repo_approvers():
        if f"/{LABEL_APPROVE}".lower() in body and LABEL_APPROVE not in get_labels(
            pull=pull
        ):
            add_label(pull=pull, label=LABEL_APPROVE)
            set_commit_status_success_approve(commit=last_commit)

        if f"/un{LABEL_APPROVE}".lower() in body:
            remove_label(pull=pull, label=LABEL_APPROVE)
            set_commit_status_pending_no_approve(commit=last_commit)

    new_labels, remove_labels = check_body_for_semver_labels(body=body)
    if (
        (new_labels or remove_labels)
        and add_remove_labels(
            pull=pull, new_labels=new_labels, remove_labels=remove_labels
        )
    ) or semver_labels_exist_in_pr(pull):
        set_commit_status_success_semver(commit=last_commit)
    else:
        set_commit_status_pending_no_semver(commit=last_commit)
