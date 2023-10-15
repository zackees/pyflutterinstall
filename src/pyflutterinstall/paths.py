"""
Provides a path interface to generate paths for the various tools.
"""

# pylint: disable=missing-function-docstring,invalid-name,pointless-string-statement,missing-class-docstring,too-many-instance-attributes
import os
import tempfile
import time

from dataclasses import dataclass
from pathlib import Path
import shutil
from setenvironment import reload_environment
from pyflutterinstall.config import config_load


def retry_delete(path, max_retries=3, delay=0.001):
    for _ in range(max_retries):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return
        except PermissionError:
            time.sleep(delay)
    print(f"Failed to delete {path} after {max_retries} attempts.")


def error_handler(func, path, exc_info):
    """Custom error handler for shutil.rmtree"""
    print(f"Error deleting {path}. Error: {exc_info[1]}")

    if os.name == "nt":
        os.chmod(path, 0o777)  # Try making the file/directory writable

    retry_delete(path)

    if not os.path.exists(path):
        return

    # Try to fix the issue for busy files by renaming and then deleting
    if "PermissionError" in str(exc_info[0]):
        tmp_dir = tempfile.mkdtemp(dir=os.path.dirname(path))
        tmp_path = os.path.join(tmp_dir, os.path.basename(path))

        try:
            os.rename(path, tmp_path)
            func(tmp_path)  # Retry the delete operation
            os.rmdir(tmp_dir)
            print(f"Successfully fixed and deleted {path}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Failed to fix the error for {path}. Error: {e}")


@dataclass
class Paths:
    INSTALL_ROOT: Path
    INSTALL_DIR: Path
    ENV_FILE: Path
    DOWNLOAD_DIR: Path
    ANDROID_SDK: Path
    ANDROID_HOME: Path
    ANT_DIR: Path
    FLUTTER_HOME: Path
    FLUTTER_HOME_BIN: Path
    JAVA_DIR: Path
    GRADLE_DIR: Path
    CMDLINE_TOOLS_DIR: Path
    BUILD_TOOLS_DIR: Path
    OVERRIDEN: bool
    INSTALLED: bool

    def __init__(self, cwd_override: str | None = None):
        if cwd_override is not None:
            self.OVERRIDEN = True
            self.INSTALL_ROOT = Path(cwd_override).resolve()
            self.INSTALL_DIR = self.INSTALL_ROOT / "FlutterSDK"
            self.ANDROID_SDK = self.INSTALL_DIR / "Android" / "sdk"
        else:
            self.OVERRIDEN = False
            config = config_load()
            env = config.vars
            assert env is not None
            maybe_android_sdk = env.get("ANDROID_SDK", None)
            assert maybe_android_sdk is not None
            android_sdk = Path(maybe_android_sdk).resolve()
            self.ANDROID_SDK = android_sdk
            self.INSTALL_DIR = self.ANDROID_SDK.parent.parent
            self.INSTALL_ROOT = self.INSTALL_DIR.parent
        self.INSTALLED = self.ANDROID_SDK.name == "sdk"
        self.ANDROID_HOME = self.ANDROID_SDK
        self.ENV_FILE = self.INSTALL_ROOT / ".env"
        self.DOWNLOAD_DIR = self.INSTALL_ROOT / ".downloads"
        self.ANDROID_SDK = self.ANDROID_SDK
        self.ANT_DIR = self.INSTALL_DIR / "ant"
        self.FLUTTER_HOME = self.INSTALL_DIR / "flutter"
        self.FLUTTER_HOME_BIN = self.FLUTTER_HOME / "bin"
        self.JAVA_DIR = self.INSTALL_DIR / "java"
        self.GRADLE_DIR = self.INSTALL_DIR / "gradle"
        self.CMDLINE_TOOLS_DIR = self.ANDROID_SDK / "cmdline-tools" / "latest" / "bin"
        self.BUILD_TOOLS_DIR = self.ANDROID_SDK / "build-tools"

    def apply_env(self) -> None:
        """Apply environment variables"""
        reload_environment(verbose=True)

    def make_dirs(self) -> None:
        # assert self.OVERRIDEN is False
        if not self.OVERRIDEN:
            raise AssertionError("make_dirs() should only be called when not overriden")
        """Make directories for installation"""
        # os.makedirs(INSTALL_DIR, exist_ok=True)
        # os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        # os.makedirs(ANDROID_SDK, exist_ok=True)
        # os.makedirs(JAVA_DIR, exist_ok=True)
        os.makedirs(self.INSTALL_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(self.ANDROID_SDK, exist_ok=True)
        os.makedirs(self.JAVA_DIR, exist_ok=True)
        sep = os.sep
        # INSTALL_DIR.mkdir(parents=True, exist_ok=True)
        # DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        env = os.environ
        env["ANDROID_SDK"] = str(self.ANDROID_SDK)
        env["JAVA_DIR"] = str(self.JAVA_DIR)
        # add to path
        # ${FLUTTER_HOME}/bin
        # add to path
        # env["PATH"] = f"{FLUTTER_HOME}/bin{os.pathsep}{env['PATH']}"
        # env["PATH"] = f"{JAVA_DIR}/bin{os.pathsep}{env['PATH']}"
        env["PATH"] = f"{self.FLUTTER_HOME}{sep}bin{os.pathsep}{env['PATH']}"
        env["PATH"] = f"{self.JAVA_DIR}{sep}bin{os.pathsep}{env['PATH']}"

    def delete_all(self) -> None:
        """Delete all directories"""
        if os.path.exists(self.INSTALL_DIR):
            print(f"Removing existing Flutter SDK at {self.INSTALL_DIR}")
            shutil.rmtree(self.INSTALL_DIR, onerror=error_handler)

    def __str__(self) -> str:
        # auto parse into list[str]
        out = []
        for key, value in self.__dict__.items():
            out.append(f"{key}={value}")
        return "\n".join(out)
