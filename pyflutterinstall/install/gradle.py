"""
Install gradle
"""


import os
import shutil
from pathlib import Path
from download import download  # type: ignore

from pyflutterinstall.resources import (
    DOWNLOAD_DIR,
    GRADLE_DIR
)

from pyflutterinstall.setenv import add_env_path


def install_gradle() -> None:
    # install gradle
    gradle_url = "https://services.gradle.org/distributions/gradle-7.6-bin.zip"
    gradle_path_zip = Path(download(gradle_url, DOWNLOAD_DIR / os.path.basename(gradle_url)))

    if os.path.exists(GRADLE_DIR):
        print(f"Removing gradle at {GRADLE_DIR}")
        shutil.rmtree(GRADLE_DIR)
    shutil.unpack_archive(gradle_path_zip, GRADLE_DIR)
    gradle_bin_dir = GRADLE_DIR / os.listdir(GRADLE_DIR)[0] / "bin"
    add_env_path(gradle_bin_dir)


if __name__ == "__main__":
    install_gradle()
