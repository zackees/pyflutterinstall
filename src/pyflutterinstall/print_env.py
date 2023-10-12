"""
Prints the environment. Runnable module.
python -m pyflutterinstall.print_env
"""

import os


def print_env() -> None:
    """Prints the environment, sorted environmlental variables then paths"""
    env_copy = os.environ.copy()
    paths = env_copy.pop("PATH")
    for key, val in sorted(env_copy.items()):
        print(f"{key} = {val}")
    print("PATH:")
    for path in paths.split(os.pathsep):
        print(f"  {path}")
    print("")

if __name__ == "__main__":
    print_env()