from app.core.config import settings
from app.email.base_template import email_html

WELCOME_SUBJECT = f"Welcome to {settings.APP_NAME}"

def welcome_html(email: str) -> str:
    return email_html(
        title="Welcome",
        recipient=email,
        paragraphs=["Thanks for signing up."],
    )