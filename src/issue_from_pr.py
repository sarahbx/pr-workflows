def issue_from_pr(repo, pull):
    issue_title = f"{pull.title} #{pull.number}"
    try:
        issue = repo.get_issue(issue_title)
    except AssertionError:
        issue = repo.create_issue(issue_title)
        issue.add_to_assignees(issue.user)
