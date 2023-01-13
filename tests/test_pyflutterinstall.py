import unittest
import os


class PyflutterinstallTester(unittest.TestCase):
    def test_platform_executable(self) -> None:
        rtn = os.system("python -m pyflutterinstall.run --help")
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
