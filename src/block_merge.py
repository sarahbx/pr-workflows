from src.utils import set_commit_status_pending


def block_merge_no_verify(pull):
    last_commit = list(pull.get_commits())[-1]
    set_commit_status_pending(commit=last_commit)
