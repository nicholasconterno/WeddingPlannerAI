import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, parsedate_to_datetime
from email.header import decode_header


def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Send an email using the SMTP protocol.
    """
    try:
        # Remove any leading or trailing whitespace from the subject
        subject = " ".join(subject.split())
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg.attach(MIMEText(body, "plain"))
        # Send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return msg["Date"]
    except smtplib.SMTPAuthenticationError:
        print(
            "Failed to authenticate with the SMTP server. Check your email and password."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def receive_emails(email_user, email_app_password, max_emails=10):
    """
    Receive emails using the IMAP protocol.
    """
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_app_password)
        mail.select("inbox")
        # Get the email IDs
        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        emails = []
        # Iterate through the email IDs in reverse order
        for i in range(min(len(mail_ids), max_emails)):
            latest_email_id = mail_ids[-(i + 1)]
            status, data = mail.fetch(latest_email_id, "(RFC822)")
            # Parse the email
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            # Decode the subject
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            body = None
            # Get the email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and "attachment" not in part.get(
                        "Content-Disposition", ""
                    ):
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                # If the email is not multipart, get the email body
                body = msg.get_payload(decode=True).decode()
            # Get the email date
            date = parsedate_to_datetime(msg["Date"])
            # Add the email to the list
            emails.append(
                {"from": msg["From"], "subject": subject, "body": body, "date": date}
            )

        mail.logout()
        return emails
    except imaplib.IMAP4.error:
        print(
            "Failed to authenticate with the IMAP server. Check your email and app password."
        )
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
