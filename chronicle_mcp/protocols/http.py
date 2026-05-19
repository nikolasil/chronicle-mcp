"""HTTP/SSE protocol adapter for ChronicleMCP.

This module provides HTTP endpoints using Starlette.
All business logic is delegated to the HistoryService in the core layer.
"""

import contextlib
import logging
import time
from typing import Any

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from chronicle_mcp.config import load_config, setup_logging
from chronicle_mcp.protocols.routes import all_routes
from chronicle_mcp.protocols.routes._shared import (
    DEFAULT_BROWSER,
    RequestMetrics,
    _classify_operation,
    _metrics,
    limiter,
)

setup_logging()
logger = logging.getLogger(__name__)

routes = all_routes


def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        {"error": "Rate limit exceeded", "detail": str(exc.detail)},
        status_code=429,
    )


class MetricsMiddleware:
    def __init__(self, app: Any):
        self.app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        start = time.time()
        from chronicle_mcp.protocols.routes._shared import (
            _correlation_id,
            generate_correlation_id,
            get_metrics,
        )

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
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
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
