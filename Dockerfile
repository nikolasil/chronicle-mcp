FROM python:3.12-alpine

LABEL maintainer="Nikolas Iliopoulos <iliopoulos.info@gmail.com>"
LABEL description="MCP server for secure local browser history access"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    libstdc++ \
    libc-dev \
    && adduser -D -u 1000 chronicle

COPY pyproject.toml .
COPY chronicle_mcp ./chronicle_mcp

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e . \
    && rm -rf /root/.cache/pip

USER chronicle

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["python", "-m", "chronicle_mcp"]

CMD ["http", "--host", "0.0.0.0", "--port", "8080"]
