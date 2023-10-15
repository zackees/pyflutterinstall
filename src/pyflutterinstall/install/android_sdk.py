"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import os
import shutil
import sys

from download import download  # type: ignore
from pyflutterinstall.interactive_execute import execute

from pyflutterinstall.paths import Paths


from pyflutterinstall.resources import (
    ANDROID_SDK_URL,
    CMDLINE_TOOLS,
    IS_GITHUB_RUNNER,
)
from pyflutterinstall.setenv import add_env_path, set_env_var
from pyflutterinstall.util import make_title, check_git

BULK_INSTALL_TOOLS = True


def install_sdk_tools(sdkmanager_path: str) -> None:
    paths = Paths()
    paths.apply_env()
    if not BULK_INSTALL_TOOLS:
        tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
        for tool in tools_to_install:
            execute(
                f'{sdkmanager_path} --sdk_root="{paths.ANDROID_SDK}" --verbose --install {tool}',
                ignore_errors=False,
                timeout=60 * 20,
            )
    else:
        tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
        # Combine all tools into a single string, separated by spaces
        tools_string = " ".join(tools_to_install)

        # Execute the sdkmanager command once with all the tools listed
        execute(
            f'{sdkmanager_path} --sdk_root="{paths.ANDROID_SDK}" --verbose --install {tools_string}',
            ignore_errors=False,
            timeout=60 * 20,
        )


def install_android_sdk() -> int:
    check_git()
    paths = Paths()
    paths.apply_env()
    check_git()
    make_title("Installing Android SDK")
    print(
        f"Install Android commandline-tools SDK from {ANDROID_SDK_URL} to {paths.INSTALL_DIR}"
    )
    # sdk\Android\tools\bin\sdkmanager.bat
    path = download(
        ANDROID_SDK_URL, paths.DOWNLOAD_DIR / os.path.basename(ANDROID_SDK_URL)
    )
    print(f"Unpacking {path} to {paths.INSTALL_DIR}")
    shutil.unpack_archive(path, paths.ANDROID_SDK / "cmdline-tools" / "tools")
    sdkmanager_name = "sdkmanager.bat" if os.name == "nt" else "sdkmanager"
    sdkmanager_path = (
        paths.ANDROID_SDK
        / "cmdline-tools"
        / "tools"
        / "cmdline-tools"
        / "bin"
        / sdkmanager_name
    )
    if not os.path.exists(sdkmanager_path):
        raise FileNotFoundError(f"Could not find {sdkmanager_path}")
    os.chmod(sdkmanager_path, 0o755)
    # Adding the sdkmanager shouldn't be needed because it should be installed to
    # latest.
    # add_env_path(sdkmanager_path.parent)
    print("About to install Android SDK tools")
    # install latest
    execute(
        f'{sdkmanager_path} --sdk_root="{paths.ANDROID_SDK}" --install "platform-tools"',
        ignore_errors=False,
    )
    set_env_var("ANDROID_SDK_ROOT", paths.ANDROID_SDK)
    set_env_var("ANDROID_HOME", paths.ANDROID_SDK)
    # update tools
    print(f"Updating Android SDK with {sdkmanager_path}")
    execute(
        f'{sdkmanager_path} --sdk_root="{paths.ANDROID_SDK}" --update',
        ignore_errors=False,
    )
    install_sdk_tools(str(sdkmanager_path))
    confirmation = "y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\nn\n"
    send_confirmation = []
    send_confirmation.append(
        ("Review licenses that have not been accepted (y/N)?", "y")
    )
    for conf in confirmation.splitlines():
        send_confirmation.append(("Accept? (y/N):", conf))
    execute(
        f'{sdkmanager_path} --licenses --sdk_root="{paths.ANDROID_SDK}"',
        ignore_errors=False,
    )
    add_env_path(paths.ANDROID_SDK / "platform-tools")
    add_env_path(paths.ANDROID_SDK / "emulator")
    add_env_path(paths.ANDROID_SDK / "tools" / "bin")
    # avdmanager needs to get picked up from here.
    add_env_path(paths.ANDROID_SDK / "cmdline-tools" / "latest" / "bin")
    # now add build tools
    if os.path.exists(paths.BUILD_TOOLS_DIR):
        for build_tool in os.listdir(paths.BUILD_TOOLS_DIR):
            add_env_path(paths.BUILD_TOOLS_DIR / build_tool)
            break
    if sys.platform == "darwin":
        if IS_GITHUB_RUNNER:
            package_mgr = "gem"
        else:
            package_mgr = "brew"
        execute(f"{package_mgr} install cocoapods", ignore_errors=True)
    check_git()
    return 0


def main():
    install_android_sdk()


if __name__ == "__main__":
    print("blah")
    sys.exit(main())
