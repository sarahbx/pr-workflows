import os
import shlex
import subprocess


def upload_to_pypi():
    # for k, v in os.environ.items():
    #     print(f"{k}: {v}")
    # os.environ["INPUT_PYPI_TOKEN"]
    # print(os.environ["GITHUB_REF"])
    # sha = os.environ["GITHUB_SHA"]
    # print(sha)
    # subprocess.check_output(shlex.split(f"git checkout {sha}"))
    # print(subprocess.check_output(shlex.split("cat setup.cfg")))

    tag = os.environ["GITHUB_REF"].split("/")[-1]
    branch = f"branch-{tag}"
    subprocess.check_output(shlex.split(f"git checkout {branch}"))
    print(subprocess.check_output(shlex.split("cat setup.cfg")))
