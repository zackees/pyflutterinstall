"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement

import os
import subprocess
import signal
import time
from contextlib import contextmanager
from threading import Thread, Event
from tempfile import TemporaryFile
from colorama import just_fix_windows_console  # type: ignore
from pyflutterinstall.resources import (
    INSTALL_DIR,
    DOWNLOAD_DIR,
    ANDROID_SDK,
    FLUTTER_TARGET,
    JAVA_DIR,
)

just_fix_windows_console()  # Fixes color breakages in win32


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


class WatchDogTimer(Thread):
    """Watch dog timer, kills process on hang."""

    def __init__(self, name: str, timeout: int):
        Thread.__init__(self, daemon=True)
        self.timeout = timeout
        self.event = Event()
        self.name = name
        self.start()

    def run(self):
        if not self.event.wait(self.timeout):
            print(f"\n\nTimeout reached while executing {self.name} killing process.")
            time.sleep(10)
            os.kill(os.getpid(), signal.SIGTERM)

    def cancel(self):
        """Cancel the timer"""
        self.event.set()


@contextmanager
def watch_dog_timer(name: str, timeout: int):
    """Watch dog timer"""
    wdt = WatchDogTimer(name=name, timeout=timeout)
    try:
        yield wdt
    finally:
        wdt.cancel()
        wdt.join()


def execute(
    command,
    cwd=None,
    send_confirmation=None,
    ignore_errors=False,
    timeout=60 * 10,
    encoding="utf-8",
) -> int:
    """Execute a command"""
    interactive = not SKIP_CONFIRMATION or not send_confirmation
    print("####################################")
    print(f"Executing\n  {command}")
    if not interactive:
        conf_str = send_confirmation.replace("\n", "\\n")
        print(f'Sending confirmation: "{conf_str}"')
    print("####################################")
    if cwd:
        print(f"  CWD={cwd}")

    with watch_dog_timer(name=command, timeout=timeout):
        with TemporaryFile(encoding="utf-8", mode="a") as stdin_string_stream:
            if send_confirmation:
                stdin_string_stream.write(send_confirmation)
            # temporary buffer for stderr
            with TemporaryFile() as stderr_stream:
                proc = subprocess.Popen(
                    command,
                    cwd=cwd,
                    shell=True,
                    stdin=stdin_string_stream,
                    stderr=stderr_stream,
                    stdout=subprocess.PIPE,
                    encoding=encoding,
                    # 5 MB buffer
                    bufsize=1024 * 1024 * 5,
                    universal_newlines=encoding == "utf-8",
                )
                stdout_stream = proc.stdout
                assert stdout_stream is not None

                def read_one() -> str:
                    # Needed for flutter install on MacOS, othrwise it hangs.
                    char = stdout_stream.read(1)  # type: ignore
                    return char

                for char in iter(read_one, ""):
                    try:
                        print(char, end="")
                    except UnicodeEncodeError as exc:
                        print("UnicodeEncodeError:", exc)
                stderr_stream.seek(0)
                stderr_text = stderr_stream.read().decode("utf-8").strip()
                rtn = proc.returncode
                if rtn != 0 and not ignore_errors:
                    if stderr_text:
                        print(f"stderr:\n{stderr_text}")
                    RuntimeError(f"Command {command} failed with return code {rtn}")
                return rtn


def make_title(title: str) -> None:
    """Make a title"""
    title = f" {title} "
    print("\n\n###########################################")
    print(f"{title.center(43, '#')}")
    print("###########################################\n\n")
