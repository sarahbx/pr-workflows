from src.utils import get_labels


def size_label_prs(data, pull):
    labels = get_labels(pull=pull)
    additions = data["pull_request"]["additions"]

    comment = None
    if additions < 20:
        label = "Size/XS"

    elif additions < 50:
        label = "Size/S"

    elif additions < 100:
        label = "Size/M"

    elif additions < 300:
        label = "Size/L"

    elif additions < 500:
        label = "Size/XL"

    else:
        label = "Size/XXL"
        comment = "Please try to break up this PR, it is very large."

    if label.lower() in [lb.lower() for lb in labels]:
        return

    else:
        print(f"Labeling {pull.title}: {label}")
        [pull.remove_from_labels(lb) for lb in labels if lb.lower().startswith("size/")]
        pull.add_to_labels(label)
        if comment:
            print(f"Commenting on {pull.title!r}: {comment!r}")
            pull.create_review(body=comment)
