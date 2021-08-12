from src.utils import set_commit_status_pending_no_verify


NEEDS_MAINTAINERS_APPROVE = "Needs Maintainers Approve"


def _get_approved_commit(pull):
    reviews = list(pull.get_reviews())
    approved = [review for review in reviews if review.state == "APPROVED"]
    return approved[0] if approved else None


def block_merge_no_verify(pull):
    last_commit = list(pull.get_commits())[-1]
    set_commit_status_pending_no_verify(commit=last_commit)


def block_merge_no_approve(pull):
    last_commit = list(pull.get_commits())[-1]
    approved = _get_approved_commit(pull=pull)
    print(approved)
    if approved:
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


def remove_approved_on_code_change(pull):
    approved = _get_approved_commit(pull=pull)
    if approved:
        approved.dismiss("code change: Auto-dismissing Approve state")
