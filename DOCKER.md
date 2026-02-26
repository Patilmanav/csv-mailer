# Docker Deployment Guide

## Quick Start

### Development
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production
```bash
# Build and run production setup
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your SMTP credentials:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   USE_TLS=true
   ```

## Access

- Application: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

## Troubleshooting

### 404 Errors in Production

If you're getting 404 errors, check:

1. **Container is running:**
   ```bash
   docker-compose ps
   ```

2. **Check logs for errors:**
   ```bash
   docker-compose logs csv-mailer
   ```

3. **Verify the app is accessible:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **If behind a reverse proxy**, ensure proper headers are forwarded:
   ```nginx
   # Nginx example
   location / {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

### Port Already in Use

If port 8000 is already in use, change it in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

### Permission Issues with Uploads

```bash
# Fix upload directory permissions
chmod 777 uploads
```

## Volumes

- `./uploads` - Persistent storage for uploaded CSV files
- `./templates` - HTML email templates (read-only in production)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SMTP_HOST | SMTP server hostname | - |
| SMTP_PORT | SMTP server port | - |
| SMTP_USER | SMTP username | - |
| SMTP_PASSWORD | SMTP password | - |
| USE_TLS | Use TLS encryption | true |

## Building for Different Architectures

```bash
# For ARM64 (Apple Silicon, Raspberry Pi)
docker buildx build --platform linux/arm64 -t csv-mailer:arm64 .

# For AMD64 (Intel/AMD)
docker buildx build --platform linux/amd64 -t csv-mailer:amd64 .

# Multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t csv-mailer:latest .
```
