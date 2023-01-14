"""
Dummy
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member,consider-using-f-string

import subprocess
import re
import sys
import os
from typing import Optional, Union
from pathlib import Path


_DEFAULT_PRINT = print
_REGISTERLY_VALUE_PATTERN = re.compile(r"    .+    (?P<type>.+)    (?P<value>.+)*")
_ENCODINGS = ["utf-8", "cp949", "ansi"]


def _print(message):
    _DEFAULT_PRINT(f"** {message}", flush=True)


def _command(*args, **kwargs):
    return subprocess.run(*args, **kwargs)  # pylint: disable=subprocess-run-check


def _try_decode(byte_string: bytes) -> str:
    for encoding in _ENCODINGS:
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
    completed_proc: subprocess.CompletedProcess = _command(
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
    if completed_proc.returncode != 0:
        _print(f"Error happened while setting {name}={value}")
        _print(_try_decode(completed_proc.stdout))
    assert value in get_env_var(name), f"Failed to set {name}={value}"  # type: ignore


def get_env_path() -> str:
    path = get_env_var("PATH")
    assert path is not None, "PATH was None, which was unexpected."
    return path


def broadcast_changes():
    print("Broadcasting changes")
    os.system("refreshenv")
    if sys.platform == "win32":
        # os.system("setx /M PATH %PATH%")
        import win32gui  # type: ignore

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        sParam = "Environment"

        res1, res2 = win32gui.SendMessageTimeout(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 10000
        )
        if not res1:
            print("result: %s, %s, from SendMessageTimeout" % (bool(res1), res2))


def parse_paths(path_str: str) -> list[str]:
    path_str = path_str.replace("/", "\\")
    paths = path_str.split(os.path.pathsep)

    def strip_trailing_slash(path: str) -> str:
        """Strips trailing slash."""
        if path.endswith("\\") or path.endswith("/"):
            return path[:-1]
        return path

    paths = [strip_trailing_slash(path) for path in paths]
    return paths


def add_env_path(new_path: Union[Path, str]):
    new_path = str(new_path)
    if sys.platform == "win32":
        new_path = new_path.replace("/", "\\")
    print(f"&&& Adding {new_path} to Windows PATH")
    prev_paths = parse_paths(get_env_path())
    if new_path in prev_paths:
        print(f"{new_path} already in PATH")
        return
    sep = os.path.pathsep
    prev_path_str = sep.join(prev_paths)
    set_env_var("PATH", f"{str(new_path)}{sep}{prev_path_str}", verbose=False)


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    var_name = str(var_name)
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    set_env_var_cmd(var_name, var_value)
    os.environ[var_name] = var_value


def main():
    set_env_var_cmd("FOO", "BAR")
    print(get_env_var("FOO"))
    # print(get_env_var("ANDROID_HOME"))


if __name__ == "__main__":
    main()