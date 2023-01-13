"""
Pre run script
"""

import sys
from shutil import which

TOOLS = [
    "flutter",
    "dart",
]


def main() -> int:
    """Checks that the environment is correct."""
    print("Checking environment")
    errors = []
    for tool in TOOLS:
        if which(tool) is None:
            errors.append(f"  {tool} not installed")
    if errors:
        error_str = "\n".join(errors)
        raise RuntimeError(f"Environment not correct:\n{error_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
