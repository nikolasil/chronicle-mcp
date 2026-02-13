"""HTTP/SSE protocol adapter for ChronicleMCP.

This module provides HTTP endpoints using Starlette.
All business logic is delegated to the HistoryService in the core layer.
"""

import contextlib
import logging
import time
from datetime import datetime, timezone
from typing import Any

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from chronicle_mcp.config import get_version, setup_logging
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

default_browser: str = "chrome"

REQUEST_COUNT = 0
REQUEST_LATENCY_TOTAL = 0.0
START_TIME = time.time()


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Create a standardized error response."""
    return JSONResponse({"error": message}, status_code=status_code)


def handle_service_error_http(error: Exception) -> JSONResponse:
    """Convert service exceptions to HTTP error responses.

    Args:
        error: Exception from service layer

    Returns:
        JSONResponse with appropriate status code
    """
    if isinstance(error, ValidationError):
        return error_response(error.message, 400)
    elif isinstance(error, BrowserNotFoundError):
        return error_response(error.message, 404)
    elif isinstance(error, DatabaseLockedError):
        return error_response(error.message, 423)  # Locked
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
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "chronicle-mcp",
        "version": get_version(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


async def ready_check(request: Request) -> JSONResponse:
    """Readiness check endpoint."""
    try:
        result = HistoryService.list_available_browsers()
        browsers = result["browsers"]
        return JSONResponse({
            "status": "ready" if browsers else "degraded",
            "service": "chronicle-mcp",
            "browsers": browsers,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "service": "chronicle-mcp",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, status_code=500)


async def metrics_check(request: Request) -> JSONResponse:
    """Basic metrics endpoint."""
    global REQUEST_COUNT, REQUEST_LATENCY_TOTAL, START_TIME

    uptime = time.time() - START_TIME
    avg_latency = REQUEST_LATENCY_TOTAL / REQUEST_COUNT if REQUEST_COUNT > 0 else 0

    return JSONResponse({
        "uptime_seconds": uptime,
        "requests_total": REQUEST_COUNT,
        "requests_per_second": REQUEST_COUNT / uptime if uptime > 0 else 0,
        "average_latency_seconds": avg_latency,
        "browsers_available": len(HistoryService.list_available_browsers()["browsers"]),
    })


async def prometheus_metrics(request: Request) -> Response:
    """Prometheus metrics endpoint."""
    global REQUEST_COUNT, REQUEST_LATENCY_TOTAL, START_TIME

    uptime = time.time() - START_TIME
    avg_latency = REQUEST_LATENCY_TOTAL / REQUEST_COUNT if REQUEST_COUNT > 0 else 0

    try:
        browsers_count = len(HistoryService.list_available_browsers()["browsers"])
    except Exception:
        browsers_count = 0

    metrics = f"""# HELP chronicle_uptime_seconds Server uptime in seconds
# TYPE chronicle_uptime_seconds gauge
chronicle_uptime_seconds {uptime}

# HELP chronicle_requests_total Total number of requests
# TYPE chronicle_requests_total counter
chronicle_requests_total {REQUEST_COUNT}

# HELP chronicle_requests_per_second Requests per second
# TYPE chronicle_requests_per_second gauge
chronicle_requests_per_second {REQUEST_COUNT / uptime if uptime > 0 else 0}

# HELP chronicle_average_latency_seconds Average request latency
# TYPE chronicle_average_latency_seconds gauge
chronicle_average_latency_seconds {avg_latency}

# HELP chronicle_browsers_available Number of available browsers
# TYPE chronicle_browsers_available gauge
chronicle_browsers_available {browsers_count}
"""
    return Response(content=metrics, media_type="text/plain")


async def list_browsers_endpoint(request: Request) -> JSONResponse:
    """List available browsers endpoint."""
    try:
        result = HistoryService.list_available_browsers()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def search_endpoint(request: Request) -> JSONResponse:
    """Search history endpoint."""
    try:
        data = await request.json()
        result = HistoryService.search_history(
            query=data.get("query", ""),
            limit=data.get("limit", 5),
            browser=data.get("browser", default_browser),
            format_type=data.get("format", "markdown")
        )

        if data.get("format") == "json":
            return JSONResponse({
                "results": result["results"],
                "count": result["count"]
            })
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def recent_endpoint(request: Request) -> JSONResponse:
    """Recent history endpoint."""
    try:
        data = await request.json()
        result = HistoryService.get_recent_history(
            hours=data.get("hours", 24),
            limit=data.get("limit", 20),
            browser=data.get("browser", default_browser),
            format_type=data.get("format", "markdown")
        )

        if data.get("format") == "json":
            return JSONResponse({
                "results": result["results"],
                "count": result["count"]
            })
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def count_endpoint(request: Request) -> JSONResponse:
    """Count visits endpoint."""
    try:
        data = await request.json()
        result = HistoryService.count_visits(
            domain=data.get("domain", ""),
            browser=data.get("browser", default_browser)
        )
        return JSONResponse({
            "domain": result["domain"],
            "browser": result["browser"],
            "count": result["count"]
        })
    except Exception as e:
        return handle_service_error_http(e)


async def top_domains_endpoint(request: Request) -> JSONResponse:
    """Top domains endpoint."""
    try:
        data = await request.json()
        result = HistoryService.list_top_domains(
            limit=data.get("limit", 10),
            browser=data.get("browser", default_browser),
            format_type="json"  # Always return structured data
        )
        return JSONResponse({
            "domains": [
                {"domain": d, "visits": v}
                for d, v in result["domains"]
            ]
        })
    except Exception as e:
        return handle_service_error_http(e)


async def search_date_endpoint(request: Request) -> JSONResponse:
    """Search by date endpoint."""
    try:
        data = await request.json()
        result = HistoryService.search_history_by_date(
            query=data.get("query", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            limit=data.get("limit", 10),
            browser=data.get("browser", default_browser),
            format_type=data.get("format", "markdown")
        )

        if data.get("format") == "json":
            return JSONResponse({
                "results": result["results"],
                "count": result["count"]
            })
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def delete_endpoint(request: Request) -> JSONResponse:
    """Delete history endpoint."""
    try:
        data = await request.json()
        result = HistoryService.delete_history(
            query=data.get("query", ""),
            limit=data.get("limit", 100),
            browser=data.get("browser", default_browser),
            confirm=data.get("confirm", False)
        )

        if result.get("preview"):
            return JSONResponse({
                "preview": True,
                "query": result["query"],
                "count": result["count"],
                "message": result["message"]
            })
        return JSONResponse({
            "deleted": result["deleted"],
            "query": result["query"],
            "browser": result["browser"],
            "message": result["message"]
        })
    except Exception as e:
        return handle_service_error_http(e)


async def domain_search_endpoint(request: Request) -> JSONResponse:
    """Search by domain endpoint."""
    try:
        data = await request.json()
        result = HistoryService.search_by_domain(
            domain=data.get("domain", ""),
            query=data.get("query"),
            limit=data.get("limit", 20),
            browser=data.get("browser", default_browser),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains")
        )

        if data.get("format") == "json":
            return JSONResponse({
                "domain": result["domain"],
                "results": [
                    {"title": title, "url": url, "timestamp": ts}
                    for title, url, ts in result["results"]
                ],
                "count": result["count"]
            })
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def browser_stats_endpoint(request: Request) -> JSONResponse:
    """Browser stats endpoint."""
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_browser_stats(
            browser=data.get("browser", default_browser)
        )
        return JSONResponse(result["stats"])
    except Exception as e:
        return handle_service_error_http(e)


async def most_visited_endpoint(request: Request) -> JSONResponse:
    """Most visited pages endpoint."""
    try:
        data = await request.json()
        result = HistoryService.get_most_visited_pages(
            limit=data.get("limit", 20),
            browser=data.get("browser", default_browser),
            format_type="json"  # Always return structured data
        )
        return JSONResponse({
            "pages": [
                {"title": title, "url": url, "visits": visits}
                for title, url, visits in result["pages"]
            ]
        })
    except Exception as e:
        return handle_service_error_http(e)


async def export_endpoint(request: Request) -> Response:
    """Export history endpoint."""
    try:
        data = await request.json()
        result = HistoryService.export_history(
            format_type=data.get("format_type", "csv"),
            limit=data.get("limit", 1000),
            query=data.get("query"),
            browser=data.get("browser", default_browser)
        )

        content_type = "text/csv" if result["format"] == "csv" else "application/json"
        return Response(
            content=result["content"],
            media_type=content_type
        )
    except Exception as e:
        error = handle_service_error_http(e)
        return error


async def advanced_search_endpoint(request: Request) -> JSONResponse:
    """Advanced search endpoint."""
    try:
        data = await request.json()
        result = HistoryService.search_history_advanced(
            query=data.get("query", ""),
            limit=data.get("limit", 20),
            browser=data.get("browser", default_browser),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains"),
            sort_by=data.get("sort_by", "date"),
            use_regex=data.get("use_regex", False),
            use_fuzzy=data.get("use_fuzzy", False),
            fuzzy_threshold=data.get("fuzzy_threshold", 0.6)
        )

        if data.get("format") == "json":
            return JSONResponse({
                "query": result["query"],
                "results": [
                    {"title": title, "url": url, "timestamp": ts}
                    for title, url, ts in result["results"]
                ],
                "count": result["count"],
                "options": result["options"]
            })
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def sync_endpoint(request: Request) -> JSONResponse:
    """Sync history endpoint."""
    try:
        data = await request.json()
        result = HistoryService.sync_history(
            source_browser=data.get("source_browser", ""),
            target_browser=data.get("target_browser", ""),
            merge_strategy=data.get("merge_strategy", "latest"),
            dry_run=data.get("dry_run", True)
        )

        return JSONResponse({
            "dry_run": result.get("dry_run", True),
            "source": result["source"],
            "target": result["target"],
            "entries_count": result["entries_count"],
            "merge_strategy": result["merge_strategy"],
            "message": result["message"]
        })
    except Exception as e:
        return handle_service_error_http(e)


routes = [
    Route("/health", health_check),
    Route("/ready", ready_check),
    Route("/metrics", metrics_check),
    Route("/metrics/prometheus", prometheus_metrics),
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
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> Any:
    """Lifespan context manager for startup and shutdown events."""
    global START_TIME
    START_TIME = time.time()
    logger.info("ChronicleMCP HTTP server starting...")
    yield
    logger.info("ChronicleMCP HTTP server shutting down...")


app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)


def run_http_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    default_browser_: str = "chrome",
) -> None:
    """Run the HTTP/SSE server.

    Args:
        host: Host to bind to
        port: Port to listen on
        default_browser_: Default browser to use
    """
    global default_browser
    default_browser = default_browser_

    import uvicorn

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
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
