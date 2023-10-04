"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.trampoline import trampoline

from pyflutterinstall.config import config_load

android_sdk = config_load().get("ANDROID_SDK", ".")
if android_sdk != ".":
    os.environ["ANDROID_SDK"] = android_sdk
    os.environ["ANDROID_HOME"] = android_sdk


COMMAND = "apkanalyzer"
DEFAULT_PATH = os.path.join(
    android_sdk, "cmdline-tools", "tools", "cmdline-tools", "bin"
)
LATEST_PATH = os.path.join(android_sdk, "cmdline-tools", "latest", "bin")

BINARY_PATHS = [
    DEFAULT_PATH,
    LATEST_PATH,
]


def find_path() -> str:
    """Find path"""
    for path in BINARY_PATHS:
        final_path = os.path.join(path, COMMAND)
        if sys.platform == "win32":
            final_path += ".bat"
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"Could not find {COMMAND} on any of the paths: {BINARY_PATHS}"
    )


def main(argv: list[str] | None = None) -> int:
    """Main"""
    default_path = find_path()
    return trampoline(COMMAND, args=argv, default_path=default_path)


if __name__ == "__main__":
    sys.exit(main())
