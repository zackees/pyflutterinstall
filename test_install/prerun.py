"""
Pre run script
"""

import os
import sys
from shutil import which
from pyflutterinstall.util import print_tree_dir

TOOLS = [
    "flutter",
    "dart",
]


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    # Print out the current environment
    print("ANDROID_HOME = " + os.environ["ANDROID_HOME"])
    print(f"dir $ANDROID_HOME = {os.listdir(os.environ['ANDROID_HOME'])}")
    print_tree_dir(os.environ["ANDROID_HOME"])
    print("Environment:")
    for key, value in os.environ.items():
        # skip path
        if key == "PATH":
            continue
        print(f"  {key} = {value}")
    print("PATH:")
    for path in os.environ["PATH"].split(os.pathsep):
        print(f"  {path}")
    print("Checking environment")
    errors = []
    for tool in TOOLS:
        if which(tool):
            errors.append(f"  {tool} not installed")
    if errors:
        error_str = "\n".join(errors)
        raise RuntimeError(f"Environment not correct:\n{error_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
