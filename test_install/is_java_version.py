"""
Pre run script
"""

import subprocess

import argparse
import os
import sys
from shutil import which
from pyflutterinstall.util import print_tree_dir



def get_java_version() -> str:
    """Get java version"""
    java_version = subprocess.check_output(
        "java -version",
        shell=True,
        universal_newlines=True,
        stderr=subprocess.STDOUT,
    )
    return java_version.strip()

def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    # Print out the current environment
    # if not macos arm
    parser = argparse.ArgumentParser()
    parser.add_argument("version", type=str, help="java version to check for")
    args = parser.parse_args()
    java_version = get_java_version()
    print(f"Java version: {java_version}")
    if args.version not in java_version:
        print(f"Java version {args.version} not found")
        return 1
    return 0
    


if __name__ == "__main__":
    sys.exit(main())
