"""
Command stub for sdkmanager
"""
import os
import sys
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load
import shutil

ANDROID_SDK = config_load().get("ANDROID_SDK", ".")
JAVA_DIR = config_load().get("JAVA_DIR", None)
if ANDROID_SDK != ".":
    os.environ["ANDROID_SDK"] = ANDROID_SDK
    os.environ["ANDROID_HOME"] = ANDROID_SDK

COMMAND = "sdkmanager"
DEFAULT_PATH = os.path.join(ANDROID_SDK, "cmdline-tools", "latest", "bin")


def find_java_exe(java_base_dir: str) -> str | None:
    """Find bin folder"""
    # use os walk
    for root, dirs, files in os.walk(java_base_dir):
        if "bin" in dirs:
            bin_dir = os.path.join(root, "bin")
            java_bin = os.path.join(bin_dir, "java")
            if sys.platform == "win32":
                java_bin += ".exe"
            if os.path.isfile(java_bin):
                return java_bin
    return None


def find_default_path_or_none() -> str | None:
    """Find default path"""
    if JAVA_DIR is None:
        return None
    jdk_folders = os.listdir(JAVA_DIR)
    if not jdk_folders:
        return None
    if len(jdk_folders) > 1:
        jdk_folders.sort()
        jdk_folders.reverse()
    print(f"jdk_folders: {jdk_folders}")
    base_java_dir = os.path.join(JAVA_DIR, jdk_folders[0])
    if "linux" in sys.platform:
        return base_java_dir
    if "darwin" in sys.platform:
        return os.path.join(base_java_dir, "Contents", "Home", "bin")
    #if sys.platform == "darwin":
    #    return os.path.join(base_java_dir, "Contents", "Home", "bin")
    # return os.path.join(base_java_dir, "bin")
    return base_java_dir

def main(argv: list[str] | None = None) -> int:
    """Main"""
    argv = argv or sys.argv[1:]
    has_sdk_root = False
    for arg in argv:
        if arg.startswith("--sdk_root"):
            has_sdk_root = True
            break
    if not has_sdk_root:
        argv.append(f"--sdk_root={ANDROID_SDK}")
    java_home = find_default_path_or_none()
    assert java_home is not None, "Java home not found"
    os.environ["JAVA_HOME"] = java_home
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
