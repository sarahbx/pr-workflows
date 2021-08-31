def issue_from_pr(repo, pull):
    issue = repo.create_issue(f"{pull.title} #{pull.number}")
    issue.add_to_assignees(issue.user)
