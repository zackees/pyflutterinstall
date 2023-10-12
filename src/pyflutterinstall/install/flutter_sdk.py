"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil

from shellexecute import execute  # type: ignore

from pyflutterinstall.resources import (
    FLUTTER_GIT_DOWNLOAD,
)  # , ANDROID_SDK, , FLUTTER_HOME
from pyflutterinstall.setenv import add_env_path
from pyflutterinstall.util import make_title

from pyflutterinstall.paths import Paths


def install_flutter_sdk(prompt: bool, install_precache=False) -> int:
    make_title("Installing Flutter")
    paths = Paths()
    paths.apply_env()
    if shutil.which("git") is None:
        error_msg = "'git' not found in path"
        error_msg += "\npath = \n"
        for path in os.environ["PATH"].split(os.path.pathsep):
            error_msg += f"  {path}\n"
        print(error_msg)
        raise FileNotFoundError(error_msg)
    print(f"Install Flutter from {FLUTTER_GIT_DOWNLOAD} to {paths.FLUTTER_HOME}")
    if not paths.FLUTTER_HOME.exists():
        cmd = f'{FLUTTER_GIT_DOWNLOAD} "{paths.FLUTTER_HOME}"'
        execute(cmd, ignore_errors=False)
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
    execute(
        f'flutter config --android-sdk "{paths.ANDROID_SDK}" --no-analytics',
        send_confirmation=[("Accept? (y/n): ", "y")] if not prompt else None,
        ignore_errors=False,
        timeout=60 * 20,
    )
    # If we don't have this then flutter will attempt to use the embedded version
    # of the java jre which will fail.
    execute(
        f"flutter config --android-studio-dir={paths.ANDROID_SDK} --no-analytics",
        send_confirmation=[("Accept? (y/n): ", "y")] if not prompt else None,
        ignore_errors=False,
        timeout=60 * 20,
    )
    confirmation = "y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n"
    send_confirmation = [
        ("Accept? (y/n): ", conf.strip())
        for conf in confirmation.splitlines()
        if conf.strip()
    ]
    if install_precache:
        execute("flutter precache", ignore_errors=True)
    execute(
        "flutter doctor --android-licenses 2>&1",
        send_confirmation=send_confirmation if not prompt else None,
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
