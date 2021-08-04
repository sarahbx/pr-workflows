import datetime
import json
import os
import github


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def labels_by_user_input(data, pull):
    body = data["comment"]["body"]
    label = "Verified"
    if "/verified" in body and label not in get_labels(pull=pull):
        print(f"Adding {label} to {pull.title}")
        pull.add_to_labels(label)


def remove_verified_label(data, pull):
    label = "Verified"
    labels = get_labels(pull=pull)
    if label in labels:
        pull.remove_from_labels(label)


def add_reviewers(data, pull):
    reviewers = ["myakove"]
    author = [data["sender"]["login"]]
    current_reviewers_requests = data["pull_request"]["requested_reviewers"]
    for reviewer in reviewers:
        if reviewer not in current_reviewers_requests + author:
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])


def size_label_prs(data, pull):
    labels = get_labels(pull=pull)
    additions = data["pull_request"]["additions"]
    label = None
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
        [pull.remove_from_labels(lb) for lb in labels if lb.startswith("Size/")]
        pull.add_to_labels(label)


if __name__ == "__main__":
    token = os.environ['INPUT_TOKEN']
    event_type = os.environ["GITHUB_EVENT_NAME"]
    print(event_type)
    print(os.environ.get("GITHUB_EVENT_PATH"))
    print(os.environ.get("GITHUB_SHA"))
    print(os.environ.get("GITHUB_REF"))
    with open(os.environ.get("GITHUB_EVENT_PATH"), "r") as fd:
        data = json.load(fd)

    print(data)
    github = github.Github(token)
    repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])
    commit = repo.get_commit(os.environ.get("GITHUB_SHA"))
    try:
        issue_number = data["number"]
    except KeyError:
        issue_number = data["issue"]["number"]

    pull = repo.get_pull(issue_number)

    if event_type == "pull_request_target":
        remove_verified_label(data=data, pull=pull)
        size_label_prs(data=data, pull=pull)
        add_reviewers(data=data, pull=pull)

    if event_type == "issue_comment":
        labels_by_user_input(data=data, pull=pull)


