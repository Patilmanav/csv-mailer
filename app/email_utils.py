import smtplib
import asyncio
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
import pandas as pd
from app.schemas import EmailConfig


def render_template(template: str, row: dict) -> str:
    """Replace {{column_name}} placeholders with row values."""
    for key, value in row.items():
        template = template.replace(f"{{{{{key}}}}}", str(value) if value is not None else "")
    return template


def html_to_plaintext(html: str) -> str:
    """Very lightweight HTML → plain text strip for fallback generation."""
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def send_single_email(
    to_email: str,
    config: EmailConfig,
    row_data: dict,
    attachments: List[dict],  # [{"filename": str, "data": bytes}]
) -> None:
    # Render placeholders
    html_rendered   = render_template(config.html_body,   row_data)
    plain_rendered  = render_template(config.plain_body,  row_data)
    subject_rendered = render_template(config.subject,    row_data)

    # Outer wrapper: mixed (for attachments)
    outer = MIMEMultipart("mixed")
    outer["Subject"] = subject_rendered
    outer["From"]    = config.smtp_user
    outer["To"]      = to_email
    if config.cc:
        outer["Cc"] = ", ".join(config.cc)

    # Alternative part: plain + html
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain_rendered, "plain", "utf-8"))
    alt.attach(MIMEText(html_rendered,  "html",  "utf-8"))
    outer.attach(alt)

    # Attachments
    for att in attachments:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(att["data"])
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{att["filename"]}"')
        outer.attach(part)

    all_recipients = [to_email] + config.cc

    if config.use_tls:
        server = smtplib.SMTP(config.smtp_host, config.smtp_port)
        server.starttls()
    else:
        server = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)

    server.login(config.smtp_user, config.smtp_password)
    server.sendmail(config.smtp_user, all_recipients, outer.as_string())
    server.quit()


async def send_emails(
    emails: List[str],
    config: EmailConfig,
    df: pd.DataFrame,
    email_column: str,
    attachments: List[dict],
) -> dict:
    sent = 0
    failed = 0
    errors = []

    for email in emails:
        matching = df[df[email_column].astype(str).str.strip() == email]
        row_data = matching.iloc[0].to_dict() if not matching.empty else {}

        try:
            await asyncio.to_thread(send_single_email, email, config, row_data, attachments)
            sent += 1
        except Exception as e:
            failed += 1
            errors.append({"email": email, "error": str(e)})

    return {"sent": sent, "failed": failed, "errors": errors}
