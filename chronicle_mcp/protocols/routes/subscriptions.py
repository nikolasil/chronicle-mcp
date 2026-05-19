from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from chronicle_mcp.core import HistoryService

from ._shared import get_default_browser, handle_service_error_http


async def subscribe_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.subscribe_history_changes(
            browser=data.get("browser", get_default_browser()),
            event_types=data.get("event_types", ["history_added", "history_deleted"]),
            callback=None,
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def unsubscribe_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.unsubscribe_history_changes(
            subscription_id=data.get("subscription_id", "")
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def subscription_status_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_subscription_status(subscription_id=data.get("subscription_id"))
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def find_duplicates_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.find_duplicate_entries(
            browser=data.get("browser", get_default_browser()),
            similarity_threshold=data.get("similarity_threshold", 0.9),
            limit=data.get("limit", 100),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


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
    except Exception as e:
        return handle_service_error_http(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/subscribe", subscribe_endpoint, methods=["POST"]),
        Route("/api/unsubscribe", unsubscribe_endpoint, methods=["POST"]),
        Route("/api/subscription-status", subscription_status_endpoint, methods=["POST"]),
        Route("/api/find-duplicates", find_duplicates_endpoint, methods=["POST"]),
        Route("/api/delete-duplicates", delete_duplicates_endpoint, methods=["POST"]),
    ]
