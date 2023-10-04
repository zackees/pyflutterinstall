"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.config import config_load
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.util import print_tree_dir

JAVA_DIR = config_load().get("JAVA_DIR", None)

COMMAND = "java"


def find_default_path_or_none() -> str | None:
    """Find default path"""
    if JAVA_DIR is None:
        return None
    jdk_folders = os.listdir(JAVA_DIR)
    if not jdk_folders:
        return None
    if len(jdk_folders) > 1:
        jdk_folders.sort()
        jdk_folders.reverse()
    print(f"jdk_folders: {jdk_folders}")
    base_java_dir = os.path.join(JAVA_DIR, jdk_folders[0])
    if sys.platform == "darwin":
        java_bin = os.path.join(base_java_dir, "Contents", "Home", "bin")
    else:
        java_bin = os.path.join(base_java_dir, "bin")
    return java_bin


def main(argv: list[str] | None = None) -> int:
    """Main"""
    print(f"Java dir: {JAVA_DIR}")
    print(os.listdir(JAVA_DIR))
    print_tree_dir(JAVA_DIR, max_level=5)

    rtn = trampoline(COMMAND, args=argv, default_path=find_default_path_or_none())
    return rtn


if __name__ == "__main__":
    sys.exit(main())
