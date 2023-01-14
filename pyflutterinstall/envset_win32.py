"""
Allows setting environment variables and the path.
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member,consider-using-f-string

import sys
import os
from pathlib import Path
from typing import Union


def gen_powershell_script_set_env(var_name: str, var_value: str):
    cmd = f"""[Environment]::SetEnvironmentVariable('{var_name}', '{var_value}','User');"""
    return cmd


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


def add_system_path(new_path: Union[Path, str]):
    new_path = str(new_path)
    if sys.platform == "win32":
        new_path = new_path.replace("/", "\\")
    print(f"Adding {new_path} to Windows PATH")
    old_path = os.environ["PATH"]
    if new_path in old_path:
        print(f"{new_path} already in PATH")
        return
    sep = os.path.pathsep
    set_env_var("PATH", f"{str(new_path)}{sep}{old_path}", verbose=False)


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    var_name = str(var_name)
    var_value = str(var_value)
    if verbose:
        print(f"Setting {var_name} to {var_value}")
    cmd = gen_powershell_script_set_env(var_name, var_value)
    cmd = 'powershell.exe -Command "& {' + cmd + '}"'
    os.system(cmd)
    os.environ[var_name] = var_value
