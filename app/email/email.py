from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from app.core.config import settings
from app.email.welcome_template import WELCOME_SUBJECT, welcome_html

config_smtp = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=settings.EMAIL_STARTTLS,
    MAIL_SSL_TLS=settings.EMAIL_SSL_TLS,
)

fm = FastMail(config_smtp)

async def send_welcome_email(email: EmailStr) -> None:
    message = MessageSchema(
        subject=WELCOME_SUBJECT,
        recipients=[email],
        body=welcome_html(email),
        subtype="html",
    )
    await fm.send_message(message)