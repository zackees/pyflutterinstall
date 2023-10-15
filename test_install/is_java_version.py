"""
Pre run script
"""

import subprocess

import argparse
import os
import sys
from shutil import which

from setenvironment import reload_environment

# paths
from pyflutterinstall.paths import Paths


reload_environment()


def get_java_version() -> str:
    """Get java version"""
    try:
        java_version = subprocess.check_output(
            "java -version",
            shell=True,
            universal_newlines=True,
            stderr=subprocess.STDOUT,
        )
        return java_version.strip()
    except subprocess.CalledProcessError:
        return "java not found"


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    Paths().apply_env()
    # Print out the current environment
    # if not macos arm
    parser = argparse.ArgumentParser()
    parser.add_argument("version", type=str, help="java version to check for")
    args = parser.parse_args()
    java_version = get_java_version()
    if args.version not in java_version:
        print(
            f"Java version {args.version} not found\n  instead we got {java_version.strip()}"
        )
        print("Printing environment")
        print(f"which java: {which('java')}")
        env_copy = os.environ.copy()
        paths = env_copy.pop("PATH")
        for key, val in sorted(env_copy.items()):
            print(f"{key} = {val}")
        print("PATH:")
        for path in paths.split(os.pathsep):
            print(f"  {path}")
        return 1
    print(f"Java version {args.version} found at {which('java')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
