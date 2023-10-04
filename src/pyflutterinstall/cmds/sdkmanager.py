"""
Command stub for sdkmanager
"""
import os
import sys
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load
import shutil

ANDROID_SDK = config_load().get("ANDROID_SDK", ".")
if ANDROID_SDK != ".":
    os.environ["ANDROID_SDK"] = ANDROID_SDK
    os.environ["ANDROID_HOME"] = ANDROID_SDK

COMMAND = "sdkmanager"
DEFAULT_PATH = os.path.join(ANDROID_SDK, "cmdline-tools", "latest", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    argv = argv or sys.argv[1:]
    has_sdk_root = False
    for arg in argv:
        if arg.startswith("--sdk_root"):
            has_sdk_root = True
            break
    if not has_sdk_root:
        argv.append(f"--sdk_root={ANDROID_SDK}")
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
