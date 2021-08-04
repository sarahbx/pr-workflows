
import os
import github

# extracting all the input from environments
token = os.environ['INPUT_TOKEN']

github = github.Github(token)
# GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])
commit = repo.get_commit(os.environ.get("GITHUB_SHA"))
pull = list(commit.get_pulls())[0]

print(os.environ.get("GITHUB_EVENT_PATH"))
print(os.environ.get("GITHUB_SHA"))
print(os.environ.get("GITHUB_REF"))


def size_label_prs(pull):
    label = None
    labels = [label.name for label in pull.get_labels()]
    data = pull.raw_data
    additions = data["additions"]
    if additions < 20:
        label = "Size:XS"

    elif additions < 50:
        label = "Size:S"

    elif additions < 100:
        label = "Size:M"

    elif additions < 300:
        label = "Size:L"

    elif additions < 500:
        label = "Size:XL"

    if label in labels:
        return

    else:
        print(f"Labeling {pull.title}: {label}")
        [pull.remove_from_labels(lb) for lb in labels if lb.startswith("Size:")]
        pull.add_to_labels(label)
