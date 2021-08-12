from src.constants import LABEL_APPROVE, LABEL_VERIFIED
from src.utils import (
    add_label,
    get_labels,
    remove_label,
    set_commit_status_pending_no_approve,
    set_commit_status_pending_no_verify,
    set_commit_status_success_approve,
    set_commit_status_success_verify,
)


def labels_by_user_input(data, pull):
    body = data["comment"]["body"]
    last_commit = list(pull.get_commits())[-1]
    if f"/{LABEL_VERIFIED}" in body and LABEL_VERIFIED not in get_labels(pull=pull):
        add_label(pull=pull, label=LABEL_VERIFIED)
        set_commit_status_success_verify(commit=last_commit)

    if f"/un{LABEL_VERIFIED}" in body:
        remove_label(pull=pull, label=LABEL_VERIFIED)
        set_commit_status_pending_no_verify(commit=last_commit)

    if f"/{LABEL_APPROVE}" in body and LABEL_APPROVE not in get_labels(pull=pull):
        add_label(pull=pull, label=LABEL_APPROVE)
        set_commit_status_success_approve(commit=last_commit)

    if f"/un{LABEL_APPROVE}" in body:
        remove_label(pull=pull, label=LABEL_APPROVE)
        set_commit_status_pending_no_approve(commit=last_commit)
