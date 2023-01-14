"""
Dummy
"""


# disable pylint
# pylint: disable=all


from typing import List
import subprocess
import re


_DEFAULT_PRINT = print
_WINDOWS_PATH_PATTERN = re.compile(r"    PATH    (?P<type>.+)    (?P<value>.+)*")


def _print(message):
    _DEFAULT_PRINT(f"** {message}", flush=True)


def _command(*args, **kwargs):
    _print(f'command: [{" ".join(list(*args))}]')
    return subprocess.run(*args, **kwargs)  # pylint: disable=subprocess-run-check


def _try_decode(
    byte_string: bytes, encodings: List[str] = ["utf-8", "cp949", "ansi"]
) -> str:
    for encoding in encodings:
        try:
            return byte_string.decode(encoding)
        except UnicodeDecodeError:
            continue
    return "Error happened"


def get_env_path() -> str:
    current_path = None
    completed_process = _command(
        ["reg", "query", "HKCU\\Environment", "/v", "PATH"], capture_output=True
    )
    if completed_process.returncode == 0:
        stdout = _try_decode(completed_process.stdout)
        _print(stdout)
        match = _WINDOWS_PATH_PATTERN.search(stdout)
        if match:
            current_path = match.group("value")
            if current_path:
                current_path = current_path.strip().replace("\r", "").replace("\n", "")
                _print(f"current PATH: [{current_path}]")
            else:
                _print("environment variable PATH is empty.")

    elif completed_process.returncode == 1:
        _print("environment variable PATH does not exist.")
        _print(_try_decode(completed_process.stderr))

    else:
        completed_process.check_returncode()
    return str(current_path)
