"""
Adds setenv for unix.
"""

# pylint: disable=invalid-name


import os
from pathlib import Path
from typing import Union

SOURCE_FILES = ["~/.bash_profile", "~/.bashrc", "~/.bash_login", "~/.profile"]
FLUTTER_ENV = None

IS_GITHUB_RUNNER = os.getenv("GITHUB_WORKFLOW")

# normalize paths so that ~ is expanded
SOURCE_FILES = [os.path.expanduser(file) for file in SOURCE_FILES]


FLUTTER_ENV = os.path.join(os.getcwd(), "flutter_env.sh")


def get_path_file() -> str:
    """Returns the file that has export PATH."""

    # For my mac environment I'm using bash_aliases
    assert FLUTTER_ENV is not None
    return FLUTTER_ENV


def replace_export(filetarget: str, linematch: str, linereplace: str) -> None:
    """Replaces a line in a file."""
    with open(filetarget, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
    found = False
    for line in lines:
        if line.startswith(linematch):
            lines[lines.index(line)] = linereplace
            found = True
    if not found:
        lines.append(linereplace)
    with open(filetarget, encoding="utf-8", mode="w") as f:
        f.write("\n".join(lines))


def add_path_if_not_exist(filetarget: str, path: str) -> None:
    """Adds a path to the file if it does not exist."""
    with open(filetarget, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
    found = False
    for line in lines:
        if line.startswith("export PATH=") and path in line:
            if path in line:
                found = True
    if not found:
        lines.append(f"export PATH={path}:$PATH")
    with open(filetarget, encoding="utf-8", mode="w") as f:
        f.write("\n".join(lines))


def ensure_hook_installed() -> None:
    """Ensures that the hook is installed."""
    bashrc = os.path.expanduser("~/.bashrc")

    # ensure file file exists
    assert FLUTTER_ENV is not None
    if not os.path.exists(FLUTTER_ENV):
        with open(FLUTTER_ENV, encoding="utf-8", mode="w") as f:
            f.write("#!/bin/bash")
    with open(bashrc, encoding="utf-8", mode="r") as f:
        # rewrite this using open()
        hook_needed = True
        with open(bashrc, encoding="utf-8", mode="r") as f:
            bashrc_text = f.read()
            if ". $FLUTTER_ENV" in bashrc_text:
                hook_needed = False
                print(". $FLUTTER_ENV already exists in ~/.bashrc")
        lines = bashrc_text.splitlines()
        found_env = False
        for i, line in enumerate(lines):
            if line.startswith("set $FLUTTER_ENV="):
                lines[i] = f"set $FLUTTER_ENV={FLUTTER_ENV}"
                found_env = True
        if not found_env:
            lines.append(f"set $FLUTTER_ENV={FLUTTER_ENV}")
        if hook_needed:
            lines.append(". $FLUTTER_ENV")
        with open(bashrc, encoding="utf-8", mode="w") as f:
            f.write("\n".join(lines))


def set_env_var(name: str, value: Union[str, Path]) -> None:
    """Sets an environment variable."""
    value = str(value)
    ensure_hook_installed()
    os.environ[name] = value
    os.system(f"export {name}={value}")
    replace_export(FLUTTER_ENV, f"export {name}=", f"export {name}={value}")
    # write out lines to the .bash_aliases file ensuring that the
    # 'export PATH' line contains a hook back to file_path.


def add_env_path(path: Union[str, Path]) -> None:
    """Adds a path to the PATH environment variable."""
    ensure_hook_installed()
    # export and add to os.environ
    path = str(path)
    add_path_if_not_exist(FLUTTER_ENV, path)
