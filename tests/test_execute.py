"""
Test pyflutterinstall
"""

import unittest
import os
import sys
import pexpect  # type: ignore

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
        child = pexpect.spawn(
            f"python {ACCEPT_PY}", encoding="utf-8", timeout=5, logfile=fake_stream
        )
        child.expect_exact("Accept? (y/n): ")
        child.sendline("y")
        child.expect(pexpect.EOF)
        child.close()
        self.assertEqual(child.exitstatus, 0)
        self.assertIsNone(child.signalstatus)


if __name__ == "__main__":
    unittest.main()
