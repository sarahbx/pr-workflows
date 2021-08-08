import os
import re
import sys

import requests


def block_offensive_lanague(pull):
    offensive_words_match = False
    offensive_words = re.compile("black[ -]?list|white[ -]?list|master|slave")

    for _file in pull.get_files():
        print(os.listdir())
        file_name = _file.filename
        # Exclude current file from check
        if __file__.split("/")[-1] == file_name.split("/")[-1]:
            continue

        for idx, line in enumerate(requests.get(_file.raw_url).text.splitlines()):
            match = re.search(offensive_words, line)
            if match:
                print(
                    f"File: {file_name}:{idx + 1}:{match.span()[0]}\n    "
                    f"Found offensive words [{match.group()}]"
                )
                offensive_words_match = True

    if offensive_words_match:
        sys.exit(1)
