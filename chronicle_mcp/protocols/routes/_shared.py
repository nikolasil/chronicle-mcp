import contextvars
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

if TYPE_CHECKING:
    pass

DEFAULT_BROWSER = "chrome"
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

_request_count: contextvars.ContextVar[int] = contextvars.ContextVar("request_count", default=0)
_request_latency_total: contextvars.ContextVar[float] = contextvars.ContextVar(
    "request_latency_total", default=0.0
)
_start_time: contextvars.ContextVar[float] = contextvars.ContextVar("start_time")
_default_browser: contextvars.ContextVar[str] = contextvars.ContextVar(
    "default_browser", default=DEFAULT_BROWSER
)
_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="")
_metrics: contextvars.ContextVar["RequestMetrics"] = contextvars.ContextVar(
    "_metrics", default=None
)


def generate_correlation_id() -> str:
    import uuid

    return str(uuid.uuid4())[:16]


def get_correlation_id() -> str:
    cid = _correlation_id.get()
    if not cid:
        cid = generate_correlation_id()
        _correlation_id.set(cid)
    return cid


def get_metrics() -> "RequestMetrics":
    metrics = _metrics.get()
    if metrics is None:
        metrics = RequestMetrics()
        _metrics.set(metrics)
    return metrics


def get_default_browser() -> str:
    return _default_browser.get()


class RequestMetrics:
    def __init__(self, default_browser: str = DEFAULT_BROWSER):
        self._count_token = _request_count.set(0)
        self._latency_token = _request_latency_total.set(0.0)
        self._start_token = _start_time.set(time.time())
        self._default_browser_token = _default_browser.set(default_browser)
        self._histogram_buckets: dict[str, list[float]] = {
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


def _classify_operation(path: str) -> str:
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


def handle_service_error(e: Exception) -> JSONResponse:
    """Handle service errors with specific exception types."""
    from json import JSONDecodeError

    from chronicle_mcp.core.exceptions import (
        BrowserNotFoundError,
        DatabaseError,
        DatabaseLockedError,
        PermissionDeniedError,
        ServiceError,
        ValidationError,
    )

    if isinstance(e, JSONDecodeError):
        return error_response("Invalid JSON in request body", 422)
    elif isinstance(e, ValidationError):
        return error_response(e.message, 400)
    elif isinstance(e, BrowserNotFoundError):
        return error_response(e.message, 404)
    elif isinstance(e, DatabaseLockedError):
        return error_response(e.message, 423)
    elif isinstance(e, PermissionDeniedError):
        return error_response(e.message, 403)
    elif isinstance(e, DatabaseError):
        return error_response(e.message, 500)
    elif isinstance(e, ServiceError):
        return error_response(e.message, 500)
    else:
        import logging

        logger = logging.getLogger(__name__)
        logger.exception("Unexpected error in HTTP endpoint")
        return error_response("An unexpected error occurred", 500)


def handle_service_error_http(error: Exception) -> JSONResponse:
    """Deprecated: Use handle_service_error instead."""
    return handle_service_error(error)


def validate_request_data(
    data: dict[str, Any],
    field_validators: list[tuple[str, Callable[..., Any], dict[str, Any]]],
) -> tuple[dict[str, Any], JSONResponse | None]:
    """Validate request data using field validators.

    Args:
        data: Request data dictionary
        field_validators: List of (field_name, validator_func, validator_kwargs) tuples

    Returns:
        Tuple of (validated_data, error_response) where error_response is None if valid
    """
    from chronicle_mcp.core import ValidationError
    from chronicle_mcp.core.validation import (
        validate_browser,
        validate_domain,
        validate_format_type,
        validate_fuzzy_threshold,
        validate_hours,
        validate_limit,
        validate_merge_strategy,
        validate_query,
        validate_sort_by,
    )

    validated: dict[str, Any] = {}

    for field_name, validator_func, kwargs in field_validators:
        value = data.get(field_name)
        if value is None:
            continue

        try:
            if validator_func is validate_query:
                validated[field_name] = validator_func(value, field_name=field_name)
            elif validator_func is validate_domain:
                validated[field_name] = validator_func(value)
            elif validator_func is validate_limit:
                validated[field_name] = validator_func(value, **kwargs)
            elif validator_func is validate_hours:
                validated[field_name] = validate_hours(value)
            elif validator_func is validate_browser:
                validated[field_name] = validate_browser(value)
            elif validator_func is validate_format_type:
                validated[field_name] = validator_func(value, **kwargs)
            elif validator_func is validate_sort_by:
                validated[field_name] = validate_sort_by(value)
            elif validator_func is validate_merge_strategy:
                validated[field_name] = validate_merge_strategy(value)
            elif validator_func is validate_fuzzy_threshold:
                validated[field_name] = validate_fuzzy_threshold(value)
            else:
                validated[field_name] = validator_func(value, **kwargs)
        except ValidationError as e:
            return {}, error_response(e.message, 400)

    return validated, None
