import unittest


class PyflutterinstallTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def test_platform_executable(self) -> None:
        print("TODO add tests")


if __name__ == "__main__":
    unittest.main()
