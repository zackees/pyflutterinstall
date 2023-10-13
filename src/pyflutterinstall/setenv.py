"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

import sys
from pathlib import Path
from typing import Union

from setenvironment import setenv

if sys.platform != "win32":
    from setenvironment import setenv_unix

    # Note that github runners are forced to use the ~/.bashrc file
    setenv_unix.set_env_config_file("~/.bashrc")


from pyflutterinstall.config import (  # pylint: disable=wrong-import-position
    config_load,
    config_save,
)

PATH_KEY = "FlutterSKDPATH"


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
    config.vars[var_name] = var_value
    config_save(config)
    setenv.set_env_var(var_name=var_name, var_value=var_value)


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    config = config_load()
    # path_list = config.setdefault("PATH", [])
    # config["PATH"] = uniquify_paths([str(new_path)] + path_list)
    config.paths.insert(0, str(new_path))
    config_save(config)
    # setenv.add_env_path(new_path)
    setenv.add_template_path(env_var=PATH_KEY, new_path=new_path)


def get_env_path() -> str:
    """Gets the PATH environment variable."""
    return setenv.get_env_var(var_name=PATH_KEY)


def get_env_var(var_name: str) -> str:
    """Gets an environment variable."""
    return setenv.get_env_var(var_name=var_name)


def unset_env_var(var_name: str) -> str:
    """Unsets an environment variable."""
    config = config_load()
    config.vars.pop(var_name, None)
    config_save(config)
    return setenv.unset_env_var(var_name=var_name)


def remove_env_path(path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    config = config_load()
    path = str(path)
    # paths = config.setdefault("PATH", [])
    while path in config.paths:
        config.paths.remove(path)
    config_save(config)
    setenv.remove_template_path(env_var=PATH_KEY, path=path, remove_if_empty=True)


def remove_all_paths() -> None:
    """Removes all paths from the PATH environment variable."""
    setenv.remove_template_group(env_var=PATH_KEY)
