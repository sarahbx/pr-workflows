from src.constants import LABEL_VERIFIED
from src.utils import get_labels


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

    if "/unverified" in body:
        remove_verified_label(pull=pull)
