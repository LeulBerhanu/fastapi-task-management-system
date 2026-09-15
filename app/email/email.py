import csv
from io import BytesIO, StringIO
from uuid import UUID

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from starlette.datastructures import Headers, UploadFile
from sqlmodel import select

from app.core.config import settings
from app.db.session import engine
from app.email.task_export_template import TASK_EXPORT_SUBJECT, task_export_html
from app.email.welcome_template import WELCOME_SUBJECT, welcome_html
from app.models import Task, User
from sqlmodel.ext.asyncio.session import AsyncSession

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

async def send_tasks_export_email(email: EmailStr, workspace_id: UUID) -> None:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        result = await session.exec(
            select(
                Task.title,
                Task.description,
                Task.status,
                User.email,
                Task.created_at,
                Task.updated_at,
            )
            .outerjoin(User, Task.assignee_id == User.id)
            .where(Task.workspace_id == workspace_id)
            .order_by(Task.created_at.desc())
        )
        tasks = result.all()

    csv_buffer = StringIO(newline="")
    writer = csv.writer(csv_buffer)
    writer.writerow(
        [
            "title",
            "description",
            "status",
            "assignee_email",
            "created_at",
            "updated_at",
        ]
    )
    for task in tasks:
        writer.writerow(
            [
                task[0],
                task[1] or "",
                task[2].value,
                task[3] or "",
                task[4].isoformat(),
                task[5].isoformat(),
            ]
        )

    attachment = UploadFile(
        file=BytesIO(csv_buffer.getvalue().encode("utf-8-sig")),
        filename=f"workspace-{workspace_id}-tasks.csv",
        headers=Headers({"content-type": "text/csv; charset=utf-8"}),
    )
    message = MessageSchema(
        subject=TASK_EXPORT_SUBJECT,
        recipients=[email],
        body=task_export_html(email, workspace_id),
        subtype="html",
        attachments=[attachment],
    )
    await fm.send_message(message)