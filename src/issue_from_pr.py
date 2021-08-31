def _get_issue_title(pull):
    return f"[ISSUE] {pull.title}"


def _get_issue_info(issue):
    return f"{issue.title} #{issue.number} state: {issue.state}"


def _get_issue(repo, pull, issue_title):
    for _issue in repo.get_issues():
        if _issue.title == issue_title and _issue.state == "open":
            print(_get_issue_info(issue=_issue))
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
    if issue:
        if pull.state != "open":
            print(
                f"Pull {pull.title} is {pull.state}. not closing issue {_get_issue_info(issue=issue)}"
            )
            return

        print(f"Closing issue {issue.title} #{issue.number}")
        issue.edit(state="closed")
