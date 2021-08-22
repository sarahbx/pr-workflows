import os
import shlex
import subprocess


def upload_to_pypi():
    os.environ["INPUT_PYPI_TOKEN"]
    sha = os.environ["GITHUB_SHA"]
    subprocess.check_output(shlex.split(f"git checkout {sha}"))
    print(subprocess.check_output(shlex.split("cat setup.cfg")))
