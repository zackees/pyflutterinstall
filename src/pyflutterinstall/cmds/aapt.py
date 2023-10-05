"""
Command stub for sdkmanager
"""
import os
import sys

from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

from pyflutterinstall.resources import BUILD_TOOLS_DIR

config = config_load()
android_sdk = config.get("ANDROID_SDK", ".")

if android_sdk != ".":
    os.environ["ANDROID_SDK"] = android_sdk
    os.environ["ANDROID_HOME"] = android_sdk

COMMAND = "aapt"

# dataclass


def get_aapt() -> str:
    """Gets the aapt path"""
    # dirs = os.listdir(BUILD_TOOLS_DIR)
    dirs = [os.path.join(BUILD_TOOLS_DIR, d) for d in os.listdir(BUILD_TOOLS_DIR)]
    # choose the highest version
    dirs.sort(reverse=True)
    aapt = os.path.join(BUILD_TOOLS_DIR, dirs[0], "aapt")
    if sys.platform == "win32":
        aapt += ".exe"
    assert os.path.exists(aapt), f"{aapt} does not exist"
    return aapt


def main(argv: list[str] | None = None) -> int:
    """Main"""
    parent_dir = os.path.dirname(get_aapt())
    return trampoline(COMMAND, args=argv, default_path=parent_dir)


if __name__ == "__main__":
    sys.exit(main())
