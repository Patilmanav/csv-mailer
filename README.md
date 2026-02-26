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
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env with your SMTP credentials
nano .env

# 3. Build and run
docker-compose up --build

# 4. Open browser
http://localhost:8000
```

For production deployment, see [DOCKER.md](DOCKER.md)

### Option 2: Local Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and configure .env
cp .env.example .env
nano .env

# 3. Run the server
uvicorn app.main:app --reload

# 4. Open browser
http://localhost:8000
```

---

## 🔧 How It Works

1. **Upload a CSV** — drag & drop or click to browse.
2. **Auto-detection** — email columns are highlighted automatically.
3. **Preview** — see the first 5 rows of your data.
4. **Compose** — write subject & body. Use `{{column_name}}` for personalization (e.g. `{{name}}`, `{{company}}`).
5. **SMTP settings** — configured via `.env` file.
6. **Send** — results show sent/failed counts.

---

## 📧 Gmail Setup

1. Enable **2-Step Verification** on your Google account.
2. Generate an **App Password** at: https://myaccount.google.com/apppasswords
3. Use these settings in `.env`:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password-here
   USE_TLS=true
   ```

---

## 🐳 Docker Commands

```bash
# Development
docker-compose up -d              # Start in background
docker-compose logs -f            # View logs
docker-compose down               # Stop

# Production
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down

# Testing
bash test-docker.sh               # Run automated tests
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the frontend UI |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/api/templates` | List built-in email templates |
| `GET` | `/api/templates/{id}` | Get specific template |
| `POST` | `/preview-csv` | Parses CSV, returns columns & preview |
| `POST` | `/api/preview-render` | Render template with first CSV row |
| `POST` | `/send-emails` | Sends emails to all addresses in chosen column |

---

## 🔍 Troubleshooting

### 404 Errors in Production

If you're getting 404 errors when accessing the app:

1. **Check container status:**
   ```bash
   docker-compose ps
   ```

2. **View logs:**
   ```bash
   docker-compose logs csv-mailer
   ```

3. **Test health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **If behind reverse proxy**, ensure proper headers are forwarded (see [DOCKER.md](DOCKER.md))

### SMTP Connection Issues

- Verify credentials in `.env` file
- Check firewall allows outbound connections on SMTP port
- For Gmail, ensure App Password is used (not regular password)

---

## 📝 License

MIT
