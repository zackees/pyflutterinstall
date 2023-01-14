"""
Resources for pyflutterinstall
"""

# pylint: disable=line-too-long

import sys

FLUTTER_GIT_DOWNLOAD = "git clone --depth 1 https://github.com/flutter/flutter.git -b stable"
# Note that commit is 135454af32477f815a7525073027a3ff9eff1bfd
CMDLINE_TOOLS = [
    "system-images;android-30;default;x86_64",
    "cmdline-tools;latest",
    "platform-tools",
    "build-tools;33.0.1",
    "platforms;android-33",
    "emulator",
    "tools",
    "system-images;android-27;google_apis_playstore;x86"
]

if sys.platform == "win32":
    JAVA_SDK_URL = "https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip"
    ANDROID_SDK_URL = "https://dl.google.com/android/repository/commandlinetools-win-9123335_latest.zip"

    CHROME_URL = "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"

else:
    JAVA_SDK_URL = "https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip"
    ANDROID_SDK_URL = "https://dl.google.com/android/repository/commandlinetools-win-9123335_latest.zip"
    CHROME_URL = "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"
