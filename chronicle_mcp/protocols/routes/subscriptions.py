from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from chronicle_mcp.core import HistoryService
from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
    ServiceError,
    ValidationError,
)

from ._shared import error_response, get_default_browser, handle_service_error


async def subscribe_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.subscribe_history_changes(
            browser=data.get("browser", get_default_browser()),
            event_types=data.get("event_types", ["history_added", "history_deleted"]),
            callback=None,
        )
        return JSONResponse(result)
    except ValidationError as e:
        return error_response(e.message, 400)
    except BrowserNotFoundError as e:
        return error_response(e.message, 404)
    except DatabaseLockedError as e:
        return error_response(e.message, 423)
    except PermissionDeniedError as e:
        return error_response(e.message, 403)
    except DatabaseError as e:
        return error_response(e.message, 500)
    except ServiceError as e:
        return error_response(e.message, 500)
    except Exception as e:
        return handle_service_error(e)


async def unsubscribe_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.unsubscribe_history_changes(
            subscription_id=data.get("subscription_id", "")
        )
        return JSONResponse(result)
    except ValidationError as e:
        return error_response(e.message, 400)
    except BrowserNotFoundError as e:
        return error_response(e.message, 404)
    except DatabaseLockedError as e:
        return error_response(e.message, 423)
    except PermissionDeniedError as e:
        return error_response(e.message, 403)
    except DatabaseError as e:
        return error_response(e.message, 500)
    except ServiceError as e:
        return error_response(e.message, 500)
    except Exception as e:
        return handle_service_error(e)


async def subscription_status_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_subscription_status(subscription_id=data.get("subscription_id"))
        return JSONResponse(result)
    except ValidationError as e:
        return error_response(e.message, 400)
    except BrowserNotFoundError as e:
        return error_response(e.message, 404)
    except DatabaseLockedError as e:
        return error_response(e.message, 423)
    except PermissionDeniedError as e:
        return error_response(e.message, 403)
    except DatabaseError as e:
        return error_response(e.message, 500)
    except ServiceError as e:
        return error_response(e.message, 500)
    except Exception as e:
        return handle_service_error(e)


async def find_duplicates_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.find_duplicate_entries(
            browser=data.get("browser", get_default_browser()),
            similarity_threshold=data.get("similarity_threshold", 0.9),
            limit=data.get("limit", 100),
        )
        return JSONResponse(result)
    except ValidationError as e:
        return error_response(e.message, 400)
    except BrowserNotFoundError as e:
        return error_response(e.message, 404)
    except DatabaseLockedError as e:
        return error_response(e.message, 423)
    except PermissionDeniedError as e:
        return error_response(e.message, 403)
    except DatabaseError as e:
        return error_response(e.message, 500)
    except ServiceError as e:
        return error_response(e.message, 500)
    except Exception as e:
        return handle_service_error(e)


async def delete_duplicates_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.delete_duplicates(
            browser=data.get("browser", get_default_browser()),
            similarity_threshold=data.get("similarity_threshold", 0.9),
            keep_strategy=data.get("keep_strategy", "most_visits"),
            confirm=data.get("confirm", False),
        )
        return JSONResponse(result)
    except ValidationError as e:
        return error_response(e.message, 400)
    except BrowserNotFoundError as e:
        return error_response(e.message, 404)
    except DatabaseLockedError as e:
        return error_response(e.message, 423)
    except PermissionDeniedError as e:
        return error_response(e.message, 403)
    except DatabaseError as e:
        return error_response(e.message, 500)
    except ServiceError as e:
        return error_response(e.message, 500)
    except Exception as e:
        return handle_service_error(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/subscribe", subscribe_endpoint, methods=["POST"]),
        Route("/api/unsubscribe", unsubscribe_endpoint, methods=["POST"]),
        Route("/api/subscription-status", subscription_status_endpoint, methods=["POST"]),
        Route("/api/find-duplicates", find_duplicates_endpoint, methods=["POST"]),
        Route("/api/delete-duplicates", delete_duplicates_endpoint, methods=["POST"]),
    ]
