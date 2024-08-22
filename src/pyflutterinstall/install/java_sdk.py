"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
import warnings
from typing import Optional

from download import download  # type: ignore

from pyflutterinstall.resources import (
    # DOWNLOAD_DIR,
    # INSTALL_DIR,
    # JAVA_DIR,
    get_platform_java_sdk,
    JAVA_SDK_VERSIONS,
    JAVA_VERSION,
)
from pyflutterinstall.setenv import add_env_path, set_env_var
from pyflutterinstall.util import make_title, check_git

from pyflutterinstall.paths import Paths


def print_paths() -> None:
    call_frame = sys._getframe(1)  # pylint: disable=protected-access
    calling_function = call_frame.f_code.co_name
    calling_function_line = call_frame.f_lineno
    os_paths = os.environ["PATH"].split(os.pathsep)
    msg = f"PATHS from {calling_function}({calling_function_line}):\n"
    for path in os_paths:
        msg += f"  {path}\n"
    # print(msg)
    sys.stdout.write(f"{msg}\n")
    sys.stdout.flush()


def _download(url: str, path: Path, replace: bool = False) -> Path:
    retries = 10
    for i in range(retries):
        try:
            if path.exists() and not replace:
                return path
            return Path(download(url=url, path=path, replace=replace))
        except Exception as e:  # pylint: disable=broad-except
            if "Exception: Error: File size is" in str(
                e
            ) or "Error while fetching file" in str(e):
                print(f"Error downloading {url}: {e}")
                print(f"Retrying download {i+1}/{retries}")
                replace = True
                continue
            break
    alt_url = url.replace("/latest/", "/archive/")
    print(f"Trying backup url: {alt_url}")
    for i in range(retries):
        try:
            if path.exists() and not replace:
                return path
            return Path(download(url=alt_url, path=path, replace=replace))
        except Exception as e:
            if "Exception: Error: File size is" in str(
                e
            ) or "Error while fetching file" in str(e):
                print(f"Error downloading {alt_url}: {e}")
                print(f"Retrying download {i+1}/{retries}")
                continue
            raise
    raise FileNotFoundError(f"Failed to download {url} or {alt_url}")


def install_java_sdk(version: Optional[int] = None) -> int:
    make_title("Installing Java SDK")
    check_git()
    print_paths()
    paths = Paths()
    paths.apply_env()
    print_paths()
    check_git()
    java_sdk_url = get_platform_java_sdk(version)
    local_file = paths.DOWNLOAD_DIR / os.path.basename(java_sdk_url)
    print(f"Install Java SDK from {java_sdk_url} to {local_file}")
    java_sdk_zip_file = _download(url=java_sdk_url, path=local_file, replace=False)
    print(f"Unpacking {java_sdk_zip_file} to {paths.JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, paths.JAVA_DIR)
    base_java_dir = paths.JAVA_DIR / os.listdir(paths.JAVA_DIR)[0]
    print(base_java_dir)
    if sys.platform == "darwin":
        java_bin_dir = base_java_dir / "Contents" / "Home" / "bin"
    else:
        java_bin_dir = base_java_dir / "bin"
    # check that java is in the path
    print(java_bin_dir)
    java_exe = "java.exe" if os.name == "nt" else "java"
    assert java_exe in os.listdir(java_bin_dir), "java not found in java bin dir"
    add_env_path(java_bin_dir)
    if sys.platform == "darwin":
        set_env_var("JAVA_HOME", str(base_java_dir / "Contents" / "Home"))
    else:
        set_env_var("JAVA_HOME", str(base_java_dir))
    paths.apply_env()
    found_java_path = shutil.which("java")
    assert found_java_path is not None, "No java path found"
    if str(java_bin_dir) not in found_java_path:
        msg = f"java installed not in expected path ({str(java_bin_dir)}), instead it's {found_java_path}\n"
        msg += "os environmental settings: \n"
        os_env = os.environ.copy()
        os_paths = os_env.pop("PATH", "").split(os.pathsep)
        os_paths = [str(Path(p).resolve()) for p in os_paths]
        for key, value in sorted(os_env.items()):
            msg += f"  {key}={value}\n"
        # print paths
        msg += "  PATH:\n"
        for path in os_paths:
            msg += f"    {path}\n"
        warnings.warn(msg)
        raise AssertionError(msg)
    assert (
        str(java_bin_dir) in found_java_path
    ), f"java installed not in expected path ({str(java_bin_dir)}), instead it's {found_java_path}"
    java_version = subprocess.check_output(
        "java -version", shell=True, universal_newlines=True, stderr=subprocess.STDOUT
    )
    print(f"Java SDK installed: {java_version}\n")
    check_git()
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        type=int,
        default=JAVA_VERSION,
        help="The version of Java to install",
        choices=JAVA_SDK_VERSIONS.keys(),
    )
    args = parser.parse_args()
    install_java_sdk(args.version)


if __name__ == "__main__":
    main()
