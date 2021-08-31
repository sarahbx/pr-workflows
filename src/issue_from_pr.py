import contextlib


def issue_from_pr(repo, pull):
    with contextlib.suppress(AssertionError):
        issue = repo.get_issue(pull.title)

    if not issue:
        issue = repo.create_issue(f"{pull.title} #{pull.number}")
        issue.add_to_assignees(issue.user)
