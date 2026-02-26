# 📬 CSV Mailer

A FastAPI web app that lets you upload a CSV, auto-detect email columns, compose a personalized message, and send it to all recipients directly from the browser.

---

## 📁 Project Structure

```
csv-mailer/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI routes
│   ├── email_utils.py   # SMTP sending logic
│   └── schemas.py       # Pydantic models
├── templates/
│   └── index.html       # Frontend UI (single-page)
├── uploads/             # Temp storage (auto-created)
├── sample.csv           # Example CSV for testing
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn app.main:app --reload
```

### 3. Open in browser

```
http://localhost:8000
```

---

## 🔧 How It Works

1. **Upload a CSV** — drag & drop or click to browse.
2. **Auto-detection** — email columns are highlighted automatically.
3. **Preview** — see the first 5 rows of your data.
4. **Compose** — write subject & body. Use `{{column_name}}` for personalization (e.g. `{{name}}`, `{{company}}`).
5. **SMTP settings** — enter your mail server credentials.
6. **Send** — results show sent/failed counts.

---

## 📧 Gmail Setup

1. Enable **2-Step Verification** on your Google account.
2. Generate an **App Password** at: https://myaccount.google.com/apppasswords
3. Use these settings:
   - SMTP Host: `smtp.gmail.com`
   - SMTP Port: `587`
   - Security: `STARTTLS`
   - Password: your App Password (not your Google password)

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the frontend UI |
| `POST` | `/preview-csv` | Parses CSV, returns columns & preview |
| `POST` | `/send-emails` | Sends emails to all addresses in chosen column |
