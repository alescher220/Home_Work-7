from datetime import date
from typing import List
import copy
from src.email import Email
from src.status import Status

class EmailService:
    def add_send_date(self) -> str:
        return date.today().isoformat()

    def send_email(self, email: Email) -> List[Email]:
        sent_emails = []

        # Подготовка письма
        prepared_email = copy.deepcopy(email)
        prepared_email.prepare()

        # Если нет получателей — возвращаем пустой список
        if not prepared_email.recipients:
            return []

        send_date = self.add_send_date()

        for recipient in prepared_email.recipients:
            # Создаём копию для каждого получателя
            sent_email = copy.deepcopy(prepared_email)
            sent_email.recipients = [recipient]
            sent_email.date = send_date

            # Устанавливаем статус
            if sent_email.status == Status.READY:
                sent_email.status = Status.SENT
            else:
                sent_email.status = Status.FAILED

            sent_emails.append(sent_email)

        return sent_emails



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
