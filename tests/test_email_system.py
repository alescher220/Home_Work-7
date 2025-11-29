import pytest
from datetime import date
from src.email_address import EmailAddress
from src.email import Email
from src.service import EmailService, LoggingEmailService
from src.status import Status



def test_email_address_valid():
    addr = EmailAddress("USER@GMAIL.COM")
    assert addr.address == "user@gmail.com"
    assert addr.masked == "us***@gmail.com"



def test_email_address_invalid():
    with pytest.raises(ValueError):
        EmailAddress("not-an-email")



def test_email_prepare_sets_ready():
    email = Email(
        subject="Hello",
        body="World",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    email.prepare()
    assert email.status == Status.READY



def test_email_prepare_sets_invalid():
    email = Email(
        subject="",
        body="",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    email.prepare()
    assert email.status == Status.INVALID



def test_recipients_auto_list():
    email = Email(
        subject="Hi",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    assert isinstance(email.recipients, list)
    assert len(email.recipients) == 1
    assert email.recipients[0].address == "b@b.com"



def test_send_email_single_recipient():
    email = Email(
        subject="Hello",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
        status=Status.READY,
    )

    service = EmailService()
    results = service.send_email(email)

    assert len(results) == 1
    sent = results[0]
    assert sent.status == Status.SENT
    assert sent.recipients[0].address == "b@b.com"
    assert sent.date == date.today().isoformat()




def test_send_email_multiple_recipients():
    email = Email(
        subject="Hello",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=[
            EmailAddress("b@b.com"),
            EmailAddress("c@c.com"),
            EmailAddress("d@d.com"),
        ],
        status=Status.READY,
    )

    service = EmailService()
    results = service.send_email(email)

    assert len(results) == 3
    assert all(msg.status == Status.SENT for msg in results)
    recipient_addresses = {msg.recipients[0].address for msg in results}
    assert recipient_addresses == {"b@b.com", "c@c.com", "d@d.com"}
    assert all(msg.date == date.today().isoformat() for msg in results)




def test_send_email_failed_if_not_ready():
    email = Email(
        subject="Hello",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=[EmailAddress("b@b.com")],
        status=Status.DRAFT,
    )

    service = EmailService()
    results = service.send_email(email)

    assert len(results) == 1
    assert results[0].status == Status.FAILED




def test_email_address_normalization_and_masking():
    addr = EmailAddress("USER@GMAIL.COM")
    assert addr.address == "user@gmail.com"
    assert addr.masked == "us***@gmail.com"



@pytest.mark.parametrize("invalid", ["abc", "test@mail", "name@domain.xx"])
def test_email_address_invalid_variants(invalid):
    with pytest.raises(ValueError):
        EmailAddress(invalid)



def test_email_prepare_cleans_text_and_sets_ready():
    email = Email(
        subject="  Hello   world  ",
        body=" Test   body\nwith   spaces ",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    email.prepare()
    assert email.status == Status.READY
    assert email.subject == "Hello world"
    assert email.body == "Test body with spaces"



def test_email_prepare_invalid_when_body_missing():
    email = Email(
        subject="Hello",
        body="",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    email.prepare()
    assert email.status == Status.INVALID



def test_add_short_body():
    email = Email(
        subject="Hi",
        body="This text is long",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    email.add_short_body(5)
    assert email.short_body == "This ..."



def test_recipients_auto_wraps_to_list():
    email = Email(
        subject="Hi",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
    )
    assert isinstance(email.recipients, list)
    assert len(email.recipients) == 1
    assert email.recipients[0].address == "b@b.com"



def test_send_email_single_recipient_creates_new_object():
    email = Email(
        subject="Hello",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=EmailAddress("b@b.com"),
        status=Status.READY,
    )

    service = EmailService()
    results = service.send_email(email)

    assert len(results) == 1
    sent = results[0]

    assert sent.status == Status.SENT
    assert sent is not email
    assert sent.recipients[0].address == "b@b.com"
    assert email.date is None
    assert email.recipients is not results[0].recipients
    assert email.recipients[0].address == results[0].recipients[0].address




def test_send_email_failed_if_status_not_ready():
    email = Email(
        subject="Hello",
        body="Msg",
        sender=EmailAddress("a@a.com"),
        recipients=[EmailAddress("b@b.com")],
        status=Status.DRAFT,
    )

    service = EmailService()
    results = service.send_email(email)

    assert len(results) == 1
    assert results[0].status == Status.FAILED



def test_repr_has_expected_format():
    email = Email(
        subject="Hello",
        body="World",
        sender=EmailAddress("a@a.com"),
        recipients=[EmailAddress("b@b.com")],
    ).prepare()

    text = repr(email)

    assert "Status: ready\n" in text
    assert "Кому: b@b.com\n" in text
    assert "От: a***@a.com\n" in text  # исправлено: маска!
    assert "Тема: Hello, дата None\n" in text
    assert "World" in text



@pytest.mark.parametrize("valid", [
    "test@gmail.com",
    "user@mail.ru",
    "a@a.net",
    "USER@GMAIL.COM",
    "  a@a.net  ",
])
def test_email_address_valid_variants(valid):
    addr = EmailAddress(valid)
    assert "@" in addr.address
    assert addr.address == valid.lower().strip()
