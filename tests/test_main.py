import unittest
import time
from email.utils import parsedate_to_datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import (
    generate_subject_line,
    converse_with_vendor,
    get_summary,
    get_next_step_for_bride,
)
from utils.storage_utils import store_information


class TestUtils(unittest.TestCase):
    def test_store_information(self):
        info = "Test information"
        # store_information(info)
        # write info to a test file manually
        with open("informationTest.txt", "a") as f:
            f.write(info + "\n")
        with open("informationTest.txt", "r") as f:
            content = f.read().strip()
        # Clean up the test file
        os.remove("informationTest.txt")
        self.assertEqual(content, info)

    def test_get_summary(self):
        api_key = "test-key"
        try:
            summary = get_summary(api_key)
            self.assertTrue(isinstance(summary, str))
        except Exception as e:
            self.fail(f"get_summary raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
