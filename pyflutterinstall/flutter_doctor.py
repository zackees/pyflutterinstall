"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import shutil
import subprocess

from pyflutterinstall.util import (
    make_title,
)


def postinstall_run_flutter_doctor() -> None:
    cmd = "flutter doctor -v"
    make_title(f"Executing '{cmd}'")
    if not shutil.which("flutter"):
        print("Flutter not found in path")
        return
    subprocess.call(cmd, shell=True, text=True, universal_newlines=True)
