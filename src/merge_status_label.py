from src.utils import add_label


def merge_status_label(pull):
    if pull.mergeable_state == "stable":
        add_label(pull=pull, label="Ready for merge")
