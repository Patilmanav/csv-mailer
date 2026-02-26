from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import pandas as pd
import io
import os
import re
from dotenv import load_dotenv
from app.email_utils import send_emails, html_to_plaintext
from app.schemas import EmailConfig
from app.builtin_templates.templates import TEMPLATES

load_dotenv()

app = FastAPI(title="CSV Mailer")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_smtp_config_from_env() -> dict:
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing SMTP env vars: {', '.join(missing)}. Check your .env file.",
        )
    return {
        "smtp_host": os.getenv("SMTP_HOST"),
        "smtp_port": int(os.getenv("SMTP_PORT")),
        "smtp_user": os.getenv("SMTP_USER"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
        "use_tls": os.getenv("USE_TLS", "true").lower() == "true",
    }


# ── Pages ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── API: built-in templates ────────────────────────────────────────────────

@app.get("/api/templates")
async def list_templates():
    return [
        {"id": k, "name": v["name"], "description": v["description"]}
        for k, v in TEMPLATES.items()
    ]


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    if template_id not in TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found.")
    t = TEMPLATES[template_id]
    return {
        "id": template_id,
        "name": t["name"],
        "subject": t["subject"],
        "html": t["html"],
        "plaintext": t["plaintext"],
    }


# ── API: preview CSV ───────────────────────────────────────────────────────

@app.post("/preview-csv")
async def preview_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    email_columns = [
        col for col in df.columns
        if df[col].dropna().astype(str).str.contains("@").any()
    ]
    return {
        "columns": list(df.columns),
        "email_columns": email_columns,
        "preview": df.head(5).fillna("").to_dict(orient="records"),
        "total_rows": len(df),
        "filename": file.filename,
    }


# ── API: render preview with first CSV row ─────────────────────────────────

@app.post("/api/preview-render")
async def preview_render(
    file: UploadFile = File(...),
    email_column: str = Form(...),
    html_body: str = Form(...),
    plain_body: str = Form(""),
    subject: str = Form(""),
):
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    row = df.iloc[0].to_dict() if not df.empty else {}

    def render(t: str) -> str:
        for k, v in row.items():
            t = t.replace(f"{{{{{k}}}}}", str(v) if v is not None else "")
        return t

    return {
        "html":    render(html_body),
        "plain":   render(plain_body),
        "subject": render(subject),
        "row":     {k: str(v) for k, v in row.items()},
    }


# ── API: send emails ───────────────────────────────────────────────────────

@app.post("/send-emails")
async def send_emails_endpoint(
    file: UploadFile = File(...),
    email_column: str = Form(...),
    subject: str = Form(...),
    html_body: str = Form(...),
    plain_body: str = Form(""),
    cc: str = Form(""),
    attachments: Optional[List[UploadFile]] = File(None),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    if email_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{email_column}' not found.")

    emails = df[email_column].dropna().astype(str).str.strip().tolist()
    valid_emails = [e for e in emails if "@" in e and "." in e.split("@")[-1]]
    if not valid_emails:
        raise HTTPException(status_code=400, detail="No valid email addresses found.")

    # Auto-generate plain text from HTML if not provided
    if not plain_body.strip():
        plain_body = html_to_plaintext(html_body)

    cc_list = [e.strip() for e in cc.split(",") if e.strip() and "@" in e.strip()]

    attachment_data = []
    if attachments:
        for att in attachments:
            if att.filename:
                attachment_data.append({"filename": att.filename, "data": await att.read()})

    smtp = get_smtp_config_from_env()
    config = EmailConfig(
        smtp_host=smtp["smtp_host"],
        smtp_port=smtp["smtp_port"],
        smtp_user=smtp["smtp_user"],
        smtp_password=smtp["smtp_password"],
        use_tls=smtp["use_tls"],
        subject=subject,
        html_body=html_body,
        plain_body=plain_body,
        cc=cc_list,
    )

    results = await send_emails(valid_emails, config, df, email_column, attachment_data)

    return {
        "total": len(valid_emails),
        "sent": results["sent"],
        "failed": results["failed"],
        "errors": results["errors"],
        "cc_count": len(cc_list),
        "attachment_count": len(attachment_data),
    }
