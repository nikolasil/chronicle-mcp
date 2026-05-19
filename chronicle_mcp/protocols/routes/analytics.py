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


async def compare_periods_endpoint(request: Request) -> JSONResponse:
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

        result = HistoryService.compare_time_periods(
            start_date1=data.get("start_date1", ""),
            end_date1=data.get("end_date1", ""),
            start_date2=data.get("start_date2", ""),
            end_date2=data.get("end_date2", ""),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
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


async def productivity_endpoint(request: Request) -> JSONResponse:
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

        result = HistoryService.analyze_productivity(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
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


async def suggest_categories_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        validated, err = validate_request_data(
            data,
            [
                ("browser", validate_browser, {}),
                ("limit", validate_limit, {"min_val": 1, "max_val": 50, "field_name": "limit"}),
            ],
        )
        if err:
            return err

        result = HistoryService.suggest_categories(
            browser=validated.get("browser", data.get("browser", get_default_browser())),
            limit=validated.get("limit", data.get("limit", 20)),
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


async def visualization_endpoint(request: Request) -> JSONResponse:
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

        result = HistoryService.export_visualization(
            format_type=data.get("format_type", "chart_json"),
            period=data.get("period", "month"),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
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


async def insights_endpoint(request: Request) -> JSONResponse:
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

        result = HistoryService.generate_insights_report(
            period=data.get("period", "week"),
            browser=validated.get("browser", data.get("browser", get_default_browser())),
            format_type=data.get("format_type", "markdown"),
        )
        if data.get("format_type") == "json":
            return JSONResponse(result)
        return JSONResponse({"report": result["summary_markdown"]})
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
        Route("/api/compare-periods", compare_periods_endpoint, methods=["POST"]),
        Route("/api/productivity", productivity_endpoint, methods=["POST"]),
        Route("/api/suggest-categories", suggest_categories_endpoint, methods=["POST"]),
        Route("/api/visualization", visualization_endpoint, methods=["POST"]),
        Route("/api/insights", insights_endpoint, methods=["POST"]),
    ]
