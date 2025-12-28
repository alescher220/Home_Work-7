from datetime import date
from typing import List
import copy
from src.email import Email
from src.status import Status

from src.status import Status
from copy import deepcopy

class EmailService:
    def send_email(self, email: Email) -> list[Email]:
        # 1. Письмо не готово – сразу FAILED
        if email.status != Status.READY:
            return [
                Email(
                    subject=email.subject,
                    body=email.body,
                    sender=email.sender,
                    recipients=email.recipients,
                    status=Status.FAILED,
                )
            ]

        # 2. Главная ветка – рассылаем каждому получателю
        sent_messages = []
        for rcpt in email.recipients:
            copy = deepcopy(email)
            copy.recipients = [rcpt]          # по одному адресату
            copy.status = Status.SENT
            copy.date = date.today().isoformat()
            sent_messages.append(copy)

        return sent_messages   # ← важно: всегда возвращаем список




class LoggingEmailService(EmailService):
    def send_email(self, email: Email) -> List[Email]:
        sent_emails = super().send_email(email)
        with open("send.log", "a", encoding="utf-8") as log_file:
            for email_copy in sent_emails:
                log_entry = (
                    f"[{email_copy.date}] "
                    f"From: {email_copy.sender.masked} "
                    f"To: {email_copy.recipients[0]} "
                    f"Subject: '{email_copy.subject}' "
                    f"Status: {email_copy.status}\n"
                )
                log_file.write(log_entry)

        return sent_emails
