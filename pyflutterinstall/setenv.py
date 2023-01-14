"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

import sys
from typing import Union
from pathlib import Path


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    """Sets an environment variable for the platform."""
    if sys.platform == "win32":
        from pyflutterinstall.setenv_win32 import set_env_var as win32_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        if verbose:
            print(f"$$$ Setting {var_name} to {var_value}")
        win32_set_env_var(var_name, var_value)
    else:
        raise NotImplementedError("set_env_var not implemented for this platform")


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    if sys.platform == "win32":
        from pyflutterinstall.setenv_win32 import add_env_path as win32_add_env_path

        win32_add_env_path(new_path)
    else:
        raise NotImplementedError("add_env_path not implemented for this platform")
