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
from chronicle_mcp.core.validation import validate_browser, validate_limit

from ._shared import (
    error_response,
    get_default_browser,
    handle_service_error,
    validate_request_data,
)


async def list_browsers_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_browsers()
        return JSONResponse({"browsers": result["browsers"]})
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


async def list_bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_bookmarks()
        return JSONResponse({"browsers": result["browsers"]})
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


async def list_downloads_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_downloads()
        return JSONResponse({"browsers": result["browsers"]})
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


async def bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        validated, err = validate_request_data(
            data,
            [
                ("query", lambda v, **k: v, {}),
                ("limit", validate_limit, {"min_val": 1, "max_val": 100, "field_name": "limit"}),
                ("browser", validate_browser, {}),
                ("format", lambda v, **k: v, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.get_bookmarks(
            query=validated.get("query", data.get("query")),
            limit=validated.get("limit", data.get("limit", 50)),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
            format_type=validated.get("format", data.get("format", "markdown")),
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


async def downloads_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        validated, err = validate_request_data(
            data,
            [
                ("query", lambda v, **k: v, {}),
                ("limit", validate_limit, {"min_val": 1, "max_val": 100, "field_name": "limit"}),
                ("browser", validate_browser, {}),
                ("format", lambda v, **k: v, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.get_downloads(
            query=validated.get("query", data.get("query")),
            limit=validated.get("limit", data.get("limit", 50)),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
            format_type=validated.get("format", data.get("format", "markdown")),
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
        Route("/api/browsers", list_browsers_endpoint),
        Route("/api/bookmarks", list_bookmarks_endpoint),
        Route("/api/bookmarks/query", bookmarks_endpoint, methods=["POST"]),
        Route("/api/downloads", list_downloads_endpoint),
        Route("/api/downloads/query", downloads_endpoint, methods=["POST"]),
    ]
