"""
Allows setting environment variables and the path.
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member

import os
from pathlib import Path
from typing import Union


def gen_powershell_script_set_env(var_name: str, var_value: str):
    cmd = f"""[Environment]::SetEnvironmentVariable('{var_name}', '{var_value}','User');"""
    return cmd


def add_system_path(new_path: Path):
    print(f"Adding {new_path} to Windows PATH")
    old_path = os.environ["PATH"]
    if str(new_path) in old_path:
        print(f"{new_path} already in PATH")
        return
    set_env_var("PATH", f"{str(new_path)};{old_path}", verbose=False)


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    assert var_name.lower() != "path", "Use add_system_path instead"
    var_name = str(var_name)
    var_value = str(var_value)
    if verbose:
        print(f"Setting {var_name} to {var_value}")
    cmd = gen_powershell_script_set_env(var_name, var_value)
    cmd = 'powershell.exe -Command "& {' + cmd + '}"'
    os.system(cmd)
    os.environ[var_name] = var_value
