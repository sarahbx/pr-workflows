import os
import subprocess


def upload_to_pypi():
    os.environ["INPUT_PYPI_TOKEN"]
    subprocess.check_output(["cat", "setup.cfg"])
