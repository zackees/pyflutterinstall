import os
import sys
import subprocess


def print_env() -> None:
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

import chardet

def main() -> int:
    print_env()
    print("\nstarting pyflutterinstall...")
    env = os.environ.copy()
    env['OutputEncoding'] = 'utf8'
    proc = subprocess.Popen(
        "pyflutterinstall --skip-confirmation --skip-chrome",
        shell=True,
        env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("STDOUT:")
    for line in proc.stdout:
        # Have to use print() in order to get the output to the console in order.
        enc = chardet.detect(line)
        line = line.decode(enc, errors='replace')
        print(line, end="")
    print("STDERR:")
    for line in proc.stderr:
        # Have to use print() in order to get the output to the console in order.
        enc = chardet.detect(line)
        line = line.decode(enc, errors='replace')
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
