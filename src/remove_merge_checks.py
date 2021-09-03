from src.constants import LABEL_APPROVE, LABEL_VERIFIED, READY_FOR_MERGE
from src.utils import (
    remove_label,
    set_commit_status_pending_no_approve,
    set_commit_status_pending_no_verify,
)


def remove_merge_checks(pull):
    last_commit = list(pull.get_commits())[-1]
    remove_label(pull=pull, label=LABEL_VERIFIED)
    remove_label(pull=pull, label=LABEL_APPROVE)
    remove_label(pull=pull, label=READY_FOR_MERGE)
    set_commit_status_pending_no_verify(commit=last_commit)
    set_commit_status_pending_no_approve(commit=last_commit)
