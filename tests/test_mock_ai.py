import unittest
from unittest.mock import MagicMock, patch
import sys
import os

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
    @patch("utils.ai_utils.OpenAI")
    def test_create_openai_client(self, mock_openai):
        api_key = "test-api-key"
        client = MagicMock()
        mock_openai.return_value = client
        result = create_openai_client(api_key)
        mock_openai.assert_called_once_with(
            base_url="http://host.docker.internal:8080/v1", api_key=api_key
        )
        self.assertEqual(result, client)

    @patch("utils.ai_utils.generate_email_content")
    def test_generate_email_content(self, mock_generate_email_content):
        client = MagicMock()
        user_input = "Test user input"
        mock_generate_email_content.return_value = "Email content"
        result = mock_generate_email_content(client, user_input)
        self.assertEqual(result, "Email content")

    @patch("utils.ai_utils.generate_user_content")
    def test_generate_user_content(self, mock_generate_user_content):
        client = MagicMock()
        user_input = "Test user input"
        mock_generate_user_content.return_value = "User content"
        result = mock_generate_user_content(client, user_input)
        self.assertEqual(result, "User content")

    @patch("utils.ai_utils.analyze_email_for_information")
    def test_analyze_email_for_information(self, mock_analyze_email_for_information):
        client = MagicMock()
        user_request = "Test user request"
        email_body = "Test email body"
        mock_analyze_email_for_information.return_value = True
        result = mock_analyze_email_for_information(client, user_request, email_body)
        self.assertTrue(result)

    @patch("utils.ai_utils.summarize_information")
    def test_summarize_information(self, mock_summarize_information):
        mock_summarize_information.return_value = "Summary"
        result = mock_summarize_information()
        self.assertEqual(result, "Summary")

    @patch("utils.ai_utils.get_next_step")
    def test_get_next_step(self, mock_get_next_step):
        summary = "Test summary"
        mock_get_next_step.return_value = "Next step"
        result = mock_get_next_step(summary)
        self.assertEqual(result, "Next step")


import unittest
from utils.email_utils import send_email, receive_emails


class TestEmailUtils(unittest.TestCase):
    @patch("smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        sender_email = "sender@example.com"
        sender_password = "password"
        recipient_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test Body"

        date_sent = send_email(
            sender_email, sender_password, recipient_email, subject, body
        )
        self.assertIsNotNone(date_sent)

    @patch("imaplib.IMAP4_SSL")
    def test_receive_emails(self, mock_imap):
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        email_user = "user@example.com"
        email_app_password = "password"

        mock_mail.search.return_value = ("OK", [b"1 2"])
        mock_mail.fetch.return_value = (
            "OK",
            [(b"1 (RFC822 {3420}", b"raw email content", b")")],
        )
        mock_mail.select.return_value = ("OK", [b"1"])

        emails = receive_emails(email_user, email_app_password)
        self.assertIsInstance(emails, list)


if __name__ == "__main__":
    unittest.main()
