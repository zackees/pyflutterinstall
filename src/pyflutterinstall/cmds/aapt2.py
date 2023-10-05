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

COMMAND = "aapt2"


def get_aapt2() -> str | None:
    """Gets the aapt path"""
    dirs = [
        os.path.join(paths.BUILD_TOOLS_DIR, d)
        for d in os.listdir(paths.BUILD_TOOLS_DIR)
    ]
    # choose the highest version
    dirs.sort(reverse=True)
    aapt2 = os.path.join(paths.BUILD_TOOLS_DIR, dirs[0], "aapt2")
    if sys.platform == "win32":
        aapt2 += ".exe"
    if not os.path.exists(aapt2):
        return None
    return aapt2


def main(argv: list[str] | None = None) -> int:
    """Main"""
    aapt2 = get_aapt2()
    if aapt2 is None:
        warnings.warn("aapt2 not found")
        return 1
    parent_dir = os.path.dirname(aapt2)
    return trampoline(COMMAND, args=argv, default_path=parent_dir)


if __name__ == "__main__":
    sys.exit(main())
