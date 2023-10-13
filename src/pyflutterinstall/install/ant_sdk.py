"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import os
import shutil
import sys
from pathlib import Path

from download import download  # type: ignore
from pyflutterinstall.interactive_execute import execute

from pyflutterinstall.resources import (
    # ANT_DIR,
    ANT_SDK_DOWNLOAD,
    # DOWNLOAD_DIR,
    # INSTALL_DIR,
)
from pyflutterinstall.setenv import add_env_path
from pyflutterinstall.util import make_title


from pyflutterinstall.paths import Paths


def install_ant_sdk() -> int:
    make_title("Installing Ant SDK")
    paths = Paths()
    paths.apply_env()
    if shutil.which("ant") is not None:
        print("Ant already installed")
        return 0
    if sys.platform in ["win32", "linux"]:
        print(f"Install Ant from {ANT_SDK_DOWNLOAD} to {paths.INSTALL_DIR}")
        ant_sdk_sip = Path(
            download(
                ANT_SDK_DOWNLOAD,
                paths.DOWNLOAD_DIR / os.path.basename(ANT_SDK_DOWNLOAD),
            )
        )
        if os.path.exists(paths.ANT_DIR):
            print(f"Removing existing Ant SDK at {paths.ANT_DIR}")
            shutil.rmtree(paths.ANT_DIR)
        print(f"Unpacking {ant_sdk_sip} to {paths.ANT_DIR}")
        shutil.unpack_archive(ant_sdk_sip, paths.ANT_DIR)
        base_ant_dir = paths.ANT_DIR / os.listdir(paths.ANT_DIR)[0]
        print(base_ant_dir)
        ant_bin_dir = base_ant_dir / "bin"
        add_env_path(ant_bin_dir)
        ant_exe = "ant.exe" if os.name == "nt" else "ant"
        if os.name != "nt":
            os.chmod(ant_bin_dir / ant_exe, 0o755)
        # check that ant is in the path
        print(f"Ant SDK installed: {base_ant_dir}\n")
    if sys.platform == "darwin":
        execute("brew install ant")
    # assert shutil.which("ant"), "ant not found in ant bin dir"
    return 0


def main():
    install_ant_sdk()


if __name__ == "__main__":
    sys.exit(main())
