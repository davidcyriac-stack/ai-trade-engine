from typing import Dict
from email.message import EmailMessage
import smtplib

class NotificationService:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str, from_address: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address

    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        if not self.smtp_host or not self.from_address or not to_address:
            return False

        message = EmailMessage()
        message["From"] = self.from_address
        message["To"] = to_address
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)
        return True

    def create_in_app_notification(self, channel: str, subject: str, body: str) -> Dict[str, str]:
        return {"channel": channel, "subject": subject, "body": body}
