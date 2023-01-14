"""
Pre run script
"""

# pylint: disable=R0801

import os
import sys
from shutil import which
# import win32api

from colorama import just_fix_windows_console  # type: ignore

from pyflutterinstall.mywin32 import get_env_path

def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    just_fix_windows_console()  # Fixes color breakages
    #current_path = win32api.GetEnvironmentVariable("PATH")
    current_path = get_env_path()
    os.environ.update({"PATH": current_path})
    # Print out the current environment
    print("Environment:")
    for key, value in os.environ.items():
        # skip path
        if key == "PATH":
            continue
        print(f"  {key} = {value}")
    print("PATH:")
    for path in os.environ["PATH"].split(os.pathsep):
        print(f"  {path}")

    if not which("flutter"):
        raise RuntimeError("Flutter not installed, are the paths ok?")
    os.system("flutter doctor -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
