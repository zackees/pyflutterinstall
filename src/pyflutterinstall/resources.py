"""
Resources for pyflutterinstall
"""

# pylint: disable=line-too-long,fixme

import os
import sys
import platform
from typing import Optional

CMDLINE_TOOLS_VERSION = "latest"
BUILD_TOOLS_VERSION = "34.0.0"
ANDROID_SDK_VERSION = "11076708"
JAVA_VERSION = 17
GRADLE_URL = "https://services.gradle.org/distributions/gradle-8.7-all.zip"
SOURCES_VERSION = "android-35"
PLATFORMS_VERSION = "android-35"

# Flutter 3.16 beta
FLUTTER_COMMIT = "f0abad66b249244cbdbb291cf6edfbba9937ffa0"

ANT_SDK_DOWNLOAD = "https://dlcdn.apache.org//ant/binaries/apache-ant-1.10.13-bin.zip"
# Note that commit is 135454af32477f815a7525073027a3ff9eff1bfd
CMDLINE_TOOLS = [
    f"sources;{SOURCES_VERSION}",
    # HUGE
    # "system-images;android-33;google_apis;x86_64",
    f"cmdline-tools;{CMDLINE_TOOLS_VERSION}",
    "platform-tools",
    f"build-tools;{BUILD_TOOLS_VERSION}",
    f"platforms;{PLATFORMS_VERSION}",
    "emulator",
    "tools",
]


# Not all versions of java support getting url by version number.
def get_platform_java_sdk_dynamic(version: str) -> str:
    """Gets the java platform specific url using the version string."""
    major_version = int(version.split(".")[0])
    if sys.platform == "win32":
        return f"https://download.oracle.com/java/{major_version}/latest/jdk-{version}_windows-x64_bin.zip"
    if platform.machine() == "x86_64":
        arch = "x64"
    else:
        arch = "aarch64"
    if sys.platform == "darwin":
        return f"https://download.oracle.com/java/{major_version}/latest/jdk-{version}_macos-{arch}_bin.tar.gz"
    if "linux" in sys.platform:
        return f"https://download.oracle.com/java/{major_version}/latest/jdk-{version}_linux-{arch}_bin.tar.gz"
    raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def get_platform_java_sdk11() -> str:
    """Gets the java platform specific url"""
    if sys.platform == "win32":
        return "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.18%2B10/OpenJDK11U-jdk_x64_windows_hotspot_11.0.18_10.zip"
    if sys.platform == "darwin":
        return "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.18%2B10/OpenJDK11U-jdk_x64_mac_hotspot_11.0.18_10.tar.gz"
    if "linux" in sys.platform:
        return "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.18%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.18_10.tar.gz"
    raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def get_platform_java_sdk17() -> str:
    """Gets the java platform specific url"""
    return get_platform_java_sdk_dynamic("17.0.6")


def get_platform_java_sdk20() -> str:
    """Java version 20."""
    return get_platform_java_sdk_dynamic("20")


def get_platform_java_sdk21() -> str:
    """Java version 21."""
    return get_platform_java_sdk_dynamic("21")


def get_platform_java_sdk8() -> str:
    """Gets the java platform specific url"""
    return get_platform_java_sdk_dynamic("8.0.312")


JAVA_SDK_VERSIONS = {
    8: get_platform_java_sdk8,
    11: get_platform_java_sdk11,
    17: get_platform_java_sdk17,
    20: get_platform_java_sdk20,
    21: get_platform_java_sdk21,
}


def get_platform_java_sdk(version: Optional[int] = None) -> str:
    """Gets the java platform specific url"""
    version = version or JAVA_VERSION
    url_function = JAVA_SDK_VERSIONS.get(version)
    if url_function:
        return url_function()
    raise NotImplementedError(f"Unsupported java version: {version}")


def get_android_sdk_url() -> str:
    """Gets the android platform specific url"""
    version = ANDROID_SDK_VERSION
    if sys.platform == "win32":
        os_name = "win"
    elif sys.platform == "darwin":
        os_name = "mac"
    else:
        os_name = "linux"
    return f"https://dl.google.com/android/repository/commandlinetools-{os_name}-{version}_latest.zip"


def get_chrome_url() -> str:
    """Gets the chrome platform specific url"""
    if sys.platform == "win32":
        return "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"
    if sys.platform == "darwin":
        return "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
    return "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"


CHROME_URL = get_chrome_url()
ANDROID_SDK_URL = get_android_sdk_url()
IS_GITHUB_RUNNER = os.getenv("GITHUB_ACTIONS", "false") == "true"
