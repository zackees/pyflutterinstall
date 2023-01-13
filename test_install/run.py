"""
Runs an installation routine.
"""

import os
import sys
import subprocess
from ftfy import fix_text


def print_env() -> None:
    """Prints the environment variables."""
    env = os.environ.copy()
    print("env:")
    for key in env:
        if key.lower() == "path":
            continue
        print(f"  {key}={env[key]}")
    paths = env["PATH"].split(os.pathsep)
    print("paths:")
    for path in paths:
        print(f"  {path}")


def main() -> int:
    """Runs the installation routine."""
    os.makedirs("install_dir", exist_ok=True)
    os.chdir("install_dir")
    print_env()
    print("\nstarting pyflutterinstall...")
    env = os.environ.copy()
    env["OutputEncoding"] = "utf8"
    proc = subprocess.Popen(  # pylint: disable=consider-using-with
        "pyflutterinstall --skip-confirmation --skip-chrome",
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding="utf-8",
        # large 1 MB buffer size to avoid blocking
        bufsize=1024 * 1024,
    )
    stdout = proc.stdout
    assert stdout is not None
    stderr = proc.stderr
    assert stderr is not None

    stdout_iter = iter(stdout.readline, "")
    stderr_iter = iter(stderr.readline, "")
    print("STDOUT:")
    while True:
        try:
            line = next(stdout_iter)
            line = fix_text(line)
            print(line, end="")
        except StopIteration:
            break
        except UnicodeDecodeError as err:
            print(f"UnicodeDecodeError: {err}")
            continue
    print("STDERR:")
    while True:
        try:
            line = next(stderr_iter)
            line = fix_text(line)
            print(line, end="")
        except StopIteration:
            break
        except UnicodeDecodeError as err:
            print(f"UnicodeDecodeError: {err}")
            continue
    rtn = proc.wait()
    print("\n\n\n")
    print_env()
    if rtn != 0:
        print(f"pyflutterinstall failed with return code {rtn}")
        raise RuntimeError("pyflutterinstall failed")
    return rtn


if __name__ == "__main__":
    sys.exit(main())
