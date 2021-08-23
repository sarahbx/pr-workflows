BLOCK_MERGE_SEMVER_CONTEXT = "Semver label"
BLOCK_MERGE_VERIFY_CONTEXT = "Verified label"

LABEL_VERIFIED = "Verified"
LABEL_APPROVE = "Approve"
NEEDS_MAINTAINERS_APPROVE = "Needs Maintainers Approve"

LABEL_SEMVER_PREFIX = "semver"
LABELS_SEMVER_MAJOR = [
    f"{LABEL_SEMVER_PREFIX}/major",
    f"{LABEL_SEMVER_PREFIX}/breaking-change",
]
LABELS_SEMVER_MINOR = [
    f"{LABEL_SEMVER_PREFIX}/minor",
    f"{LABEL_SEMVER_PREFIX}/non-breaking-feature",
]
LABELS_SEMVER_PATCH = [
    f"{LABEL_SEMVER_PREFIX}/patch",
    f"{LABEL_SEMVER_PREFIX}/non-breaking-fix",
]
