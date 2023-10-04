"""
Unit test file.
"""

import unittest

import os
from pyflutterinstall.config import config_load

config = config_load()
INSTALLED = config.get("INSTALL_DIR") is not None


class JavaTest(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test apkanalyzer")
        rtn = os.system("apkanalyzer --help")
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
