"""Used in testing."""

import sys

prompt = input("Accept? (y/n): ")
sys.exit(0 if prompt == "y" else 1)
