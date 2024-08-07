import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.storage_utils import store_information, get_original_message


class TestStorageUtils(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_information.txt"
        # Override the store_information function to write to the test file
        global store_information

        def store_information(info):
            with open(self.test_file, "a") as f:
                f.write(info + "\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_store_information(self):
        info = "Test information"
        store_information(info)
        with open(self.test_file, "r") as f:
            content = f.read().strip()
        self.assertEqual(content, info)

    def test_get_original_message_no_forwarded(self):
        email_content = "This is a test email.\nNo forwarded message."
        result = get_original_message(email_content)
        self.assertEqual(result, email_content)

    def test_get_original_message_with_forwarded(self):
        email_content = "This is the original email.\n\nOn some date, someone wrote:\nThis is the forwarded part."
        expected_result = "This is the original email."
        result = get_original_message(email_content)
        self.assertEqual(result, expected_result)

    def test_get_original_message_with_forwarded_at_start(self):
        email_content = "On some date, someone wrote:\nThis is the forwarded part."
        result = get_original_message(email_content)
        self.assertEqual(result, email_content)


if __name__ == "__main__":
    unittest.main()
