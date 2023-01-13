"""
Runs an installation routine.
"""

import os
import sys
import subprocess


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
    )
    stdout = proc.stdout
    assert stdout is not None
    stderr = proc.stderr
    assert stderr is not None
    print("STDOUT:")

    for line in iter(stdout.readline, ""):
        # Have to use print() in order to get the output to the console in order.
        print(line, end="")
    print("STDERR:")
    for line in iter(stderr.readline, ""):
        # Have to use print() in order to get the output to the console in order.
        print(line, end="")
    rtn = proc.wait()
    print("\n\n\n")
    print_env()
    if rtn != 0:
        print(f"pyflutterinstall failed with return code {rtn}")
        raise RuntimeError("pyflutterinstall failed")
    return rtn


if __name__ == "__main__":
    sys.exit(main())
