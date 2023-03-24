"""
Unit test file.
"""

import unittest

from pyflutterinstall.cmds import java


class JavaTest(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test java")
        self.assertEqual(0, java.main(["-version"]))


if __name__ == "__main__":
    unittest.main()
