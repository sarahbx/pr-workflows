from src.constants import (
    BLOCK_MERGE_SEMVER_CONTEXT,
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_APPROVE,
    LABEL_VERIFIED,
    NEEDS_MAINTAINERS_APPROVE,
    READY_FOR_MERGE,
    STATE_PENDING,
    STATE_SUCCESS,
    STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
    STATUS_DESCRIPTION_MISSING_VERIFIED,
)
from src.utils import (
    add_label,
    add_remove_labels,
    get_labels,
    get_repo_approvers,
    get_semver_label_data,
    remove_label,
)


def labels_by_user_input(event_data, pull):
    commented_user = event_data["comment"]["user"]["login"]
    body = event_data["comment"]["body"]
    last_commit = list(pull.get_commits())[-1]
    if f"/{LABEL_VERIFIED}".lower() in body and LABEL_VERIFIED not in get_labels(
        pull=pull
    ):
        add_label(pull=pull, label=LABEL_VERIFIED)
        last_commit.create_status(
            state=STATE_SUCCESS,
            description="Verified label exists",
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )

    if f"/un{LABEL_VERIFIED}".lower() in body:
        remove_label(pull=pull, label=LABEL_VERIFIED)
        remove_label(pull=pull, label=READY_FOR_MERGE)

        last_commit.create_status(
            state=STATE_PENDING,
            description=STATUS_DESCRIPTION_MISSING_VERIFIED,
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )

    (
        semver_status_state,
        semver_status_description,
        semver_labels_to_add,
        semver_labels_to_remove,
    ) = get_semver_label_data(pull=pull, body=body)
    semver_modified = add_remove_labels(
        pull=pull,
        labels_to_add=semver_labels_to_add,
        labels_to_remove=semver_labels_to_remove,
    )

    last_commit.create_status(
        state=semver_status_state,
        description=semver_status_description,
        context=BLOCK_MERGE_SEMVER_CONTEXT,
    )

    if commented_user in get_repo_approvers():
        if f"/{LABEL_APPROVE}".lower() in body and LABEL_APPROVE not in get_labels(
            pull=pull
        ):
            add_label(pull=pull, label=LABEL_APPROVE)
            last_commit.create_status(
                state=STATE_SUCCESS,
                description="Approved by maintainers",
                context=NEEDS_MAINTAINERS_APPROVE,
            )

        if f"/un{LABEL_APPROVE}".lower() in body or semver_modified:
            remove_label(pull=pull, label=LABEL_APPROVE)
            remove_label(pull=pull, label=READY_FOR_MERGE)

            last_commit.create_status(
                state=STATE_PENDING,
                description=STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
                context=NEEDS_MAINTAINERS_APPROVE,
            )
