from src.constants import (
    BLOCK_MERGE_SEMVER_CONTEXT,
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_APPROVE,
    LABEL_VERIFIED,
    NEEDS_MAINTAINERS_APPROVE,
    READY_FOR_MERGE,
    SEMVER_LABELS_LIST,
    SEMVER_USER_INPUT_LABELS_MAP,
    STATE_PENDING,
    STATE_SUCCESS,
    STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
    STATUS_DESCRIPTION_MISSING_VERIFIED,
    STATUS_DESCRIPTION_SEMVER_LABELS_EXIST,
    STATUS_DESCRIPTION_SEMVER_LABELS_MISSING,
)
from src.utils import (
    add_label,
    add_remove_labels,
    get_labels,
    get_repo_approvers,
    get_semver_user_input,
    remove_label,
    semver_labels_in_pull_labels,
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

        if f"/un{LABEL_APPROVE}".lower() in body:
            remove_label(pull=pull, label=LABEL_APPROVE)
            remove_label(pull=pull, label=READY_FOR_MERGE)

            last_commit.create_status(
                state=STATE_PENDING,
                description=STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
                context=NEEDS_MAINTAINERS_APPROVE,
            )

    semver_key = get_semver_user_input(body=body)
    existing_semver_labels = semver_labels_in_pull_labels(pull=pull)
    if semver_key or existing_semver_labels:
        if (
            semver_key
            and SEMVER_USER_INPUT_LABELS_MAP[semver_key] not in existing_semver_labels
        ):
            add_remove_labels(
                pull=pull,
                labels_to_add=[SEMVER_USER_INPUT_LABELS_MAP[semver_key]],
                labels_to_remove=list(
                    SEMVER_LABELS_LIST - {SEMVER_USER_INPUT_LABELS_MAP[semver_key]}
                ),
            )
        last_commit.create_status(
            state=STATE_SUCCESS,
            description=STATUS_DESCRIPTION_SEMVER_LABELS_EXIST,
            context=BLOCK_MERGE_SEMVER_CONTEXT,
        )

    else:
        last_commit.create_status(
            state=STATE_PENDING,
            description=STATUS_DESCRIPTION_SEMVER_LABELS_MISSING,
            context=BLOCK_MERGE_SEMVER_CONTEXT,
        )
