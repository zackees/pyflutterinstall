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
    argv = argv or []
    if "--sdk_root" not in argv:
        argv.append("--sdk_root")
        argv.append(ANDROID_SDK)
    java_path = shutil.which("java")
    version = os.popen(f"{java_path} -version").read()
    print(f"java version: {version}")
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
