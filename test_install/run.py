import os
import sys


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


def main() -> int:
    print_env()
    print("\nstarting pyflutterinstall...")
    rtn = os.system("pyflutterinstall --skip-confirmation --skip-chrome")
    print("\n\n\n")
    print_env()
    return rtn


if __name__ == "__main__":
    sys.exit(main())
