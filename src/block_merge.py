def block_merge_no_verify(pull):
    context = "Verified label"
    last_commit = list(pull.get_commits())[-1]
    last_commit.create_status(
        state="pending", description="Missing Verified label", context=context
    )
