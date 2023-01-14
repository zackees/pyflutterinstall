"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement

import os
import subprocess


from pyflutterinstall.resources import (
    INSTALL_DIR,
    DOWNLOAD_DIR,
    ANDROID_SDK,
    FLUTTER_TARGET,
    JAVA_DIR,
)

SKIP_CONFIRMATION = False


def set_global_skip_confirmation(val: bool) -> None:
    """Set the global skip confirmation flag"""
    global SKIP_CONFIRMATION
    SKIP_CONFIRMATION = val
    print(f"**** Setting SKIP_CONFIRMATION to {SKIP_CONFIRMATION} ****")


def make_dirs() -> None:
    """Make directories for installation"""
    os.makedirs(INSTALL_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(ANDROID_SDK, exist_ok=True)
    os.makedirs(JAVA_DIR, exist_ok=True)

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ
    env[str(ANDROID_SDK)] = str(ANDROID_SDK)
    env[str(JAVA_DIR)] = str(JAVA_DIR)
    # add to path
    # ${FLUTTER_TARGET}/bin
    # add to path
    env["PATH"] = f"{FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
    env["PATH"] = f"{JAVA_DIR}/bin{os.pathsep}{env['PATH']}"


def execute(command, cwd=None, send_confirmation=None, ignore_errors=False) -> int:
    """Execute a command"""
    interactive = not SKIP_CONFIRMATION or not send_confirmation
    print("####################################")
    print(f"Executing\n  {command}")
    if not interactive:
        conf_str = send_confirmation.replace("\n", "\\n")
        print(f"Sending confirmation: {conf_str}")
    print("####################################")
    if cwd:
        print(f"  CWD={cwd}")

    if interactive:
        # return subprocess.check_call(command, cwd=cwd, shell=True, universal_newlines=True)
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            universal_newlines=True,
            encoding="utf-8",
            bufsize=1024 * 1024,
            text=True,
        )
        rtn = proc.wait()
        if not ignore_errors:
            RuntimeError(f"Command {command} failed with return code {rtn}")
        return rtn
    proc = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdin=subprocess.PIPE,
        universal_newlines=True,
        encoding="utf-8",
        # 1MB buffer
        bufsize=1024 * 1024,
        text=True,
    )
    proc.communicate(input=send_confirmation)
    rtn = proc.returncode
    if rtn != 0 and not ignore_errors:
        RuntimeError(f"Command {command} failed with return code {rtn}")
    return rtn


def make_title(title: str) -> None:
    """Make a title"""
    title = f" {title} "
    print("\n\n###########################################")
    print(f"{title.center(43, '#')}")
    print("###########################################\n\n")
