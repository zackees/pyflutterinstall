"""
Command stub for sdkmanager
"""
import os
import sys
import warnings
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()

COMMAND = "aapt"


def get_aapt() -> str | None:
    """Gets the aapt path"""
    # dirs = os.listdir(BUILD_TOOLS_DIR)
    print(f"BUILD_TOOLS_DIR: {paths.BUILD_TOOLS_DIR}")
    dirs = [
        os.path.join(paths.BUILD_TOOLS_DIR, d)
        for d in os.listdir(paths.BUILD_TOOLS_DIR)
    ]
    # choose the highest version
    dirs.sort(reverse=True)
    aapt = os.path.join(paths.BUILD_TOOLS_DIR, dirs[0], "aapt")
    if sys.platform == "win32":
        aapt += ".exe"
    if not os.path.exists(aapt):
        return None
    return aapt


def main(argv: list[str] | None = None) -> int:
    """Main"""
    aapt = get_aapt()
    if aapt is None:
        warnings.warn("aapt not found")
        return 1
    parent_dir = os.path.dirname(aapt)
    # print(f"parent_dir: {parent_dir}")
    return trampoline(COMMAND, args=argv, default_path=parent_dir)


if __name__ == "__main__":
    os.chdir("FlutterSDK")
    sys.exit(main())
