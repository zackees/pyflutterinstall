"""
Runs the installer
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check
# pylint: disable=wrong-import-position

import argparse
import os
import shutil
import sys
import json
from typing import Callable
import warnings

# if --install-dir is specified, add it to the path
try:
    install_dir_found = sys.argv.index("--install-dir") + 1
    install_dir = sys.argv[install_dir_found]
    print(f"Setting install location to '{install_dir}'")
    os.chdir(install_dir)  # Do this early before any other imports
except BaseException:  # pylint: disable=broad-except
    pass

# isort: off
# black: off
from pyflutterinstall.flutter_doctor import postinstall_run_flutter_doctor
from pyflutterinstall.install.android_sdk import install_android_sdk
from pyflutterinstall.install.ant_sdk import install_ant_sdk
from pyflutterinstall.install.chrome import install_chrome
from pyflutterinstall.install.flutter_sdk import install_flutter_sdk
from pyflutterinstall.install.gradle import install_gradle
from pyflutterinstall.install.java_sdk import install_java_sdk
from pyflutterinstall.resources import (
    JAVA_SDK_VERSIONS,
    JAVA_VERSION,
)
from pyflutterinstall.paths import Paths
from pyflutterinstall.config import config_load, config_save, CONFIG_FILE
from pyflutterinstall.setenv import remove_env_path, unset_env_var, remove_all_paths


def ask_if_interactive(
    is_interactive: bool, callback_name: str, callback: Callable[[], int]
) -> int:
    if not is_interactive:
        return callback()
    do_install = input(f"install {callback_name} (y/n)? ") == "y"
    if not do_install:
        return 0
    return callback()


def check_preqs() -> None:
    if shutil.which("git") is None:
        print("Git is not installed, please install, add it to the path then continue.")
        sys.exit(1)
    if sys.platform == "linux":
        if shutil.which("ninja") is None:
            print(
                "Ninja is not installed, please install, add it to the path then continue."
            )
            sys.exit(1)


def handle_show_config(show_config: bool, verify_config: bool) -> int:
    if show_config:
        config_str = json.dumps(config_load(), indent=4)
        print(f"{CONFIG_FILE}:\n{config_str}")
        if not verify_config:
            return 0
    if verify_config:
        bad = False
        config = config_load()
        for key, val in config.items():
            if not os.path.exists(val):
                warnings.warn(f"Config value {key} is invalid: {val}")
                bad = True
        if bad:
            print("Please fix the above errors and try again.")
            return 1
        print("Config is valid.")
        return 0
    assert False, "unexpected state"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Installs Flutter Dependencies")
    parser.add_argument(
        "--show-config", action="store_true", help="Print the current configuration"
    )
    parser.add_argument(
        "--verify-config", action="store_true", help="Verify the current configuration"
    )
    parser.add_argument(
        "--skip-confirmation",
        "-y",
        action="store_true",
        help="Skip confirmation",
        default=False,
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Uninstalls pyflutterinstall and removes all files",
        default=False,
    )

    # Note that --install-dir is handled at the import level
    parser.add_argument("--install-dir", help="Install directory", default=None)
    parser.add_argument("--skip-java", action="store_true", help="Skip Java SDK")
    parser.add_argument("--skip-android", action="store_true", help="Skip Android SDK")
    parser.add_argument("--skip-ant", action="store_true", help="Skip Ant")
    parser.add_argument("--skip-flutter", action="store_true", help="Skip Flutter SDK")
    parser.add_argument("--skip-chrome", action="store_true", help="Skip Chrome")
    parser.add_argument(
        "--only-java", action="store_true", help="Only install Java SDK"
    )
    parser.add_argument(
        "--java-version",
        help="Java version to install",
        default=JAVA_VERSION,
        choices=JAVA_SDK_VERSIONS.keys(),
    )
    args = parser.parse_args()
    return args


def remove(cwd_override: str) -> int:
    paths = Paths(cwd_override=cwd_override)
    if paths.INSTALLED:
        paths.delete_all()
    else:
        warnings.warn("pyflutterinstall is not installed, skipping delete")
    config = config_load()
    env_paths: list[str] = config.get("PATHS", [])
    env: dict[str, str] = config.get("ENV", {})
    for p in env_paths:
        remove_env_path(str(p))
    for key in env:
        unset_env_var(key)
    config_save({})
    remove_all_paths()
    return 0


def main() -> int:
    cwd_override = os.getcwd()
    paths = Paths(cwd_override)
    args = parse_args()
    if args.show_config or args.verify_config:
        return handle_show_config(
            show_config=args.show_config, verify_config=args.verify_config
        )

    def install_java_sdk_versioned() -> int:
        return install_java_sdk(args.java_version)

    check_preqs()
    any_skipped = any(
        [args.skip_java, args.skip_android, args.skip_flutter, args.skip_chrome]
    )
    msg = ""
    if args.only_java:
        msg = "This will only install the Java SDK"
    else:
        msg = f"This will install Flutter and its dependencies into {os.path.basename(paths.INSTALL_DIR)}"

    if args.remove:
        return remove(cwd_override)

    print(msg)
    skip_confirmation = (
        args.skip_confirmation or input("auto-accept all? (y/n): ").lower() == "y"
    )
    interactive = not skip_confirmation
    print("\nInstalling Java/Flutter SDK and dependencies\n")
    config = config_load()
    config["ENV"] = {
        "ANDROID_SDK": str(paths.ANDROID_SDK),
        "GRADLE_DIR": str(paths.GRADLE_DIR),
        "INSTALL_DIR": str(paths.INSTALL_DIR),
        "JAVA_DIR": str(paths.INSTALL_DIR / "java"),
        "JAVA_HOME": str(paths.INSTALL_DIR / "java"),
        "FLUTTER_HOME": str(paths.FLUTTER_HOME),
    }
    config_save(config)
    paths.make_dirs()

    if args.only_java:
        rtn = install_java_sdk_versioned()
        if rtn != 0:
            warnings.warn("Java SDK install failed")
            return rtn
    else:
        if not args.skip_java:
            ask_if_interactive(interactive, "java_sdk", install_java_sdk_versioned)
        if not args.skip_android:

            def install_android_sdk_and_gradle():
                install_android_sdk(interactive)
                install_gradle()

            ask_if_interactive(
                interactive,
                "android_sdk",
                install_android_sdk_and_gradle,
            )
        if not args.skip_ant:
            install_ant_sdk()
        if not args.skip_flutter:
            ask_if_interactive(
                interactive, "flutter", lambda: install_flutter_sdk(interactive)
            )
        if not args.skip_chrome:
            ask_if_interactive(interactive, "chrome", install_chrome)
        if not args.skip_flutter:
            postinstall_run_flutter_doctor()
        if not any_skipped:
            print("\nDone installing Flutter SDK and dependencies\n")
    if sys.platform == "win32":
        print("Please restart your terminal to apply the changes")
    print(f"Paths: {paths.INSTALL_DIR}")
    print(f"Config: {CONFIG_FILE}")
    config = config_load()
    config_str = json.dumps(config, indent=4)
    print(f"Config:\n{config_str}")
    return 0


if __name__ == "__main__":
    sys.argv.append("-y")
    sys.exit(main())
