"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement,too-many-arguments,too-many-locals,fixme,too-many-statements,chained-comparison

import subprocess
import sys
from typing import Optional
import pexpect  # type: ignore
from colorama import just_fix_windows_console  # type: ignore

from pyflutterinstall.outstream import Outstream

just_fix_windows_console()  # Fixes color breakages in win32


def execute(
    command,
    cwd=None,
    send_confirmation: Optional[list[tuple[str, str]]] = None,
    ignore_errors=False,
    timeout=60 * 10,
    encoding="utf-8",
) -> int:
    """Execute a command"""
    print("####################################")
    print(f"Executing\n  {command}")
    print("####################################")
    if cwd:
        print(f"  CWD={cwd}")

    if send_confirmation is None:
        completed_process = subprocess.run(
            command, cwd=cwd, shell=True, check=not ignore_errors,
            timeout=timeout, encoding=encoding,
        )
        return completed_process.returncode
    # temporary buffer for stderr
    outstream = Outstream
    child = pexpect.spawn(
        command,
        cwd=cwd,
        encoding=encoding,
        timeout=timeout,
        logfile=outstream,
    )
    child.logfile = sys.stdout
    for expect, answer in send_confirmation:
        which = child.expect_exact([expect, pexpect.EOF], timeout=timeout)
        if which == 1:
            break  # EOF
        child.sendline(answer)
    child.expect(pexpect.EOF)
    child.close()

    if child.exitstatus != 0 and not ignore_errors:
        raise RuntimeError("Command failed: " + command)
    return child.exitstatus
