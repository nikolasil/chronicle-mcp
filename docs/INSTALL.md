# ChronicleMCP Installation Guide

This guide covers all installation methods for ChronicleMCP.

## Table of Contents

1. [pip (Recommended)](#pip-recommended)
2. [pipx](#pipx)
3. [Docker](#docker)
4. [From Source](#from-source)
5. [Homebrew (macOS)](#homebrew-macos)
6. [Scoop (Windows)](#scoop-windows)
7. [Verifying Installation](#verifying-installation)
8. [Troubleshooting](#troubleshooting)

---

## pip (Recommended)

Best for most users.

### Install

```bash
pip install chronicle-mcp
```

### Upgrade

```bash
pip install --upgrade chronicle-mcp
```

### Uninstall

```bash
pip uninstall chronicle-mcp
```

### Requirements

- Python 3.10 or higher
- pip

---

## pipx

Best for isolated, command-line focused installations.

### Install pipx

```bash
# macOS with Homebrew
brew install pipx

# Linux
pip install --user pipx

# Windows
pip install pipx
```

### Install ChronicleMCP

```bash
pipx install chronicle-mcp
```

### Upgrade

```bash
pipx upgrade chronicle-mcp
```

### Uninstall

```bash
pipx uninstall chronicle-mcp
```

---

## Docker

Best for server deployments or containerized environments.

### Prerequisites

- Docker installed
- Docker daemon running

### Pull Image

```bash
# Latest version
docker pull ghcr.io/nikolasil/chronicle-mcp:latest

# Specific version
docker pull ghcr.io/nikolasil/chronicle-mcp:v1.1.0
```

### Run Container

```bash
# Basic run (foreground)
docker run -p 8080:8080 ghcr.io/nikolasil/chronicle-mcp:latest

# Run in background
docker run -d -p 8080:8080 --name chronicle-mcp ghcr.io/nikolasil/chronicle-mcp:latest

# With custom port
docker run -d -p 9000:8080 --name chronicle-mcp ghcr.io/nikolasil/chronicle-mcp:latest http --port 8080
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  chronicle-mcp:
    image: ghcr.io/nikolasil/chronicle-mcp:latest
    ports:
      - "8080:8080"
    restart: unless-stopped
```

Start the service:

```bash
docker-compose up -d
```

### Build Local Image

```bash
docker build -t chronicle-mcp:local .
docker run -p 8080:8080 chronicle-mcp:local
```

### Volume Mounts

If you need to access browser history from the host:

```bash
# macOS
docker run -p 8080:8080 \
  -v "/Users/$USER/Library/Application Support/Google/Chrome/Default/History:/chrome/History:ro" \
  ghcr.io/nikolasil/chronicle-mcp:latest
```

---

## From Source

Best for developers or contributors.

### Prerequisites

- Python 3.10+
- git

### Clone Repository

```bash
git clone https://github.com/nikolasil/chronicle-mcp.git
cd chronicle-mcp
```

### Install in Development Mode

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Install Without Dev Dependencies

```bash
pip install .
```

### Run After Installation

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run CLI
chronicle-mcp --help
```

---

## Homebrew (macOS)

### Prerequisites

- Homebrew installed

### Install

```bash
# Add the tap
brew tap nikolasil/chronicle-mcp

# Install
brew install chronicle-mcp
```

### Upgrade

```bash
brew update
brew upgrade chronicle-mcp
```

### Uninstall

```bash
brew uninstall chronicle-mcp
brew untap nikolasil/chronicle-mcp
```

---

## Scoop (Windows)

### Prerequisites

- Scoop installed

### Install

```bash
# Add the bucket
scoop bucket add nikolasil https://github.com/nikolasil/scoop-bucket

# Install
scoop install chronicle-mcp
```

### Upgrade

```bash
scoop update chronicle-mcp
```

### Uninstall

```bash
scoop uninstall chronicle-mcp
```

---

## Winget (Windows)

### Prerequisites

- Windows Package Manager (winget) installed

### Install

```bash
winget install nikolasil.chronicle-mcp
```

### Upgrade

```bash
winget upgrade nikolasil.chronicle-mcp
```

### Uninstall

```bash
winget uninstall nikolasil.chronicle-mcp
```

---

## Verifying Installation

### Check Version

```bash
chronicle-mcp version
```

Expected output:
```
ChronicleMCP version: 1.1.0
```

### Check Available Browsers

```bash
chronicle-mcp list-browsers
```

Expected output:
```
Available browsers:
  - chrome
  - edge
```

### Run a Quick Test

```bash
chronicle-mcp http --port 8080 &
sleep 2
curl http://localhost:8080/health
pkill -f chronicle-mcp
```

---

## Troubleshooting

### "command not found: chronicle-mcp"

**Cause:** PATH not configured

**Solution:**
- Ensure pip's bin directory is in PATH
- Or use `python -m chronicle_mcp` instead

### Python Version Too Old

**Cause:** Python 3.9 or earlier

**Solution:**
```bash
# Check version
python --version

# Install Python 3.10+ from python.org
```

### Permission Denied

**Cause:** Insufficient permissions

**Solution:**
```bash
# Install for user only
pip install --user chronicle-mcp

# Or use sudo (not recommended)
sudo pip install chronicle-mcp
```

### Docker Permission Denied

**Cause:** User not in docker group

**Solution:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Port Already in Use

**Cause:** Another service using port 8080

**Solution:**
```bash
# Use different port
chronicle-mcp http --port 9000
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|----------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 512 MB | 1 GB |
| Disk | 10 MB | 50 MB |
| OS | Windows/macOS/Linux | Latest versions |

---

## See Also

- [CLI Reference](CLI.md)
- [API Documentation](API.md)
- [Architecture](ARCHITECTURE.md)
- [GitHub Repository](https://github.com/nikolasil/chronicle-mcp)
