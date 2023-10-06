"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

from pathlib import Path
from typing import Union

import setenvironment  # type: ignore


def uniquify_paths(paths: list[str]) -> list[str]:
    """Removes duplicate paths from the given path string."""
    found = set()
    result = []
    for path in paths:
        if path not in found:
            result.append(path)
            found.add(path)
    return result


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    """Sets an environment variable for the platform."""
    #var_value = str(var_value)
    #if verbose:
    #    print(f"$$$ Setting {var_name} to {var_value}")
    #setenvironment.set_env_var(var_name, var_value)
    pass


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    setenvironment.add_env_path(new_path)


def get_env_path() -> str:
    """Gets the PATH environment variable."""
    return setenvironment.get_env_var("PATH")


def get_env_var(var_name: str) -> str:
    """Gets an environment variable."""
    return setenvironment.get_env_var(var_name)


def unset_env_var(var_name: str) -> str:
    """Unsets an environment variable."""
    return setenvironment.unset_env_var(var_name)

def remove_env_path(path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    setenvironment.remove_env_path(str(path))