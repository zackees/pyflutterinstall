"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

from pathlib import Path
from typing import Union

import setenvironment  # type: ignore

from pyflutterinstall.config import config_load, config_save


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
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    config = config_load()
    env = config.setdefault("ENV", {})
    env[var_name] = var_value
    config_save(config)
    setenvironment.set_env_var(var_name, var_value)


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    config = config_load()
    path_list = config.setdefault("PATH", [])
    config["PATH"] = uniquify_paths([str(new_path)] + path_list)
    config_save(config)
    setenvironment.add_env_path(new_path)


def get_env_path() -> str:
    """Gets the PATH environment variable."""
    return setenvironment.get_env_var("PATH")


def get_env_var(var_name: str) -> str:
    """Gets an environment variable."""
    return setenvironment.get_env_var(var_name)


def unset_env_var(var_name: str) -> str:
    """Unsets an environment variable."""
    config = config_load()
    config.setdefault("ENV", {}).pop(var_name, None)
    config_save(config)
    return setenvironment.unset_env_var(var_name)


def remove_env_path(path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    config = config_load()
    path = str(path)
    # paths = config["PATH"]
    paths = config.setdefault("PATH", [])
    while path in paths:
        paths.remove(path)
    config["PATH"] = paths
    config_save(config)
    setenvironment.remove_env_path(path)
