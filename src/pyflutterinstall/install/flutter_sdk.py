"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil
import warnings
import subprocess

from pyflutterinstall.interactive_execute import execute
from pyflutterinstall.print_env import print_env

from pyflutterinstall.resources import (
    FLUTTER_COMMIT,
)  # , ANDROID_SDK, , FLUTTER_HOME
from pyflutterinstall.setenv import add_env_path
from pyflutterinstall.util import make_title

from pyflutterinstall.paths import Paths


def check_cmd_installed(command: str) -> None:
    if shutil.which(command) is None:
        error_msg = f"'{command}' not found in path"
        error_msg += "\npath = \n"
        for path in os.environ["PATH"].split(os.path.pathsep):
            error_msg += f"  {path}\n"
        env_vars = os.environ.copy()
        env_vars.pop("PATH")
        error_msg += "\nENVIRONMENT:\n"
        for key, val in sorted(env_vars.items()):
            error_msg += f"  {key} = {val}\n"
        warnings.warn(error_msg)
        raise FileNotFoundError(error_msg)

from pathlib import Path

def install_flutter_sdk(install_precache=False) -> int:
    make_title("Installing Flutter")
    paths = Paths()
    paths.apply_env()
    check_cmd_installed("git")
    print(f"Install Flutter to {paths.FLUTTER_HOME}")
    flutter_git = paths.FLUTTER_HOME / ".git"
    flutter_dir = str(paths.FLUTTER_HOME.relative_to(Path(".")))
    if not flutter_git.exists():
        cmd_list = [
            "git",
            "clone",
            "https://github.com/flutter/flutter.git",
            "--single-branch",
            f"{flutter_dir}",
            "&&",
            "cd",
            f"{flutter_dir}",
            "&&",
            "git",
            "checkout",
            f"{FLUTTER_COMMIT}",
        ]

        cmd = subprocess.list2cmdline(cmd_list)
        print(f"pyflutter home is {paths.FLUTTER_HOME}")
        print_env()
        execute(cmd, ignore_errors=False, accept_all=False)
    else:
        print(f"Flutter already installed at {paths.FLUTTER_HOME}")
    if not os.path.exists(paths.FLUTTER_HOME):
        print(
            f"!!!!!!!!!!!!! FLUTTER FOLDER {paths.FLUTTER_HOME} DOES NOT EXIST EITHER !!!!!!!!!!!!!!!"
        )
        path = os.environ["PATH"]
        error_msg = f"Could not find {paths.FLUTTER_HOME} in path"
        error_msg += "\npath = \n"
        for path in path.split(os.pathsep):
            error_msg += f"  {path}\n"
        print(error_msg)
        raise FileNotFoundError(error_msg)
    # Add flutter to path
    add_env_path(paths.FLUTTER_HOME_BIN)
    paths.apply_env()
    check_cmd_installed("flutter")
    execute(
        f'flutter config --android-sdk "{paths.ANDROID_SDK}" --no-analytics',
        ignore_errors=False,
        timeout=60 * 20,
    )
    # If we don't have this then flutter will attempt to use the embedded version
    # of the java jre which will fail.
    execute(
        f"flutter config --android-studio-dir={paths.ANDROID_SDK} --no-analytics",
        ignore_errors=False,
        timeout=60 * 20,
    )
    paths.apply_env()
    flutter = shutil.which("flutter")
    if flutter is None:
        raise FileNotFoundError("Could not find flutter in path")

    if install_precache:
        execute("flutter precache", ignore_errors=True)
    execute(
        "flutter doctor --android-licenses 2>&1",
        ignore_errors=False,
        timeout=60 * 20,
    )

    # os.system("echo y | flutter doctor --android-licenses")
    print("Flutter installed.\n")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", action="store_true")
    args = parser.parse_args()
    install_flutter_sdk(not args.prompt)


if __name__ == "__main__":
    main()
