"""
Pre run script
"""

# pylint: disable=R0801,invalid-name

import os
import sys
from shutil import which

from colorama import just_fix_windows_console  # type: ignore

from pyflutterinstall.setenv import init_dotenv

init_dotenv()


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    just_fix_windows_console()  # Fixes color breakages
    print("Environment:")
    for key, value in os.environ.items():
        # skip path
        if key == "PATH":
            continue
        print(f"  {key} = {value}")
    print("PATH:")
    for path in os.environ["PATH"].split(os.pathsep):
        print(f"  {path}")

    if sys.platform != "win32":
        print("Printing ~/.bashrc file")
        bashrc = os.path.expanduser("~/.bashrc")
        assert os.path.exists(bashrc)
        with open(bashrc, encoding="utf-8", mode="r") as f:
            print(f.read())

    needle = os.path.join("cmdline-tools", "latest", "bin")
    found = False
    for path in os.environ["PATH"].split(os.pathsep):
        if needle in path:
            found = True
            break
    if not found:
        raise RuntimeError(f'Android tools "{needle} not found in PATH')

    print("Checking if Flutter is in path")
    if not which("flutter"):
        print("Flutter not found in path")
        return 1
    rtn = os.system("java -version")
    if rtn != 0:
        print("Java not found in path")
        return 1
    os.system("flutter doctor -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
