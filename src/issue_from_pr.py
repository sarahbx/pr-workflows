def issue_from_pr(repo, pull):
    issue_title = pull.title
    try:
        repo.get_issue(issue_title)
    except AssertionError:
        issue = repo.create_issue(issue_title)
        issue.add_to_assignees(issue.user)
        issue.create_comment(f"Address #{pull.number}")
