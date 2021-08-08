def add_reviewers(data, pull, reviewers):
    reviewers = [reviewer.strip() for reviewer in reviewers.split(",")]
    author = [data["sender"]["login"]]
    current_reviewers_requests = data["pull_request"]["requested_reviewers"]
    for reviewer in reviewers:
        if reviewer not in current_reviewers_requests + author + pull.user:
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])
