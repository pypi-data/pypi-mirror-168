import os
import re
import subprocess
from typing import List


def re_replace(text: str, pattern: str, replace_with: str) -> str:
    matches = list(re.compile(pattern, flags=re.UNICODE).finditer(text))
    matches.reverse()
    for m in matches:
        (start, end) = get_replace_span(m)
        text = text[:start] + replace_with + text[end:]

    return text


def get_replace_span(match):
    try:
        return match.span("replace")
    except IndexError:
        return match.span()


def get_filename_without_extension(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def call(command: List[str], verbose: bool):
    if not verbose:
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else: return subprocess.call(command)
