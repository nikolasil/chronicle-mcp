from datetime import datetime, timezone

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

from chronicle_mcp.config import get_version
from chronicle_mcp.core import HistoryService

from ._shared import get_metrics


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


def get_routes() -> list[Route]:
    return [
        Route("/health", health_check),
        Route("/ready", ready_check),
        Route("/metrics", metrics_check),
        Route("/metrics/prometheus", prometheus_metrics),
        Route("/docs", docs_endpoint),
        Route("/api-docs/openapi.json", openapi_spec),
    ]
