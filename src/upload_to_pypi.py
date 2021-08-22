import os
import shlex
import subprocess
import sys

import pygit2


def upload_to_pypi():
    os.environ["TWINE_USERNAME"] = "__token__"
    os.environ["TWINE_PASSWORD"] = os.environ["INPUT_PYPI_TOKEN"]
    tag = os.environ["GITHUB_REF"].split("/")[-1]
    version = tag.strip("v")
    dist_pkg = [pkg for pkg in os.listdir("dist") if version in pkg]
    if not dist_pkg:
        print("No package to upload under dist/ folder")
        sys.exit(1)

    dist_pkg = dist_pkg[0]
    if version not in dist_pkg:
        print(f"Package {dist_pkg} not match version {tag}")
        sys.exit(1)

    repo = pygit2.Repository(".")
    repo.checkout(f"refs/remotes/origin/branch-{tag}")
    subprocess.check_output(shlex.split(f"twine check dist/{dist_pkg}"))
    subprocess.check_output(
        shlex.split(f"twine upload dist/{dist_pkg} --skip-existing")
    )
