"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement,too-many-arguments,too-many-locals,fixme,too-many-statements,chained-comparison

import os
import sys
import shutil


def make_title(title: str) -> None:
    """Make a title"""
    title = f" {title} "
    out = ""
    out += "\n\n###########################################\n"
    out += f"{title.center(43, '#')}\n"
    out += "###########################################\n\n\n"
    sys.stdout.write(out)
    sys.stdout.flush()


def print_tree_dir(path: str, max_level=2, only_exe=False) -> None:
    """Prints the tree of a directory"""
    output = ""
    for root, dirs, files in os.walk(path):
        level = str(root).replace(path, "").count(os.sep)
        indent = " " * 4 * (level)
        if max_level > 0 and (level + 1) > max_level:
            del dirs[:]
            continue
        output += f"{indent}{os.path.basename(root)}" + os.linesep
        subindent = " " * 4 * (level + 1)
        for file in files:
            if only_exe:
                if sys.platform == "win32":
                    if not file.endswith(".exe") and not file.endswith(".bat"):
                        continue
                    output += f"{subindent}{file}" + os.linesep
                else:
                    if not os.access(os.path.join(root, file), os.X_OK):
                        continue
                    output += f"{subindent}{file}" + os.linesep
            else:
                output += f"{subindent}{file}" + os.linesep
    sys.stdout.write(output)
    sys.stdout.flush()


def check_git() -> None:
    """Check that git is installed"""
    git_path = shutil.which("git")
    if git_path is None:
        error_msg = "'git' not found in path"
        error_msg += "\npath = \n"
        for path in os.environ["PATH"].split(os.path.pathsep):
            error_msg += f"  {path}\n"
        env_vars = os.environ.copy()
        env_vars.pop("PATH")
        error_msg += "\nENVIRONMENT:\n"
        for key, val in sorted(env_vars.items()):
            error_msg += f"  {key} = {val}\n"
        sys.stdout.write(f"{error_msg}\n")
        sys.stdout.flush()
        raise FileNotFoundError(error_msg)
