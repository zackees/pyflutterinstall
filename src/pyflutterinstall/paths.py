"""
Provides a path interface to generate paths for the various tools.
"""

# pylint: disable=missing-function-docstring,invalid-name,pointless-string-statement,missing-class-docstring,too-many-instance-attributes
import os

from dataclasses import dataclass
from pathlib import Path
from pyflutterinstall.config import config_load


"""
prior definitions
-PROJECT_ROOT = Path(os.getcwd())
-INSTALL_DIR = PROJECT_ROOT / "FlutterSDK"
-ENV_FILE = PROJECT_ROOT / ".env"
-DOWNLOAD_DIR = PROJECT_ROOT / ".downloads"
-ANDROID_SDK = INSTALL_DIR / "Android" / "sdk"
-ANT_DIR = INSTALL_DIR / "ant"
-FLUTTER_TARGET = INSTALL_DIR / "flutter"
-JAVA_DIR = INSTALL_DIR / "java"
-GRADLE_DIR = INSTALL_DIR / "gradle"
-CMDLINE_TOOLS_DIR = ANDROID_SDK / "cmdline-tools" / "latest" / "bin"
-BUILD_TOOLS_DIR = ANDROID_SDK / "build-tools"
+# PROJECT_ROOT = Path(os.getcwd()).resolve()
+# INSTALL_DIR = PROJECT_ROOT / "FlutterSDK"
+# ENV_FILE = PROJECT_ROOT / ".env"
+# DOWNLOAD_DIR = PROJECT_ROOT / ".downloads"
+# ANDROID_SDK = INSTALL_DIR / "Android" / "sdk"
+# ANT_DIR = INSTALL_DIR / "ant"
"""


@dataclass
class Paths:
    INSTALL_ROOT: Path
    INSTALL_DIR: Path
    ENV_FILE: Path
    DOWNLOAD_DIR: Path
    ANDROID_SDK: Path
    ANDROID_HOME: Path
    ANT_DIR: Path
    FLUTTER_TARGET: Path
    JAVA_DIR: Path
    GRADLE_DIR: Path
    CMDLINE_TOOLS_DIR: Path
    BUILD_TOOLS_DIR: Path
    OVERRIDEN: bool

    def __init__(self, cwd_override: str | None = None):
        if cwd_override is not None:
            self.OVERRIDEN = True
            self.INSTALL_ROOT = Path(cwd_override).resolve()
            self.INSTALL_DIR = self.INSTALL_ROOT / "FlutterSDK"
            self.ANDROID_SDK = self.INSTALL_DIR / "Android" / "sdk"
        else:
            self.OVERRIDEN = False
            self.ANDROID_SDK = Path(config_load().get("ANDROID_SDK", ".")).resolve()
            self.INSTALL_DIR = self.ANDROID_SDK.parent
            self.INSTALL_ROOT = self.INSTALL_DIR.parent
        self.ANDROID_HOME = self.ANDROID_SDK
        self.ENV_FILE = self.INSTALL_ROOT / ".env"
        self.DOWNLOAD_DIR = self.INSTALL_ROOT / ".downloads"
        self.ANDROID_SDK = self.ANDROID_SDK
        self.ANT_DIR = self.INSTALL_DIR / "ant"
        self.FLUTTER_TARGET = self.INSTALL_DIR / "flutter"
        self.JAVA_DIR = self.INSTALL_DIR / "java"
        self.GRADLE_DIR = self.INSTALL_DIR / "gradle"
        self.CMDLINE_TOOLS_DIR = self.ANDROID_SDK / "cmdline-tools" / "latest" / "bin"
        self.BUILD_TOOLS_DIR = self.ANDROID_SDK / "build-tools"

    def apply_env(self) -> None:
        """Apply environment variables"""
        env = os.environ
        env["ANDROID_SDK"] = str(self.ANDROID_SDK)
        env["JAVA_DIR"] = str(self.JAVA_DIR)
        env["PATH"] = f"{self.FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
        env["PATH"] = f"{self.JAVA_DIR}/bin{os.pathsep}{env['PATH']}"

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

        # INSTALL_DIR.mkdir(parents=True, exist_ok=True)
        # DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        env = os.environ
        env["ANDROID_SDK"] = str(self.ANDROID_SDK)
        env["JAVA_DIR"] = str(self.JAVA_DIR)
        # add to path
        # ${FLUTTER_TARGET}/bin
        # add to path
        # env["PATH"] = f"{FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
        # env["PATH"] = f"{JAVA_DIR}/bin{os.pathsep}{env['PATH']}"
        env["PATH"] = f"{self.FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
        env["PATH"] = f"{self.JAVA_DIR}/bin{os.pathsep}{env['PATH']}"

    def __str__(self) -> str:
        # auto parse into list[str]
        out = []
        for key, value in self.__dict__.items():
            out.append(f"{key}={value}")
        return "\n".join(out)
