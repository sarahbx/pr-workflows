from src.utils import get_labels


def remove_verified_label(pull):
    label = "Verified"
    labels = get_labels(pull=pull)
    if label in labels:
        pull.remove_from_labels(label)


def labels_by_user_input(**kwargs):
    data, pull = kwargs["data"], kwargs["pull"]
    body = data["comment"]["body"]
    label = "Verified"
    if "/verified" in body and label not in get_labels(pull=pull):
        print(f"Adding {label} to {pull.title}")
        pull.add_to_labels(label)

    if "/unverified" in body:
        print(f"Removing {label} from {pull.title}")
        remove_verified_label(pull=pull)
