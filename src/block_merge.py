from src.utils import set_commit_status_pending_no_verify


NEEDS_MAINTAINERS_APPROVE = "Needs Maintainers Approve"


def block_merge_no_verify(pull):
    last_commit = list(pull.get_commits())[-1]
    set_commit_status_pending_no_verify(commit=last_commit)


def block_merge_no_approve(pull):
    last_commit = list(pull.get_commits())[-1]
    if list(pull.get_reviews())[-1].state == "APPROVED":
        last_commit.create_status(
            state="success",
            description="Maintainers approved",
            context=NEEDS_MAINTAINERS_APPROVE,
        )

    else:
        last_commit.create_status(
            state="pending",
            description="Needs approve from maintainers",
            context=NEEDS_MAINTAINERS_APPROVE,
        )
