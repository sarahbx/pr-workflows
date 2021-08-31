def _get_issue_title(pull):
    return f"[ISSUE] {pull.title}"


def _get_issue(repo, pull, issue_title):
    for _issue in repo.get_issues():
        if _issue.title == issue_title and _issue.state == "open":
            print(f"{_issue.title} #{_issue.number} state: {_issue.state}")
            print(f"Issue already exists for PR {issue_title} #{pull.number}")
            return _issue


def issue_from_pr(repo, pull):
    issue_title = _get_issue_title(pull=pull)
    if not _get_issue(repo=repo, pull=pull, issue_title=issue_title):
        print(f"Create issue for PR: {issue_title} #{pull.number}")
        issue = repo.create_issue(issue_title)
        issue.add_to_assignees(issue.user)
        issue.create_comment(f"Address #{pull.number}")


def close_issue(repo, pull):
    issue = _get_issue(repo=repo, pull=pull, issue_title=_get_issue_title(pull=pull))
    print(f"Close issue {issue.title} #{issue.number}")
    issue.edit(state="closed")
