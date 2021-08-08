from github.GithubException import GithubException


def add_reviewers(data, pull, reviewers):
    reviewers = [reviewer.strip() for reviewer in reviewers.split(",")]
    for reviewer in reviewers:
        try:
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])
        except GithubException as exp:
            # author ot the user who pushed cannot be add as reviewers
            print(f"Failed to add {reviewer}: {exp}")
