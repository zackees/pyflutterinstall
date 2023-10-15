"""
Test pyflutterinstall
"""

import unittest
import subprocess

from setenvironment import reload_environment

reload_environment()


def exe(cmd: str) -> str:
    """Run a command and return the stdout, or raise an exception."""
    proc = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Error executing {cmd}\n{stderr}")
    return stdout


class PyflutterinstallTester(unittest.TestCase):
    """Tests pyflutterinstall"""

    def test_platform_executable(self) -> None:
        """Tests the platform executable"""
        # rtn = os.system("java --version")
        # self.assertEqual(rtn, 0)
        exe("java --version")


if __name__ == "__main__":
    unittest.main()
