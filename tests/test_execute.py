"""
Test pyflutterinstall
"""

import unittest
import os
import sys

from pyflutterinstall.execute import execute

if sys.platform == "win32":
    from wexpect import spawn, EOF  # type: ignore  # pylint: disable=import-error
else:
    from pexpect import spawn, EOF  # type: ignore  # pylint: disable=import-error

HERE = os.path.abspath(os.path.dirname(__file__))
ACCEPT_PY = os.path.join(HERE, "accept.py")


class FakeStream:
    """Fake input stream."""

    def __init__(self) -> None:
        self.buffer = ""

    def write(self, data: str) -> None:
        """Writes to the buffer."""
        self.buffer += data
        sys.stdout.write(data)

    def flush(self) -> None:
        """Flushes the buffer."""
        sys.stdout.flush()


class ExecuteTester(unittest.TestCase):
    """Tests pyflutterinstall"""

    def test_platform_executable(self) -> None:
        """Tests the platform executable"""
        fake_stream = FakeStream()

        rtn = execute(
            f"python {ACCEPT_PY}",
            send_confirmation=[("Accept? (y/n): ", "y")],
            outstream=fake_stream,
        )
        if sys.platform != "win32":
            self.assertIn("ok - y", fake_stream.buffer)
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
