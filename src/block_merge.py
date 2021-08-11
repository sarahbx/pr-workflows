from src.constants import LABEL_VERIFIED


def block_merge_no_verify(pull):
    context = "Verified label"
    labels = pull.get_labels()
    last_commit = list(pull.get_commits())[-1]
    if LABEL_VERIFIED not in labels:
        last_commit.create_status(
            state="pending", description="Missing Verified label", context=context
        )

    else:
        last_commit.create_status(
            state="success", description="Missing Verified label", context=context
        )
