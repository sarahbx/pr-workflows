from src.constants import BLOCK_MERGE_VERIFY_CONTEXT


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def set_commit_status_pending_no_verify(commit):
    commit.create_status(
        state="pending",
        description="Missing Verified label",
        context=BLOCK_MERGE_VERIFY_CONTEXT,
    )
