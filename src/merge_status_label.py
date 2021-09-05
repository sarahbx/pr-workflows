from src.constants import READY_FOR_MERGE
from src.utils import add_label, get_labels, remove_label


def merge_status_label(pull, commit):
    if not commit:
        print("No commit given")
        return

    label = READY_FOR_MERGE
    if commit.get_combined_status().state == "success":
        add_label(pull=pull, label=label)
    else:
        if label in get_labels(pull=pull):
            remove_label(pull=pull, label=label)
