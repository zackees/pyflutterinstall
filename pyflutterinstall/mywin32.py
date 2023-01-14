"""
Dummy
"""


# disable pylint
# pylint: disable=all


from typing import List, Optional
import subprocess
import re


_DEFAULT_PRINT = print
_REGISTERLY_VALUE_PATTERN = re.compile(r"    .+    (?P<type>.+)    (?P<value>.+)*")


def _print(message):
    _DEFAULT_PRINT(f"** {message}", flush=True)


def _command(*args, **kwargs):
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


def get_env_var(name: str) -> Optional[str]:
    current_path = None
    completed_process = _command(
        ["reg", "query", "HKCU\\Environment", "/v", name], capture_output=True
    )
    if completed_process.returncode == 0:
        stdout = _try_decode(completed_process.stdout)
        match = _REGISTERLY_VALUE_PATTERN.search(stdout)
        if match:
            current_path = match.group("value")
            if current_path:
                current_path = current_path.strip().replace("\r", "").replace("\n", "")

    elif completed_process.returncode == 1:
        _print("environment variable PATH does not exist.")
        _print(_try_decode(completed_process.stderr))
        raise OSError("environment variable PATH does not exist.")
    return current_path


def set_env_var_cmd(name: str, value: str) -> None:
    _command(
        [
            "reg",
            "add",
            "HKCU\\Environment",
            "/t",
            "REG_SZ",
            "/v",
            name,
            "/d",
            value,
            "/f",
        ]
    )


def get_env_path() -> str:
    path = get_env_var("PATH")
    assert path is not None, "PATH was None, which was unexpected."
    return path


def main():
    set_env_var_cmd("FOO", "BAR")
    print(get_env_var("FOO"))
    # print(get_env_var("ANDROID_HOME"))


if __name__ == "__main__":
    main()
