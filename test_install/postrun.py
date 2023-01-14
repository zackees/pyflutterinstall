"""
Pre run script
"""

# pylint: disable=R0801

import os
import sys


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
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
    print("Checking environment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
