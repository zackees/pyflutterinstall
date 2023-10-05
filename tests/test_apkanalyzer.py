"""
Unit test file.
"""

# pylint: disable=R0801

import unittest

import os
from pyflutterinstall.config import config_load

# from pyflutterinstall.util import print_tree_dir
from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()


config = config_load()
INSTALLED = config.get("INSTALL_DIR") is not None


class ApkAnalyzerTester(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_apkanalyzer(self) -> None:
        """Tests that we can bind to the java executable."""
        # print("Test apkanalyzer")
        rtn = os.system("apkanalyzer --help")
        # print_tree_dir(paths.ANDROID_SDK, max_level=5, only_exe=True)
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
