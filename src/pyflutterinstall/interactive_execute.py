"""
Trampoline to shellexecute.execute
"""

import os
import subprocess
import sys

# from typing import Optional

# import shellexecute

# execute = shellexecute.execute

HERE = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.join(HERE, "install")
WIN_DIR = os.path.join(INSTALL_DIR, "win")


def get_yes_cmd() -> str:
    """Get's the yes command for the platform"""
    if sys.platform == "win32":
        return os.path.join(WIN_DIR, "yes.exe")
    return "yes"


def execute(
    command,
    cwd=None,
    ignore_errors=False,
    timeout=None,
) -> int:
    """Executes commands and pipes the command "yes" to it."""
    out = ""
    out += "####################################\n"
    out += f"Executing\n  {command}\n"
    if cwd:
        out += f"  CWD={cwd}\n"
    out += "####################################\n"

    sys.stdout.write(out)
    sys.stdout.flush()
    yes = get_yes_cmd()
    command = f'"{yes}" | {command}'

    rtn = subprocess.call(
        command,
        shell=True,
        cwd=cwd,
        timeout=timeout,
        universal_newlines=True,
    )
    if rtn != 0 and not ignore_errors:
        raise RuntimeError("Command failed: " + command)
    return rtn
