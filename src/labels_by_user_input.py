from src.utils import get_labels


LABEL_VERIFIED = "Verified"


def remove_verified_label(pull):
    labels = get_labels(pull=pull)
    if LABEL_VERIFIED in labels:
        print(f"Remove {LABEL_VERIFIED} from {pull.title}")
        pull.remove_from_labels(LABEL_VERIFIED)


def labels_by_user_input(data, pull):
    body = data["comment"]["body"]
    if "/verified" in body and LABEL_VERIFIED not in get_labels(pull=pull):
        print(f"Adding {LABEL_VERIFIED} to {pull.title}")
        pull.add_to_labels(LABEL_VERIFIED)
        last_commit = list(pull.get_commits())[-1]
        last_commit.create_status(
            state="pending",
            description="Missing Verified label",
            context="Verified label",
        )

    if "/unverified" in body:
        remove_verified_label(pull=pull)
