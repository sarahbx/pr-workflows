def _get_issue_title(pull):
    return f"[ISSUE] {pull.title}"


def _get_issue_info(issue):
    return f"{issue.title} #{issue.number} state: {issue.state}"


def _get_issue(repo, pull):
    issue_title = _get_issue_title(pull=pull)
    for _issue in repo.get_issues():
        if _issue.title == issue_title and _issue.state == "open":
            print(_get_issue_info(issue=_issue))
            return _issue


def issue_from_pr(repo, pull):
    issue_title = _get_issue_title(pull=pull)
    if not _get_issue(repo=repo, pull=pull):
        print(f"Create issue for PR: {issue_title} #{pull.number}")
        issue = repo.create_issue(title=issue_title)
        issue.add_to_assignees(issue.user)
        issue.create_comment(body=f"Address #{pull.number}")


def close_issue_from_pr(repo, pull):
    issue = _get_issue(repo=repo, pull=pull)
    print(f"Closing issue {issue.title} #{issue.number} for pull {pull.number}")
    issue.edit(state="closed")
