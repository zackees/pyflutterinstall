"""
Pre run script
"""

# pylint: disable=R0801,invalid-name

import os
import sys
from shutil import which

from colorama import just_fix_windows_console  # type: ignore

from pyflutterinstall.setenv import get_env_var, init_dotenv

init_dotenv()


def update_env_win32(names: list[str]) -> None:
    """Updates the environment with the given name."""
    for name in names:
        value = get_env_var(name)
        if value:
            os.environ.update({name: value})
        else:
            print(f"Warning: {name} not found")
            cmd = f"reg query HKCU\\Environment /v {name}"
            print(f"Searching reg environment to it (dbg) with {cmd}")
            os.system(f"reg query HKCU\\Environment /v {name}")


def main() -> int:
    """Checks the environment and other tools are correct before run is invoked."""
    just_fix_windows_console()  # Fixes color breakages
    # Get the environment and slurp them in. Note that this is necessary
    # because the previously run subprocesses will have modified the
    # user environment but the parent process will not have seen these
    # so it's necessary to update the environment in this child process.
    if sys.platform == "win32":
        update_env_win32(["PATH", "ANDROID_SDK_ROOT", "ANDROID_HOME", "JAVA_HOME"])
    # Print out the current environment
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
