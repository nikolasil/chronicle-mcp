from starlette.requests import Request
from starlette.responses import JSONResponse, Response
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
from chronicle_mcp.core.validation import validate_browser, validate_limit, validate_merge_strategy

from ._shared import (
    error_response,
    get_default_browser,
    handle_service_error,
    limiter,
    validate_request_data,
)


@limiter.limit("10/minute")
async def delete_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        validated, err = validate_request_data(
            data,
            [
                ("query", lambda v, **k: v, {}),
                ("limit", validate_limit, {"min_val": 1, "max_val": 500, "field_name": "limit"}),
                ("browser", validate_browser, {}),
                ("confirm", lambda v, **k: v, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.delete_history(
            query=validated.get("query", data.get("query", "")),
            limit=validated.get("limit", data.get("limit", 100)),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
            confirm=validated.get("confirm", data.get("confirm", False)),
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


async def export_endpoint(request: Request) -> Response:
    try:
        data = await request.json()
        validated, err = validate_request_data(
            data,
            [
                ("format_type", lambda v, **k: v, {}),
                ("limit", validate_limit, {"min_val": 1, "max_val": 5000, "field_name": "limit"}),
                ("query", lambda v, **k: v, {}),
                ("browser", validate_browser, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.export_history(
            format_type=validated.get("format_type", data.get("format_type", "csv")),
            limit=validated.get("limit", data.get("limit", 1000)),
            query=validated.get("query", data.get("query")),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
        )

        content_type = "text/csv" if result["format"] == "csv" else "application/json"
        return Response(content=result["content"], media_type=content_type)
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


async def sync_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        validated, err = validate_request_data(
            data,
            [
                ("source_browser", validate_browser, {}),
                ("target_browser", validate_browser, {}),
                ("merge_strategy", validate_merge_strategy, {}),
                ("dry_run", lambda v, **k: v, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.sync_history(
            source_browser=validated.get("source_browser", data.get("source_browser", "")),
            target_browser=validated.get("target_browser", data.get("target_browser", "")),
            merge_strategy=validated.get("merge_strategy", data.get("merge_strategy", "latest")),
            dry_run=validated.get("dry_run", data.get("dry_run", True)),
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


async def browser_stats_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        validated, err = validate_request_data(
            data,
            [
                ("browser", validate_browser, {}),
            ],
        )
        if err:
            return err

        result = HistoryService.get_browser_stats(
            browser=validated.get("browser", data.get("browser", get_default_browser()))
        )
        return JSONResponse(result["stats"])
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
        Route("/api/delete", delete_endpoint, methods=["POST"]),
        Route("/api/export", export_endpoint, methods=["POST"]),
        Route("/api/sync", sync_endpoint, methods=["POST"]),
        Route("/api/stats", browser_stats_endpoint, methods=["POST"]),
    ]
