from dataclasses import dataclass, field
from typing import List, Optional, Union
from src.status import Status
from src.email_address import EmailAddress
from src.utils import clean_text

@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: Union[EmailAddress, List[EmailAddress]]
    date: Optional[str] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

    def get_recipients_str(self) -> str:
        return ', '.join(str(r) for r in self.recipients)

    def clean_data(self) -> 'Email':
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n: int = 10) -> 'Email':
        if self.body:
            self.short_body = (self.body[:n] + "...") if len(self.body) > n else self.body
        return self

    def is_valid_fields(self) -> bool:
        return bool(self.subject and self.body and self.sender and self.recipients)

    def prepare(self) -> 'Email':
        self.clean_data()
        if self.is_valid_fields():
            self.status = Status.READY
        else:
            self.status = Status.INVALID
        return self

    def __str__(self) -> str:
        recipients_str = self.get_recipients_str()
        content = self.short_body or self.body
        return (f"""Status: {self.status}
    Кому: {recipients_str}
    От: {self.sender.masked}
    Тема: {self.subject}, дата {self.date}
    {content}""")

    def __repr__(self) -> str:
        return self.__str__()
