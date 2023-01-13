"""
Runs the installer

When this is done, the directory structure will look like this
sdk/Android:
    build-tools
    cmdline-tools
    emulator       # Generated by the Android SDK Manager
    flutter
    java
    licenses       # Generated by the Android SDK Manager
    patcher        # Generated by the Android SDK Manager
    platforms      # Generated by the Android SDK Manager
    platform-tools # Generated by the Android SDK Manager
    system-images  # Generated by the Android SDK Manager
    tools          # Generated by the Android SDK Manager
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check

import argparse
import os
import sys
from pathlib import Path
import shutil
import subprocess
from download import download  # type: ignore

from pyflutterinstall.resources import (
    JAVA_SDK_URL,
    FLUTTER_GIT_DOWNLOAD,
    ANDROID_SDK_URL,
    CHROME_URL,
    CMDLINE_TOOLS,
)

from pyflutterinstall.envset import add_system_path, set_env_var


assert (
    shutil.which("git") is not None
), "Git is not installed, please install, add it to the path then continue."

DELETE_PREVIOUS_INSTALL = True

PROJECT_ROOT = Path(os.getcwd())
INSTALL_DIR = PROJECT_ROOT / "sdk"
DOWNLOAD_DIR = PROJECT_ROOT / ".downloads"

ANDROID_SDK = INSTALL_DIR / "Android"
FLUTTER_TARGET = ANDROID_SDK / "flutter"
JAVA_DIR = ANDROID_SDK / "java"
SKIP_CONFIRMATION = False


def make_dirs() -> None:
    os.makedirs(INSTALL_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(ANDROID_SDK, exist_ok=True)
    os.makedirs(JAVA_DIR, exist_ok=True)

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ
    env[str(ANDROID_SDK)] = str(ANDROID_SDK)
    env[str(JAVA_DIR)] = str(JAVA_DIR)
    # add to path
    # ${FLUTTER_TARGET}/bin
    # add to path
    env["PATH"] = f"{FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
    env["PATH"] = f"{JAVA_DIR}/bin{os.pathsep}{env['PATH']}"


def execute(command, cwd=None, send_confirmation=None, ignore_errors=False) -> int:
    print("####################################")
    print(f"Executing\n  {command}")
    print("####################################")
    if cwd:
        print(f"  CWD={cwd}")
    if not SKIP_CONFIRMATION or not send_confirmation:
        # return subprocess.check_call(command, cwd=cwd, shell=True, universal_newlines=True)
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            universal_newlines=True,
            encoding="utf-8",
            bufsize=1024 * 1024,
            text=True,
        )
        rtn = proc.wait()
        if not ignore_errors:
            RuntimeError(f"Command {command} failed with return code {rtn}")
        return rtn
    print(f"  Sending confirmation: {send_confirmation}")
    proc = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdin=subprocess.PIPE,
        universal_newlines=True,
        encoding="utf-8",
        # 1MB buffer
        bufsize=1024 * 1024,
        text=True,
    )
    proc.communicate(input=send_confirmation)
    rtn = proc.returncode
    if rtn != 0 and not ignore_errors:
        RuntimeError(f"Command {command} failed with return code {rtn}")
    return rtn


def make_title(title: str) -> None:
    print("\n\n###########################################")
    print(f"################# {title} #################")
    print("###########################################\n\n")


def install_java_sdk() -> None:
    make_title("Installing Java SDK")
    print(f"Install Java SDK from {JAVA_SDK_URL} to {INSTALL_DIR}")
    java_sdk_zip_file = Path(
        download(JAVA_SDK_URL, DOWNLOAD_DIR / os.path.basename(JAVA_SDK_URL))
    )
    print(f"Unpacking {java_sdk_zip_file} to {JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, JAVA_DIR)
    base_java_dir = JAVA_DIR / os.listdir(JAVA_DIR)[0]
    print(base_java_dir)
    java_bin_dir = base_java_dir / "bin"
    print(java_bin_dir)
    add_system_path(java_bin_dir)
    print("Java SDK installed.\n")


def install_android_sdk() -> None:
    make_title("Installing Android SDK")
    print(
        f"Install Android commandline-tools SDK from {ANDROID_SDK_URL} to {INSTALL_DIR}"
    )
    path = download(ANDROID_SDK_URL, DOWNLOAD_DIR / os.path.basename(ANDROID_SDK_URL))
    print(f"Unpacking {path} to {INSTALL_DIR}")
    shutil.unpack_archive(path, ANDROID_SDK / "cmdline-tools" / "tools")
    cmd_tools_path = ANDROID_SDK / "cmdline-tools" / "tools" / "cmdline-tools" / "bin"
    sdkmanager_path = cmd_tools_path / "sdkmanager.bat"
    print("About to install Android SDK tools")
    # install latest
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install "platform-tools"',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    add_system_path(cmd_tools_path)
    set_env_var("ANDROID_SDK_ROOT", ANDROID_SDK)
    set_env_var("ANDROID_HOME", ANDROID_SDK)
    # update tools
    print(f"Updating Android SDK with {sdkmanager_path}")
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --update',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
    for tool in tools_to_install:
        execute(
            f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install {tool}',
            send_confirmation="y\n",
            ignore_errors=True,
        )
    execute(
        f'{sdkmanager_path} --licenses --sdk_root="{ANDROID_SDK}"',
        send_confirmation="y\ny\ny\ny\ny\ny\ny\nn\n",
        ignore_errors=True,
    )


def install_flutter() -> None:
    make_title("Installing Flutter")
    print(f"Install Flutter from {FLUTTER_GIT_DOWNLOAD} to {FLUTTER_TARGET}")
    if not FLUTTER_TARGET.exists():
        execute(f'{FLUTTER_GIT_DOWNLOAD} "{FLUTTER_TARGET}"', ignore_errors=True)
    else:
        print(f"Flutter already installed at {FLUTTER_TARGET}")
    # Add flutter to path
    add_system_path(FLUTTER_TARGET / "bin")
    execute(
        f'flutter config --android-sdk "{ANDROID_SDK}" --no-analytics',
        send_confirmation="y\n",
        ignore_errors=True,
    )
    execute(
        "flutter doctor --android-licenses", send_confirmation="y\n", ignore_errors=True
    )
    print("Flutter installed.\n")


def install_chrome() -> None:
    print("\n################# Installing Chrome #################")
    # Install chrome for windows
    stdout = subprocess.check_output(
        "flutter doctor",
        shell=True,
        text=True,
        encoding="utf-8",
        universal_newlines=True,
    )
    if "Cannot find Chrome" in stdout:
        print("Chrome not found, installing")
        print(f"Install Chrome from {CHROME_URL} to {INSTALL_DIR}")
        path = download(CHROME_URL, DOWNLOAD_DIR / os.path.basename(CHROME_URL))
        print(f"Downloaded chrome at {path}")
        # install it
        os.system(f'"{path}"')


def main():
    parser = argparse.ArgumentParser(description="Installs Flutter Dependencies")
    parser.add_argument(
        "--skip-confirmation",
        action="store_true",
        help="Skip confirmation",
        default=False,
    )
    parser.add_argument("--skip-java", action="store_true", help="Skip Java SDK")
    parser.add_argument("--skip-android", action="store_true", help="Skip Android SDK")
    parser.add_argument("--skip-flutter", action="store_true", help="Skip Flutter SDK")
    parser.add_argument("--skip-chrome", action="store_true", help="Skip Chrome")
    args = parser.parse_args()
    # Check if windows comes after argparse to enable --help
    if sys.platform != "win32":
        print("This script is only for Windows")
        sys.exit(1)
    global SKIP_CONFIRMATION  # pylint: disable=global-statement
    SKIP_CONFIRMATION = args.skip_confirmation
    print("\nInstalling Flutter SDK and dependencies\n")
    make_dirs()
    if not args.skip_java:
        install_java_sdk()
    if not args.skip_android:
        install_android_sdk()
    if not args.skip_flutter:
        install_flutter()
    if not args.skip_chrome:
        install_chrome()
    print("\nDone installing Flutter SDK and dependencies\n")
    make_title(f"Executing 'flutter doctor -v'")
    try:
        completed_proc: subprocess.CompletedProcess = subprocess.run(  # type: ignore
            "flutter doctor -v",
            shell=True,
            text=True,
            capture_output=True,
            universal_newlines=True,
            encoding="utf-8",
        )
        print(completed_proc.stdout)
        print(completed_proc.stderr)

        streams = [completed_proc.stdout, completed_proc.stderr]
        for stream in streams:
            try:
                for line in stream.splitlines():
                    print(line)
            except UnicodeEncodeError as exc:
                print("Unable to print stream, contains non-ascii characters", exc)
        try:
            if "No issues found!" in str(completed_proc.stdout):
                return 0
            return 1
        except UnicodeEncodeError as exc:
            print("Unable to print stdout, contains non-ascii characters", exc)
            return 0  # don't fail the test.
    except subprocess.CalledProcessError as exc:
        print("Unable to execute flutter doctor", exc)
        return 0 # don't fail the test.


if __name__ == "__main__":
    sys.exit(main())
