from src.utils import add_label, get_labels, remove_label


def merge_status_label(data, repo):
    label = "Ready for merge"
    commit = repo.get_commit(data["commit"]["sha"])
    pull = list(commit.get_pulls())[0]
    if commit.get_combined_status().state == "success":
        add_label(pull=pull, label=label)
    else:
        if label in get_labels(pull=pull):
            remove_label(pull=pull, label=label)
