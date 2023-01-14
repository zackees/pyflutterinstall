"""
Pre run script
"""

# pylint: disable=R0801

import os
import sys
from shutil import which

from colorama import just_fix_windows_console  # type: ignore

from pyflutterinstall.mywin32 import get_env_var


def update_env(names: list[str]) -> None:
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
    update_env(["PATH", "ANDROID_SDK_ROOT", "ANDROID_HOME", "JAVA_HOME"])
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

    needle = os.path.join('cmdline-tools', 'latest', 'bin')
    found = False
    for path in os.environ["PATH"].split(os.pathsep):
        if needle in path:
            found = True
            break
    if not found:
        raise RuntimeError("Android tools not found in PATH")

    if not which("flutter"):
        raise RuntimeError("Flutter not installed, are the paths ok?")
    os.system("flutter doctor -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
