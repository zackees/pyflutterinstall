"""
Resources for pyflutterinstall
"""

# pylint: disable=line-too-long,fixme

import os
import sys
from pathlib import Path
import platform

FLUTTER_GIT_DOWNLOAD = (
    "git clone --depth 1 https://github.com/flutter/flutter.git -b stable"
)
# Note that commit is 135454af32477f815a7525073027a3ff9eff1bfd
CMDLINE_TOOLS = [
    "system-images;android-30;default;x86_64",
    "cmdline-tools;latest",
    "platform-tools",
    "build-tools;33.0.1",
    "platforms;android-33",
    "emulator",
    "tools",
    "system-images;android-27;google_apis_playstore;x86",
]


def get_platform_java_sdk() -> str:
    """Gets the java platform specific url"""
    if sys.platform == "win32":
        return "https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip"
    if sys.platform == "darwin":
        if platform.machine() == "x86_64":
            return (
                "https://download.oracle.com/java/19/latest/jdk-19_macos-x64_bin.tar.gz"
            )
        return (
            "https://download.oracle.com/java/19/latest/jdk-19_macos-aarch64_bin.tar.gz"
        )
    return "https://download.oracle.com/java/19/latest/jdk-19_linux-x64_bin.tar.gz"


def get_android_sdk_url() -> str:
    """Gets the android platform specific url"""
    if sys.platform == "win32":
        return "https://dl.google.com/android/repository/commandlinetools-win-9123335_latest.zip"
    if sys.platform == "darwin":
        return "https://dl.google.com/android/repository/commandlinetools-mac-9123335_latest.zip"
    return "https://dl.google.com/android/repository/commandlinetools-linux-9123335_latest.zip"


def get_chrome_url() -> str:
    """Gets the chrome platform specific url"""
    if sys.platform == "win32":
        return "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"
    if sys.platform == "darwin":
        return "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
    return "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"


CHROME_URL = get_chrome_url()
ANDROID_SDK_URL = get_android_sdk_url()
JAVA_SDK_URL = get_platform_java_sdk()
PROJECT_ROOT = Path(os.getcwd())
INSTALL_DIR = PROJECT_ROOT / "FlutterSDK"
ENV_FILE = PROJECT_ROOT / ".env"
DOWNLOAD_DIR = PROJECT_ROOT / ".downloads"
ANDROID_SDK = INSTALL_DIR / "Android"
FLUTTER_TARGET = ANDROID_SDK / "flutter"
JAVA_DIR = ANDROID_SDK / "java"
IS_GITHUB_RUNNER = os.getenv("GITHUB_ACTIONS", "false") == "true"
