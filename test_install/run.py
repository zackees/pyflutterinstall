
import os
import sys

def main() -> int:
    env = os.environ.copy()
    for key in env:
        if key.lower() == "path":
            continue
        print(f"{key}={env[key]}")
    paths = env["PATH"].split(os.pathsep)
    print("paths:")
    for path in paths:
        print(f"  {path}")
    print("\nstarting pyflutterinstall...")
    rtn = os.system("pyflutterinstall --skip-confirmation --skip-chrome")
    return rtn

if __name__ == "__main__":
    sys.exit(main())