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


def print_tree_dir(path: str) -> None:
    """Prints the tree of a directory"""
    output = ""
    for root, _, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = " " * 4 * (level)
        output += f"{indent}{os.path.basename(root)}" + os.linesep
        subindent = " " * 4 * (level + 1)
        for f in files:
            output += f"{subindent}{f}" + os.linesep
    print(output)


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    just_fix_windows_console()  # Fixes color breakages
    print("ANDROID_HOME = " + os.environ["ANDROID_HOME"])
    print(f"dir $ANDROID_HOME = {os.listdir(os.environ['ANDROID_HOME'])}")
    print_tree_dir(os.environ["ANDROID_HOME"])
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
