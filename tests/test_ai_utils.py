import unittest
from unittest.mock import patch, mock_open
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.ai_utils import (
    create_openai_client,
    generate_email_content,
    generate_user_content,
    analyze_email_for_information,
    summarize_information,
    get_next_step,
)


class TestAIUtils(unittest.TestCase):
    def test_summarize_information_no_data(self):
        with patch("builtins.open", mock_open(read_data="")):
            result = summarize_information()
            self.assertEqual(result, "No information available.")

    def test_create_openai_client(self):
        api_key = "test-api-key"
        client = create_openai_client(api_key)
        self.assertIsNotNone(client)
        self.assertEqual(client.api_key, api_key)
        self.assertEqual(client.base_url, "http://host.docker.internal:8080/v1/")


if __name__ == "__main__":
    unittest.main()
