def add_reviewers(**kwargs):
    data, pull, reviewers = kwargs["data"], kwargs["pull"], kwargs["reviewers"]
    reviewers = [reviewer.strip() for reviewer in reviewers.split(",")]
    author = [data["sender"]["login"]]
    current_reviewers_requests = data["pull_request"]["requested_reviewers"]
    for reviewer in reviewers:
        if reviewer not in current_reviewers_requests + author:
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])
