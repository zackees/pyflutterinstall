"""
Install gradle
"""


import os
import shutil
import sys
from pathlib import Path

from download import download  # type: ignore

from pyflutterinstall.resources import GRADLE_URL
from pyflutterinstall.setenv import add_env_path


from pyflutterinstall.paths import Paths


def install_gradle() -> None:
    """Installs the gradle build tools"""
    paths = Paths()
    paths.apply_env()
    gradle_path_zip = Path(
        download(GRADLE_URL, paths.DOWNLOAD_DIR / os.path.basename(GRADLE_URL))
    )

    if os.path.exists(paths.GRADLE_DIR):
        print(f"Removing gradle at {paths.GRADLE_DIR}")
        shutil.rmtree(paths.GRADLE_DIR)
    shutil.unpack_archive(gradle_path_zip, paths.GRADLE_DIR)
    gradle_bin_dir = paths.GRADLE_DIR / os.listdir(paths.GRADLE_DIR)[0] / "bin"
    add_env_path(gradle_bin_dir)
    if sys.platform != "win32":
        gradle_exe = os.path.join(gradle_bin_dir, "gradle")
        assert os.path.exists(gradle_exe), f"gradle_exe {gradle_exe} does not exist"
        os.chmod(gradle_exe, 0o777)


if __name__ == "__main__":
    install_gradle()
