"""
Unit test file.
"""

import unittest

import os
import subprocess
import shutil
from pyflutterinstall.config import config_load

config = config_load()
INSTALLED = config.get("INSTALL_DIR") is not None

from pyflutterinstall.resources import (
    ANDROID_SDK,
)

from pyflutterinstall.util import print_tree_dir

class ApkAnalyzerTester(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_apkanalyzer(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test apkanalyzer")
        java_version = subprocess.check_output(
            "java -version",
            shell=True,
            universal_newlines=True,
            stderr=subprocess.STDOUT,
        )
        print(f"Java version: {java_version}\n")
        java_path = shutil.which("java")
        print(f"Java path: {java_path}\n")
        rtn = os.system("apkanalyzer --help")
        print_tree_dir(ANDROID_SDK, max_level=5)
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
