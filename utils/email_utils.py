import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, parsedate_to_datetime
from email.header import decode_header


def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        subject = ' '.join(subject.split())

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg.attach(MIMEText(body, "plain"))

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
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_app_password)
        mail.select("inbox")

        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        emails = []
        for i in range(min(len(mail_ids), max_emails)):
            latest_email_id = mail_ids[-(i + 1)]
            status, data = mail.fetch(latest_email_id, "(RFC822)")

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and "attachment" not in part.get(
                        "Content-Disposition", ""
                    ):
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            date = parsedate_to_datetime(msg["Date"])
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
