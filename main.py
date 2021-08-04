import json
import os
import github


def add_reviewers(pull):
    current_reviewers_requests = [reviewer.login for reviewer in pull.get_review_requests()[0]]
    current_reviewers = set([reviewer.user.login for reviewer in pull.get_reviews()])
    for reviewer in ["myakove", "rnetser"]:
        if reviewer not in (current_reviewers_requests or current_reviewers):
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])


def size_label_prs(pull):
    label = None
    labels = [label.name for label in pull.get_labels()]
    additions = pull.raw_data["additions"]
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

    if label in labels:
        return

    else:
        print(f"Labeling {pull.title}: {label}")
        [pull.remove_from_labels(lb) for lb in labels if lb.startswith("Size:")]
        pull.add_to_labels(label)


if __name__ == "__main__":
    token = os.environ['INPUT_TOKEN']
    print(os.environ.get("GITHUB_EVENT_PATH"))
    print(os.environ.get("GITHUB_SHA"))
    print(os.environ.get("GITHUB_REF"))
    with open(os.environ.get("GITHUB_EVENT_PATH"), "r") as fd:
        data = json.load(fd)

    print(data)
    github = github.Github(token)
    repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])
    commit = repo.get_commit(os.environ.get("GITHUB_SHA"))
    pull = repo.get_pull(data["number"])
    size_label_prs(pull=pull)


