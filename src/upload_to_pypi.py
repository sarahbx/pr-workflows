import os
import shlex
import subprocess

import pygit2


def upload_to_pypi():
    tag = os.environ["GITHUB_REF"].split("/")[-1]
    repo = pygit2.Repository(".git")
    repo.checkout(f"refs/remotes/origin/branch-{tag}")
    print(subprocess.check_output(shlex.split("cat setup.cfg")))

    # for k, v in os.environ.items():
    #     print(f"{k}: {v}")
    # os.environ["INPUT_PYPI_TOKEN"]
    # print(os.environ["GITHUB_REF"])
    # sha = os.environ["GITHUB_SHA"]
    # print(sha)
    # subprocess.check_output(shlex.split(f"git checkout {sha}"))
    # print(subprocess.check_output(shlex.split("cat setup.cfg")))

    # branch = f"branch-{tag}"
    # subprocess.check_output(shlex.split(f"git checkout origin/{branch}"))
    # print(subprocess.check_output(shlex.split("cat setup.cfg")))
