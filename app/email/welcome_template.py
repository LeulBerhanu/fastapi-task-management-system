from html import escape
from app.core.config import settings

WELCOME_SUBJECT = f"Welcome to {settings.APP_NAME}"

def welcome_html(email: str) -> str:
    safe_email = escape(email)
    return f"""
    <!DOCTYPE html>
    <html>
      <body>
        <h1>Welcome</h1>
        <p>Thanks for signing up, {safe_email}.</p>
      </body>
    </html>
    """