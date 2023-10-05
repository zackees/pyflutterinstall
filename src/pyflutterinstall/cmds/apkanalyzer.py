"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.trampoline import trampoline

from pyflutterinstall.config import config_load
from pyflutterinstall.cmds.java import find_default_path_or_none

# from pyflutterinstall.util import print_tree_dir

from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()

COMMAND = "apkanalyzer"
if sys.platform == "win32":
    COMMAND += ".bat"

DEFAULT_PATH = os.path.join(paths.ANDROID_SDK, "cmdline-tools", "latest", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    java_home = find_default_path_or_none()
    if java_home is None:
        raise RuntimeError("Java home not found")
    os.environ["JAVA_HOME"] = java_home
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
