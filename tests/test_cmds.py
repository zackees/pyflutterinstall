"""
Unit test file.
"""

import os
import unittest
from shutil import which
from pyflutterinstall.paths import Paths

paths = Paths()
paths.apply_env()
INSTALLED = paths.INSTALLED


class UseExePaths(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test java")
        rtn = os.system("java -version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_adb(self) -> None:
        """Tests that we can bind to the adb executable."""
        print("Test adb")
        rtn = os.system("adb version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_avdmanager(self) -> None:
        """Tests that we can bind to the avdmanager executable."""
        print("Test avdmanager")
        print(f"which avdmanager: {which('avdmanager')}")
        rtn = os.system("avdmanager list")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_gradle(self) -> None:
        """Tests that we can bind to the gradle executable."""
        print("Test gradle")
        rtn = os.system("gradle -version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_sdkmanager(self) -> None:
        """Tests that we can bind to the sdkmanager executable."""
        print("Test sdkmanager")
        print(f"which sdkmanager: {which('sdkmanager')}")
        rtn = os.system("sdkmanager --version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_emulator(self) -> None:
        """Tests that we can bind to the emulator executable."""
        print("Test emulator")
        rtn = os.system("emulator -help")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_aapt(self) -> None:
        """Tests that we can bind to the aapt executable."""
        print("Test aapt")
        rtn = os.system("aapt v")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_aapt2(self) -> None:
        """Tests that we can bind to the aapt2 executable."""
        print("Test aapt2")
        rtn = os.system("aapt2 version")
        self.assertEqual(0, rtn)

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_flutter(self) -> None:
        """Tests that we can bind to the aapt2 executable."""
        print("Test flutter")
        rtn = os.system("flutter --version")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
