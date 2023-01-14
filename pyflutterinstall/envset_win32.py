"""
Allows setting environment variables and the path.
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member,consider-using-f-string

import sys
import os
from pathlib import Path
from typing import Union

from pyflutterinstall.mywin32 import set_env_var_cmd, get_env_path


def set_env_powershell(var_name: str, var_value: str):
    print(f"$$$ Generating a set env script for {var_name} to {var_value}")
    cmd = f"""[Environment]::SetEnvironmentVariable('{var_name}', '{var_value}','User');"""
    cmd = 'powershell.exe -Command "& {' + cmd + '}"'
    os.system(cmd)


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
    if sys.platform == "win32":
        path_str = path_str.replace("/", "\\")
    else:
        path_str = path_str.replace("\\", "/")
    paths = path_str.split(os.path.pathsep)

    def strip_trailing_slash(path: str) -> str:
        """Strips trailing slash."""
        if path.endswith("\\") or path.endswith("/"):
            return path[:-1]
        return path

    paths = [strip_trailing_slash(path) for path in paths]
    return paths


def add_system_path(new_path: Union[Path, str]):
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
