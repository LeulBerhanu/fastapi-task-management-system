from uuid import UUID

from app.core.config import settings
from app.email.base_template import email_html


TASK_EXPORT_SUBJECT = f"Your {settings.APP_NAME} task export"


def task_export_html(email: str, workspace_id: UUID) -> str:
    return email_html(
        title="Your task export is ready",
        recipient=email,
        paragraphs=[
            f"The CSV export for workspace {workspace_id} is attached to this email."
        ],
    )
