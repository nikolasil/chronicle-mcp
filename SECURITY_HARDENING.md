# Security Hardening Guide

## Table of Contents

1. [Overview](#overview)
2. [Environment Security](#environment-security)
3. [Network Security](#network-security)
4. [Data Protection](#data-protection)
5. [Access Control](#access-control)
6. [Monitoring and Auditing](#monitoring-and-auditing)
7. [Production Deployment](#production-deployment)

---

## Overview

ChronicleMCP is designed with security in mind, but proper configuration is essential for safe operation. This guide covers best practices for deploying ChronicleMCP in production environments.

---

## Environment Security

### Environment Variables

Never commit sensitive data to version control.

```bash
# Use environment variables for secrets
export CHRONICLE_API_KEY="your-api-key-here"
export SENTRY_DSN="https://your-sentry-dsn"

# Use .env files (add to .gitignore)
echo ".env" >> .gitignore
```

### Secrets Management

```toml
# config.toml - Never commit this file!
[security]
api_key = "${CHRONICLE_API_KEY}"
```

### Container Security

```dockerfile
# Use non-root user
FROM python:3.11-slim
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser
```

---

## Network Security

### Binding to localhost

By default, ChronicleMCP binds to `127.0.0.1` for security.

```bash
# Only bind to localhost
chronicle-mcp serve --host 127.0.0.1 --port 8080
```

### TLS/HTTPS

For production, use a reverse proxy with TLS.

```nginx
# nginx.conf
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

### Firewall Rules

```bash
# Allow only local access
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -j DROP
```

---

## Data Protection

### URL Sanitization

ChronicleMCP automatically removes sensitive query parameters.

```python
# These parameters are automatically removed:
SENSITIVE_PARAMS = {
    "token", "session", "key", "password", "auth", "sid",
    "access_token", "api_key", "apikey", "api-secret",
    "secret", "api_token", "apitoken", "bearer", "jwt",
    "csrf", "xsrf", "nonce", "salt", "hash"
}
```

### Custom Sensitive Parameters

```python
# In config.toml
[security]
custom_sensitive_params = ["my_secret", "private_token"]
```

### Temporary Files

History databases are copied to temporary files that are automatically cleaned up.

```python
import tempfile
import os

# Files are created in system temp directory
# with restricted permissions (0o600)
temp_file = tempfile.NamedTemporaryFile(delete=True)
```

---

## Access Control

### API Keys

Implement API key authentication for HTTP endpoints.

```python
# Middleware for API key validation
from fastapi import Request, HTTPException

async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != os.getenv("CHRONICLE_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.route("/api/search")
@limiter.limit("10/minute")
async def search():
    pass
```

### IP Allowlisting

```python
ALLOWED_IPS = {"127.0.0.1", "192.168.1.100"}

async def check_ip(request):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="IP not allowed")
```

---

## Monitoring and Auditing

### Structured Logging

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_entry)
```

### Audit Log

```python
AUDIT_LOG = []

def log_audit_event(event_type: str, details: dict):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "details": details,
    }
    AUDIT_LOG.append(entry)
```

### Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('chronicle_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('chronicle_request_duration_seconds', 'Request latency')

@app.route("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

---

## Production Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  chronicle-mcp:
    image: ghcr.io/nikolasil/chronicle-mcp:latest
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      - CHRONICLE_LOG_LEVEL=INFO
    volumes:
      - chronicle-data:/data
    restart: unless-stopped

volumes:
  chronicle-data:
```

### Kubernetes

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: chronicle-mcp-config
data:
  CHRONICLE_HOST: "0.0.0.0"
  CHRONICLE_PORT: "8080"
  CHRONICLE_LOG_LEVEL: "INFO"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chronicle-mcp
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: chronicle-mcp
        image: ghcr.io/nikolasil/chronicle-mcp:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: chronicle-mcp-config
```

### Health Checks

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.get("/ready")
async def ready():
    return {"status": "ready"}
```

### Graceful Shutdown

```python
import signal
import sys

def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

---

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Enable API key authentication
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets
- [ ] Bind to localhost or internal network
- [ ] Enable structured logging
- [ ] Set up audit logging
- [ ] Configure health checks
- [ ] Use non-root container user
- [ ] Keep dependencies updated
- [ ] Run security audits regularly
