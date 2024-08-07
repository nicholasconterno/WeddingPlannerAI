import unittest
from unittest.mock import patch, MagicMock
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parsedate_to_datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.email_utils import send_email, receive_emails


class TestEmailUtils(unittest.TestCase):
    @patch("smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
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
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(sender_email, sender_password)

        # Generate the expected email content
        expected_msg = MIMEMultipart()
        expected_msg["From"] = sender_email
        expected_msg["To"] = recipient_email
        expected_msg["Subject"] = subject
        expected_msg["Date"] = date_sent
        expected_msg.attach(MIMEText(body, "plain"))

        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args[0]
        self.assertEqual(call_args[0], sender_email)
        self.assertEqual(call_args[1], recipient_email)
        self.assertIn("Test Body", call_args[2])

        mock_server.quit.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_authentication_error(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(
            535, b"auth failed"
        )
        mock_smtp.return_value = mock_server

        sender_email = "sender@example.com"
        sender_password = "wrong_password"
        recipient_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test Body"

        date_sent = send_email(
            sender_email, sender_password, recipient_email, subject, body
        )

        self.assertIsNone(date_sent)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(sender_email, sender_password)

    @patch("imaplib.IMAP4_SSL")
    def test_receive_emails_authentication_error(self, mock_imap):
        mock_mail = MagicMock()
        mock_mail.login.side_effect = imaplib.IMAP4.error("auth failed")
        mock_imap.return_value = mock_mail

        email_user = "user@example.com"
        email_app_password = "wrong_password"

        emails = receive_emails(email_user, email_app_password)

        self.assertEqual(len(emails), 0)
        mock_mail.login.assert_called_once_with(email_user, email_app_password)


if __name__ == "__main__":
    unittest.main()
