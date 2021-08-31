def issue_from_pr(repo, pull):
    issue_title = f"[ISSUE] {pull.title}"

    def _issue_exists():
        for _issue in repo.get_issues():
            if _issue.title == issue_title and _issue.state == "open":
                print(f"{_issue.title} #{_issue.number} state: {_issue.state}")
                print(f"Issue already exists for PR {issue_title} #{pull.number}")
                return True

    if not _issue_exists():
        print(f"Create issue for PR: {issue_title} #{pull.number}")
        issue = repo.create_issue(issue_title)
        issue.add_to_assignees(issue.user)
        issue.create_comment(f"Address #{pull.number}")
