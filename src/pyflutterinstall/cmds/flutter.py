"""
Command stub for flutter
"""
import sys

from pyflutterinstall.trampoline import trampoline

from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()

COMMAND = "flutter"


def main(argv: list[str] | None = None) -> int:
    """Main"""
    bin_path = paths.FLUTTER_HOME_BIN.resolve()
    return trampoline(COMMAND, args=argv, default_path=bin_path)


if __name__ == "__main__":
    sys.exit(main())
