from html import escape
from collections.abc import Sequence

from app.core.config import settings


BRAND_COLOR = "#059669"
PAGE_BACKGROUND = "#f3f4f6"
CARD_BACKGROUND = "#ffffff"
BORDER_COLOR = "#e5e7eb"
TEXT_COLOR = "#1f2937"
MUTED_TEXT_COLOR = "#6b7280"
FONT_FAMILY = "Arial, Helvetica, sans-serif"


def email_html(
    title: str,
    recipient: str,
    paragraphs: Sequence[str],
) -> str:
    safe_title = escape(title)
    safe_recipient = escape(recipient)
    safe_app_name = escape(settings.APP_NAME)
    content = "\n".join(
        f'<p style="margin: 0 0 16px; font-size: 15px; line-height: 24px;">{escape(paragraph)}</p>'
        for paragraph in paragraphs
    )

    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{safe_title}</title>
      </head>
      <body style="margin: 0; padding: 0; background-color: {PAGE_BACKGROUND}; font-family: {FONT_FAMILY}; color: {TEXT_COLOR};">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: {PAGE_BACKGROUND};">
          <tr>
            <td align="center" style="padding: 32px 16px;">
              <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 600px; background-color: {CARD_BACKGROUND}; border: 1px solid {BORDER_COLOR}; border-radius: 10px; overflow: hidden;">
                <tr>
                  <td style="background-color: {BRAND_COLOR}; padding: 24px 32px;">
                    <p style="margin: 0; color: #ffffff; font-size: 18px; font-weight: bold; letter-spacing: 0.3px;">{safe_app_name}</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding: 32px;">
                    <h1 style="margin: 0 0 20px; font-size: 22px; line-height: 30px; font-weight: bold;">{safe_title}</h1>
                    <p style="margin: 0 0 16px; font-size: 15px; line-height: 24px;">Hello {safe_recipient},</p>
                    {content}
                  </td>
                </tr>
                <tr>
                  <td style="border-top: 1px solid {BORDER_COLOR}; padding: 20px 32px;">
                    <p style="margin: 0; font-size: 13px; line-height: 20px; color: {MUTED_TEXT_COLOR};">
                      This is an automated message from {safe_app_name}.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """
