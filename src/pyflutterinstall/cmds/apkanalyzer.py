"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.trampoline import trampoline

from pyflutterinstall.config import config_load
from pyflutterinstall.cmds.java import find_default_path_or_none

# from pyflutterinstall.util import print_tree_dir

android_sdk = config_load().get("ANDROID_SDK", ".")
if android_sdk != ".":
    os.environ["ANDROID_SDK"] = android_sdk
    os.environ["ANDROID_HOME"] = android_sdk


COMMAND = "apkanalyzer"
if sys.platform == "win32":
    COMMAND += ".bat"

DEFAULT_PATH = os.path.join(android_sdk, "cmdline-tools", "latest", "bin")

JAVA_DIR = config_load().get("JAVA_DIR", None)



def main(argv: list[str] | None = None) -> int:
    """Main"""
    java_home = find_default_path_or_none()
    os.environ["JAVA_HOME"] = java_home
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
