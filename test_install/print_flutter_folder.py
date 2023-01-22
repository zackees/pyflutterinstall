"""
Print all files from FlutterSDK folder.
"""

import os
import sys

FLUTTER_SDK = "FlutterSDK"
MAX_DEPTH = 4


def main() -> int:
    """Main function."""
    # print all files from flutter did
    print(f"Printing files from {FLUTTER_SDK}")
    for root, _, files in os.walk(FLUTTER_SDK):
        depth = root[len(FLUTTER_SDK) + 1:].count(os.sep)
        if depth >= MAX_DEPTH:
            continue
        for file in files:
            print(os.path.join(root, file))
    return 0


if __name__ == "__main__":
    sys.exit(main())
