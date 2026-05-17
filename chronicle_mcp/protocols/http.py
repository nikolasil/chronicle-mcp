"""HTTP/SSE protocol adapter for ChronicleMCP.

This module provides HTTP endpoints using Starlette.
All business logic is delegated to the HistoryService in the core layer.
"""

import contextlib
import contextvars
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from chronicle_mcp.config import get_version, load_config, setup_logging
from chronicle_mcp.core import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    HistoryService,
    PermissionDeniedError,
    ServiceError,
    ValidationError,
)

setup_logging()
logger = logging.getLogger(__name__)

DEFAULT_BROWSER = "chrome"
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        {"error": "Rate limit exceeded", "detail": str(exc.detail)},
        status_code=429,
    )


class RequestMetrics:
    """Thread-safe, async-safe request metrics using ContextVars."""

    def __init__(self, default_browser: str = DEFAULT_BROWSER):
        self._count_token = _request_count.set(0)
        self._latency_token = _request_latency_total.set(0.0)
        self._start_token = _start_time.set(time.time())
        self._default_browser_token = _default_browser.set(default_browser)
        self._histogram_buckets = {
            "search": [],
            "recent": [],
            "count": [],
            "top_domains": [],
            "delete": [],
            "export": [],
            "other": [],
        }

    def increment(self, latency: float, operation: str = "other") -> None:
        _request_count.set(_request_count.get() + 1)
        _request_latency_total.set(_request_latency_total.get() + latency)
        if operation in self._histogram_buckets:
            self._histogram_buckets[operation].append(latency)

    @property
    def request_count(self) -> int:
        return _request_count.get()

    @property
    def total_latency(self) -> float:
        return _request_latency_total.get()

    @property
    def uptime(self) -> float:
        return time.time() - _start_time.get()

    @property
    def default_browser(self) -> str:
        return _default_browser.get()

    def get_histogram_buckets(self) -> dict[str, list[float]]:
        return self._histogram_buckets


_request_count: contextvars.ContextVar[int] = contextvars.ContextVar("request_count", default=0)
_request_latency_total: contextvars.ContextVar[float] = contextvars.ContextVar(
    "request_latency_total", default=0.0
)
_start_time: contextvars.ContextVar[float] = contextvars.ContextVar("start_time")
_default_browser: contextvars.ContextVar[str] = contextvars.ContextVar(
    "default_browser", default=DEFAULT_BROWSER
)
_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="")


def generate_correlation_id() -> str:
    """Generate a unique correlation ID for request tracing."""
    import uuid

    return str(uuid.uuid4())[:16]


def get_correlation_id() -> str:
    """Get the current correlation ID or generate a new one."""
    cid = _correlation_id.get()
    if not cid:
        cid = generate_correlation_id()
        _correlation_id.set(cid)
    return cid


_metrics: contextvars.ContextVar[RequestMetrics] = contextvars.ContextVar(
    "_metrics", default=RequestMetrics()
)


def get_metrics() -> RequestMetrics:
    return _metrics.get()


def get_default_browser() -> str:
    return _default_browser.get()


def _classify_operation(path: str) -> str:
    """Classify request operation type for histogram metrics."""
    if "/search" in path or path == "/api/search":
        return "search"
    elif "/recent" in path:
        return "recent"
    elif "/count" in path:
        return "count"
    elif "/top-domains" in path or "/top_domains" in path:
        return "top_domains"
    elif "/delete" in path:
        return "delete"
    elif "/export" in path:
        return "export"
    return "other"


def error_response(
    message: str, status_code: int = 400, correlation_id: str | None = None
) -> JSONResponse:
    error_id = correlation_id or get_correlation_id()
    return JSONResponse({"error": message, "correlation_id": error_id}, status_code=status_code)


def handle_service_error_http(error: Exception) -> JSONResponse:
    if isinstance(error, ValidationError):
        return error_response(error.message, 400)
    elif isinstance(error, json.JSONDecodeError):
        return error_response("Invalid JSON in request body", 422)
    elif isinstance(error, BrowserNotFoundError):
        return error_response(error.message, 404)
    elif isinstance(error, DatabaseLockedError):
        return error_response(error.message, 423)
    elif isinstance(error, PermissionDeniedError):
        return error_response(error.message, 403)
    elif isinstance(error, DatabaseError):
        return error_response(error.message, 500)
    elif isinstance(error, ServiceError):
        return error_response(error.message, 500)
    else:
        logger.exception("Unexpected error in HTTP endpoint")
        return error_response("An unexpected error occurred", 500)


async def health_check(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "healthy",
            "service": "chronicle-mcp",
            "version": get_version(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


async def ready_check(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_browsers()
        browsers = result["browsers"]
        return JSONResponse(
            {
                "status": "ready" if browsers else "degraded",
                "service": "chronicle-mcp",
                "browsers": browsers,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception as e:
        return JSONResponse(
            {
                "status": "error",
                "service": "chronicle-mcp",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            status_code=500,
        )


async def metrics_check(request: Request) -> JSONResponse:
    metrics = get_metrics()
    count = metrics.request_count
    total_latency = metrics.total_latency
    uptime = metrics.uptime
    avg_latency = total_latency / count if count > 0 else 0

    return JSONResponse(
        {
            "uptime_seconds": uptime,
            "requests_total": count,
            "requests_per_second": count / uptime if uptime > 0 else 0,
            "average_latency_seconds": avg_latency,
            "browsers_available": len(HistoryService.list_available_browsers()["browsers"]),
        }
    )


async def prometheus_metrics(request: Request) -> Response:
    metrics = get_metrics()
    count = metrics.request_count
    total_latency = metrics.total_latency
    uptime = metrics.uptime
    avg_latency = total_latency / count if count > 0 else 0

    try:
        browsers_count = len(HistoryService.list_available_browsers()["browsers"])
    except Exception:
        browsers_count = 0

    histogram_buckets = metrics.get_histogram_buckets()

    def calculate_percentile(values: list[float], percentile: float) -> float:
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        idx = int(len(sorted_vals) * percentile / 100.0)
        return sorted_vals[min(idx, len(sorted_vals) - 1)]

    search_latencies = histogram_buckets.get("search", [])
    recent_latencies = histogram_buckets.get("recent", [])

    metrics_output = f"""# HELP chronicle_uptime_seconds Server uptime in seconds
# TYPE chronicle_uptime_seconds gauge
chronicle_uptime_seconds {uptime:.2f}

# HELP chronicle_requests_total Total number of requests
# TYPE chronicle_requests_total counter
chronicle_requests_total {count}

# HELP chronicle_requests_per_second Requests per second
# TYPE chronicle_requests_per_second gauge
chronicle_requests_per_second {count / uptime if uptime > 0 else 0:.4f}

# HELP chronicle_average_latency_seconds Average request latency
# TYPE chronicle_average_latency_seconds gauge
chronicle_average_latency_seconds {avg_latency:.4f}

# HELP chronicle_browsers_available Number of available browsers
# TYPE chronicle_browsers_available gauge
chronicle_browsers_available {browsers_count}

# HELP chronicle_search_latency_seconds Search operation latency
# TYPE chronicle_search_latency_seconds histogram
chronicle_search_latency_seconds_bucket{{le="0.01"}} {sum(1 for v in search_latencies if v <= 0.01)}
chronicle_search_latency_seconds_bucket{{le="0.05"}} {sum(1 for v in search_latencies if v <= 0.05)}
chronicle_search_latency_seconds_bucket{{le="0.1"}} {sum(1 for v in search_latencies if v <= 0.1)}
chronicle_search_latency_seconds_bucket{{le="0.5"}} {sum(1 for v in search_latencies if v <= 0.5)}
chronicle_search_latency_seconds_bucket{{le="1.0"}} {sum(1 for v in search_latencies if v <= 1.0)}
chronicle_search_latency_seconds_bucket{{le="+Inf"}} {len(search_latencies)}
chronicle_search_latency_seconds_sum {sum(search_latencies):.4f}
chronicle_search_latency_seconds_count {len(search_latencies)}

# HELP chronicle_recent_latency_seconds Recent history operation latency
# TYPE chronicle_recent_latency_seconds histogram
chronicle_recent_latency_seconds_bucket{{le="0.01"}} {sum(1 for v in recent_latencies if v <= 0.01)}
chronicle_recent_latency_seconds_bucket{{le="0.05"}} {sum(1 for v in recent_latencies if v <= 0.05)}
chronicle_recent_latency_seconds_bucket{{le="0.1"}} {sum(1 for v in recent_latencies if v <= 0.1)}
chronicle_recent_latency_seconds_bucket{{le="0.5"}} {sum(1 for v in recent_latencies if v <= 0.5)}
chronicle_recent_latency_seconds_bucket{{le="1.0"}} {sum(1 for v in recent_latencies if v <= 1.0)}
chronicle_recent_latency_seconds_bucket{{le="+Inf"}} {len(recent_latencies)}
chronicle_recent_latency_seconds_sum {sum(recent_latencies):.4f}
chronicle_recent_latency_seconds_count {len(recent_latencies)}
"""
    return Response(content=metrics_output, media_type="text/plain")


async def docs_endpoint(request: Request) -> HTMLResponse:
    docs_html = """
<!DOCTYPE html>
<html>
<head>
    <title>ChronicleMCP API Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css">
    <style>
        body { margin: 0; padding: 0; }
        .topbar { display: none; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function() {
            SwaggerUIBundle({
                url: "/api-docs/openapi.json",
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true
            });
        };
    </script>
</body>
</html>
    """
    return HTMLResponse(content=docs_html)


async def openapi_spec(request: Request) -> JSONResponse:
    version = get_version()
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "ChronicleMCP HTTP API",
            "description": "HTTP REST API for ChronicleMCP - Browser History Context Server",
            "version": version,
            "contact": {"name": "ChronicleMCP Support"},
            "license": {"name": "MIT"},
        },
        "servers": [{"url": "http://localhost:8080", "description": "Local development server"}],
        "paths": {
            "/ready": {
                "get": {
                    "summary": "Health check",
                    "responses": {"200": {"description": "Server is ready"}},
                }
            },
            "/metrics": {
                "get": {
                    "summary": "Get metrics",
                    "responses": {"200": {"description": "Metrics data"}},
                }
            },
            "/metrics/prometheus": {
                "get": {
                    "summary": "Prometheus metrics",
                    "responses": {"200": {"description": "Prometheus format metrics"}},
                }
            },
            "/api/browsers": {
                "get": {
                    "summary": "List available browsers",
                    "responses": {"200": {"description": "List of browsers"}},
                }
            },
            "/api/search": {
                "post": {
                    "summary": "Search browser history",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "limit": {"type": "integer", "default": 20},
                                        "browser": {"type": "string"},
                                        "format_type": {
                                            "type": "string",
                                            "enum": ["json", "markdown", "csv"],
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Search results"}},
                }
            },
            "/api/recent": {
                "post": {
                    "summary": "Get recent history",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "hours": {"type": "integer", "default": 24},
                                        "limit": {"type": "integer", "default": 20},
                                        "browser": {"type": "string"},
                                        "format_type": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Recent history entries"}},
                }
            },
            "/api/count": {
                "post": {
                    "summary": "Count visits to domain",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["domain"],
                                    "properties": {
                                        "domain": {"type": "string"},
                                        "browser": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Visit count"}},
                }
            },
            "/api/top-domains": {
                "post": {
                    "summary": "Get top domains",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "limit": {"type": "integer", "default": 10},
                                        "browser": {"type": "string"},
                                        "format_type": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Top domains list"}},
                }
            },
            "/api/most-visited": {
                "post": {
                    "summary": "Get most visited pages",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "limit": {"type": "integer", "default": 10},
                                        "browser": {"type": "string"},
                                        "format_type": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Most visited pages"}},
                }
            },
            "/api/bookmarks": {
                "get": {
                    "summary": "List bookmarks browsers",
                    "responses": {"200": {"description": "List of browsers with bookmarks"}},
                }
            },
            "/api/bookmarks/query": {
                "post": {
                    "summary": "Search bookmarks",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "limit": {"type": "integer", "default": 20},
                                        "browser": {"type": "string"},
                                        "format_type": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Bookmark results"}},
                }
            },
            "/api/downloads": {
                "get": {
                    "summary": "List downloads browsers",
                    "responses": {"200": {"description": "List of browsers with downloads"}},
                }
            },
            "/api/downloads/query": {
                "post": {
                    "summary": "Search downloads",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "limit": {"type": "integer", "default": 20},
                                        "browser": {"type": "string"},
                                        "format_type": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Download results"}},
                }
            },
        },
    }
    return JSONResponse(content=spec)


class MetricsMiddleware:
    """Starlette middleware for tracking request metrics and correlation IDs."""

    def __init__(self, app: Any):
        self.app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        start = time.time()
        cid = generate_correlation_id()
        _correlation_id.set(cid)

        scope["correlation_id"] = cid

        async def send_wrapper(message: Any) -> None:
            if message["type"] == "http.response.body":
                latency = time.time() - start
                path = scope.get("path", "")
                operation = _classify_operation(path)
                get_metrics().increment(latency, operation)
                logger.info(
                    "Request completed",
                    extra={
                        "extra_data": {
                            "correlation_id": cid,
                            "method": scope.get("method"),
                            "path": path,
                            "status_code": message.get("status", 0),
                            "latency_ms": round(latency * 1000, 2),
                            "operation": operation,
                        }
                    },
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)


async def list_browsers_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_browsers()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("30/minute")
async def search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history(
            query=data.get("query", ""),
            limit=data.get("limit", 5),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("30/minute")
async def recent_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.get_recent_history(
            hours=data.get("hours", 24),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("30/minute")
async def count_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.count_visits(
            domain=data.get("domain", ""), browser=data.get("browser", get_default_browser())
        )
        return JSONResponse(
            {"domain": result["domain"], "browser": result["browser"], "count": result["count"]}
        )
    except Exception as e:
        return handle_service_error_http(e)


async def top_domains_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.list_top_domains(
            limit=data.get("limit", 10),
            browser=data.get("browser", get_default_browser()),
            format_type="json",
        )
        return JSONResponse({"domains": [{"domain": d, "visits": v} for d, v in result["domains"]]})
    except Exception as e:
        return handle_service_error_http(e)


async def search_date_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history_by_date(
            query=data.get("query", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            limit=data.get("limit", 10),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("10/minute")
async def delete_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.delete_history(
            query=data.get("query", ""),
            limit=data.get("limit", 100),
            browser=data.get("browser", get_default_browser()),
            confirm=data.get("confirm", False),
        )

        if result.get("preview"):
            return JSONResponse(
                {
                    "preview": True,
                    "query": result["query"],
                    "count": result["count"],
                    "message": result["message"],
                }
            )
        return JSONResponse(
            {
                "deleted": result["deleted"],
                "query": result["query"],
                "browser": result["browser"],
                "message": result["message"],
            }
        )
    except Exception as e:
        return handle_service_error_http(e)


async def domain_search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_by_domain(
            domain=data.get("domain", ""),
            query=data.get("query"),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains"),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "domain": result["domain"],
                    "results": [
                        {"title": title, "url": url, "timestamp": ts}
                        for title, url, ts in result["results"]
                    ],
                    "count": result["count"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def browser_stats_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_browser_stats(
            browser=data.get("browser", get_default_browser())
        )
        return JSONResponse(result["stats"])
    except Exception as e:
        return handle_service_error_http(e)


async def most_visited_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.get_most_visited_pages(
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type="json",
        )
        return JSONResponse(
            {
                "pages": [
                    {"title": title, "url": url, "visits": visits}
                    for title, url, visits in result["pages"]
                ]
            }
        )
    except Exception as e:
        return handle_service_error_http(e)


async def export_endpoint(request: Request) -> Response:
    try:
        data = await request.json()
        result = HistoryService.export_history(
            format_type=data.get("format_type", "csv"),
            limit=data.get("limit", 1000),
            query=data.get("query"),
            browser=data.get("browser", get_default_browser()),
        )

        content_type = "text/csv" if result["format"] == "csv" else "application/json"
        return Response(content=result["content"], media_type=content_type)
    except Exception as e:
        return handle_service_error_http(e)


async def advanced_search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history_advanced(
            query=data.get("query", ""),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains"),
            sort_by=data.get("sort_by", "date"),
            use_regex=data.get("use_regex", False),
            use_fuzzy=data.get("use_fuzzy", False),
            fuzzy_threshold=data.get("fuzzy_threshold", 0.6),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "query": result["query"],
                    "results": [
                        {"title": title, "url": url, "timestamp": ts}
                        for title, url, ts in result["results"]
                    ],
                    "count": result["count"],
                    "options": result["options"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def sync_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.sync_history(
            source_browser=data.get("source_browser", ""),
            target_browser=data.get("target_browser", ""),
            merge_strategy=data.get("merge_strategy", "latest"),
            dry_run=data.get("dry_run", True),
        )

        return JSONResponse(
            {
                "dry_run": result.get("dry_run", True),
                "source": result["source"],
                "target": result["target"],
                "entries_count": result["entries_count"],
                "merge_strategy": result["merge_strategy"],
                "message": result["message"],
            }
        )
    except Exception as e:
        return handle_service_error_http(e)


async def list_bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_bookmarks()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def list_downloads_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_downloads()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_bookmarks(
            query=data.get("query"),
            limit=data.get("limit", 50),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "bookmarks": [{"title": title, "url": url} for title, url in result["results"]],
                    "count": result["count"],
                    "browser": result["browser"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def downloads_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_downloads(
            query=data.get("query"),
            limit=data.get("limit", 50),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "downloads": [
                        {"filename": fn, "url": url, "timestamp": ts}
                        for fn, url, ts in result["results"]
                    ],
                    "count": result["count"],
                    "browser": result["browser"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def compare_periods_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.compare_time_periods(
            start_date1=data.get("start_date1", ""),
            end_date1=data.get("end_date1", ""),
            start_date2=data.get("start_date2", ""),
            end_date2=data.get("end_date2", ""),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def productivity_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.analyze_productivity(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def suggest_categories_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.suggest_categories(
            browser=data.get("browser", get_default_browser()),
            limit=data.get("limit", 20),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def visualization_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.export_visualization(
            format_type=data.get("format_type", "chart_json"),
            period=data.get("period", "month"),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def insights_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.generate_insights_report(
            period=data.get("period", "week"),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format_type", "markdown"),
        )
        if data.get("format_type") == "json":
            return JSONResponse(result)
        return JSONResponse({"report": result["summary_markdown"]})
    except Exception as e:
        return handle_service_error_http(e)


routes = [
    Route("/health", health_check),
    Route("/ready", ready_check),
    Route("/metrics", metrics_check),
    Route("/metrics/prometheus", prometheus_metrics),
    Route("/docs", docs_endpoint),
    Route("/api-docs/openapi.json", openapi_spec),
    Route("/api/browsers", list_browsers_endpoint),
    Route("/api/search", search_endpoint, methods=["POST"]),
    Route("/api/recent", recent_endpoint, methods=["POST"]),
    Route("/api/count", count_endpoint, methods=["POST"]),
    Route("/api/top-domains", top_domains_endpoint, methods=["POST"]),
    Route("/api/search-date", search_date_endpoint, methods=["POST"]),
    Route("/api/delete", delete_endpoint, methods=["POST"]),
    Route("/api/domain-search", domain_search_endpoint, methods=["POST"]),
    Route("/api/stats", browser_stats_endpoint, methods=["POST"]),
    Route("/api/most-visited", most_visited_endpoint, methods=["POST"]),
    Route("/api/export", export_endpoint, methods=["POST"]),
    Route("/api/advanced-search", advanced_search_endpoint, methods=["POST"]),
    Route("/api/sync", sync_endpoint, methods=["POST"]),
    Route("/api/bookmarks", list_bookmarks_endpoint),
    Route("/api/bookmarks/query", bookmarks_endpoint, methods=["POST"]),
    Route("/api/downloads", list_downloads_endpoint),
    Route("/api/downloads/query", downloads_endpoint, methods=["POST"]),
    Route("/api/compare-periods", compare_periods_endpoint, methods=["POST"]),
    Route("/api/productivity", productivity_endpoint, methods=["POST"]),
    Route("/api/suggest-categories", suggest_categories_endpoint, methods=["POST"]),
    Route("/api/visualization", visualization_endpoint, methods=["POST"]),
    Route("/api/insights", insights_endpoint, methods=["POST"]),
]


def create_middleware(default_browser: str = DEFAULT_BROWSER) -> list[Middleware]:
    config = load_config()
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=config.security.allowed_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(MetricsMiddleware),
    ]


def create_app(default_browser: str = DEFAULT_BROWSER) -> Starlette:
    application = Starlette(
        routes=routes,
        middleware=create_middleware(default_browser),
    )
    application.state.default_browser = default_browser
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    application.add_middleware(SlowAPIMiddleware)
    return application


app = create_app()


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> Any:
    _metrics.set(
        RequestMetrics(default_browser=getattr(app.state, "default_browser", DEFAULT_BROWSER))
    )
    logger.info("ChronicleMCP HTTP server starting...")
    yield
    logger.info("ChronicleMCP HTTP server shutting down...")


def run_http_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    default_browser_: str = DEFAULT_BROWSER,
) -> None:
    import signal
    import sys

    import uvicorn

    def signal_handler(sig: int, frame: object) -> None:
        logger.info(f"Received signal {sig}, shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    application = Starlette(
        routes=routes,
        middleware=create_middleware(default_browser_),
        lifespan=lifespan,
    )
    application.state.default_browser = default_browser_

    config = uvicorn.Config(application, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    import sys

    host = "127.0.0.1"
    port = 8080

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    print(f"Starting ChronicleMCP HTTP server on {host}:{port}")
    run_http_server(host=host, port=port)
