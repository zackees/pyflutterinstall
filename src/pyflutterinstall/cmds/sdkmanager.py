"""
Command stub for sdkmanager
"""
import os
import sys
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

from pyflutterinstall.cmds.java import find_default_path_or_none

from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()


COMMAND = "sdkmanager"
DEFAULT_PATH = os.path.join(paths.ANDROID_SDK, "cmdline-tools", "latest", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    argv = argv or sys.argv[1:]
    has_sdk_root = False
    for arg in argv:
        if arg.startswith("--sdk_root"):
            has_sdk_root = True
            break
    if not has_sdk_root:
        argv.append(f"--sdk_root={paths.ANDROID_SDK}")
    java_home = find_default_path_or_none()
    assert java_home is not None, "Java home not found"
    os.environ["JAVA_HOME"] = java_home
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
