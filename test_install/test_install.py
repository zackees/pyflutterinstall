import unittest
import os


class InstallerTest(unittest.TestCase):
    def test_platform_executable(self) -> None:
        rtn = os.system("pyflutterinstall --skip-confirmation --skip-chrome")
        self.assertEqual(rtn, 0)
        

if __name__ == "__main__":
    unittest.main()
