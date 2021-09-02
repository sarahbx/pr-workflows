from src.constants import (
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_APPROVE,
    LABEL_VERIFIED,
    READY_FOR_MERGE,
    NEEDS_MAINTAINERS_APPROVE,
    STATE_PENDING,
)
from src.utils import remove_label, set_commit_status


def remove_merge_checks(pull):
    last_commit = list(pull.get_commits())[-1]
    remove_label(pull=pull, label=LABEL_VERIFIED)
    remove_label(pull=pull, label=LABEL_APPROVE)
    remove_label(pull=pull, label=READY_FOR_MERGE)
    remove_label(pull=pull, label=READY_FOR_MERGE)
    set_commit_status(
        commit=last_commit,
        state=STATE_PENDING,
        description="Missing Verified",
        context=BLOCK_MERGE_VERIFY_CONTEXT,
    )
    set_commit_status(
        commit=last_commit,
        state=STATE_PENDING,
        description="Needs approve from maintainers",
        context=NEEDS_MAINTAINERS_APPROVE,
    )
