"""HTTP/SSE server for ChronicleMCP.

This module provides HTTP endpoints for accessing browser history
through a RESTful API. Uses Starlette for the web framework
and uvicorn for the ASGI server.
"""

import contextlib
import logging
import sqlite3
import time
from datetime import datetime, timezone

from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from chronicle_mcp.config import setup_logging
from chronicle_mcp.connection import (
    BrowserNotFoundError,
    ConnectionError,
    get_history_connection,
)
from chronicle_mcp.database import (
    count_domain_visits,
    format_results,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import get_top_domains as db_get_top_domains
from chronicle_mcp.database import search_by_date as db_search_by_date
from chronicle_mcp.paths import get_available_browsers

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

default_browser: str = "chrome"

REQUEST_COUNT = 0
REQUEST_LATENCY_TOTAL = 0.0
START_TIME = time.time()


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Create a standardized error response."""
    return JSONResponse({"error": message}, status_code=status_code)


async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint.

    Returns:
        JSON response with service status
    """
    return JSONResponse(
        {
            "status": "healthy",
            "service": "chronicle-mcp",
            "version": "1.1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


async def ready_check(request: Request) -> JSONResponse:
    """Readiness check endpoint.

    Returns:
        JSON response with readiness status and available browsers
    """
    browsers = get_available_browsers()
    return JSONResponse(
        {
            "status": "ready" if browsers else "degraded",
            "service": "chronicle-mcp",
            "browsers": browsers,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


async def metrics_check(request: Request) -> JSONResponse:
    """Basic metrics endpoint.

    Returns:
        JSON response with basic metrics
    """
    global REQUEST_COUNT, REQUEST_LATENCY_TOTAL, START_TIME

    uptime = time.time() - START_TIME
    avg_latency = REQUEST_LATENCY_TOTAL / REQUEST_COUNT if REQUEST_COUNT > 0 else 0

    return JSONResponse(
        {
            "uptime_seconds": uptime,
            "requests_total": REQUEST_COUNT,
            "requests_per_second": REQUEST_COUNT / uptime if uptime > 0 else 0,
            "average_latency_seconds": avg_latency,
            "browsers_available": len(get_available_browsers()),
        }
    )


async def prometheus_metrics(request: Request) -> Response:
    """Prometheus metrics endpoint.

    Returns:
        Prometheus-formatted metrics
    """
    global REQUEST_COUNT, REQUEST_LATENCY_TOTAL, START_TIME

    uptime = time.time() - START_TIME
    avg_latency = REQUEST_LATENCY_TOTAL / REQUEST_COUNT if REQUEST_COUNT > 0 else 0

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
chronicle_browsers_available {len(get_available_browsers())}
"""

    return Response(content=metrics, media_type="text/plain")


async def list_browsers_endpoint(request: Request) -> JSONResponse:
    """List available browsers endpoint.

    Returns:
        JSON response with list of available browsers
    """
    return JSONResponse({"browsers": get_available_browsers()})


async def search_endpoint(request: Request) -> JSONResponse:
    """Search history endpoint.

    Request body:
        {
            "query": "search term",
            "limit": 10,
            "browser": "chrome",
            "format": "markdown"
        }

    Returns:
        JSON response with search results
    """
    data = await request.json()
    query = data.get("query", "")
    limit = data.get("limit", 5)
    browser = data.get("browser", default_browser)
    format_type = data.get("format", "markdown")

    if not query:
        return error_response("Query cannot be empty")

    try:
        with get_history_connection(browser) as conn:
            rows = query_history(conn, query, limit)
            if format_type == "json":
                return JSONResponse({"results": rows, "count": len(rows)})
            return JSONResponse({"results": format_results(rows, query, "markdown")})
    except BrowserNotFoundError:
        return error_response(f"{browser} history not found", 404)
    except ConnectionError as e:
        return error_response(f"Connection error: {e.message}", 500)
    except PermissionError:
        return error_response(f"Permission denied accessing {browser} history", 403)
    except sqlite3.OperationalError:
        return error_response(f"Unable to access {browser} history database", 500)
    except Exception as e:
        logger.error(f"Search error: {e}")
        return error_response("Search failed", 500)


async def recent_endpoint(request: Request) -> JSONResponse:
    """Recent history endpoint.

    Request body:
        {
            "hours": 24,
            "limit": 20,
            "browser": "chrome",
            "format": "markdown"
        }

    Returns:
        JSON response with recent history entries
    """
    data = await request.json()
    hours = data.get("hours", 24)
    limit = data.get("limit", 20)
    browser = data.get("browser", default_browser)
    format_type = data.get("format", "markdown")

    try:
        with get_history_connection(browser) as conn:
            rows = query_recent_history(conn, hours, limit)
            if format_type == "json":
                return JSONResponse({"results": rows, "count": len(rows)})
            return JSONResponse(
                {"results": format_results(rows, f"last {hours} hours", "markdown")}
            )
    except BrowserNotFoundError:
        return error_response(f"{browser} history not found", 404)
    except ConnectionError as e:
        return error_response(f"Connection error: {e.message}", 500)
    except Exception as e:
        logger.error(f"Recent history error: {e}")
        return error_response("Failed to get recent history", 500)


async def count_endpoint(request: Request) -> JSONResponse:
    """Count visits endpoint.

    Request body:
        {
            "domain": "github.com",
            "browser": "chrome"
        }

    Returns:
        JSON response with visit count
    """
    data = await request.json()
    domain = data.get("domain", "")
    browser = data.get("browser", default_browser)

    if not domain:
        return error_response("Domain cannot be empty")

    try:
        with get_history_connection(browser) as conn:
            count = count_domain_visits(conn, domain)
            return JSONResponse({"domain": domain, "browser": browser, "count": count})
    except BrowserNotFoundError:
        return error_response(f"{browser} history not found", 404)
    except ConnectionError as e:
        return error_response(f"Connection error: {e.message}", 500)
    except Exception as e:
        logger.error(f"Count visits error: {e}")
        return error_response("Failed to count visits", 500)


async def top_domains_endpoint(request: Request) -> JSONResponse:
    """Top domains endpoint.

    Request body:
        {
            "limit": 10,
            "browser": "chrome"
        }

    Returns:
        JSON response with top domains
    """
    data = await request.json()
    limit = data.get("limit", 10)
    browser = data.get("browser", default_browser)

    try:
        with get_history_connection(browser) as conn:
            domains = db_get_top_domains(conn, limit)
            return JSONResponse({"domains": [{"domain": d, "visits": v} for d, v in domains]})
    except BrowserNotFoundError:
        return error_response(f"{browser} history not found", 404)
    except ConnectionError as e:
        return error_response(f"Connection error: {e.message}", 500)
    except Exception as e:
        logger.error(f"Top domains error: {e}")
        return error_response("Failed to get top domains", 500)


async def search_date_endpoint(request: Request) -> JSONResponse:
    """Search by date endpoint.

    Request body:
        {
            "query": "search term",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "limit": 10,
            "browser": "chrome",
            "format": "markdown"
        }

    Returns:
        JSON response with search results
    """
    data = await request.json()
    query = data.get("query", "")
    start_date = data.get("start_date", "")
    end_date = data.get("end_date", "")
    limit = data.get("limit", 10)
    browser = data.get("browser", default_browser)
    format_type = data.get("format", "markdown")

    if not query or not start_date or not end_date:
        return error_response("query, start_date, and end_date are required")

    try:
        with get_history_connection(browser) as conn:
            rows = db_search_by_date(conn, query, start_date, end_date, limit)
            if format_type == "json":
                return JSONResponse({"results": rows, "count": len(rows)})
            return JSONResponse({"results": format_results(rows, query, "markdown")})
    except BrowserNotFoundError:
        return error_response(f"{browser} history not found", 404)
    except ConnectionError as e:
        return error_response(f"Connection error: {e.message}", 500)
    except Exception as e:
        logger.error(f"Search by date error: {e}")
        return error_response("Search by date failed", 500)


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
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]


@contextlib.asynccontextmanager  # type: ignore[arg-type]
async def lifespan(app: Starlette) -> None:  # type: ignore[misc]
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
