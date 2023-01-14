"""
Allows setting environment variables and the path.
"""

# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member

import sys
import os
from pathlib import Path


def gen_powershell_script(path: Path):
    old_path = os.environ["PATH"]
    new_path = f"{str(path)};{old_path}"
    cmd = f"""[Environment]::SetEnvironmentVariable('PATH', '{new_path}','User');"""
    return cmd

def add_system_path(new_path: Path):
    if sys.platform == "win32":
        print(f"Adding {new_path} to Windows PATH")
        cmd = gen_powershell_script(new_path)
        os.system(cmd)
        os.environ["PATH"] += os.pathsep + str(new_path)
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")


def set_env_var(var_name, var_value):
    assert var_name.lower() != "path", "Use add_system_path instead"
    var_name = str(var_name)
    var_value = str(var_value)
    if sys.platform == "win32":
        os.system(f'setx {var_name} "{var_value}"')
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")
