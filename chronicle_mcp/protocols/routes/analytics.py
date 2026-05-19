from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from chronicle_mcp.core import HistoryService

from ._shared import get_default_browser, handle_service_error_http


async def compare_periods_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.compare_time_periods(
            start_date1=data.get("start_date1", ""),
            end_date1=data.get("end_date1", ""),
            start_date2=data.get("start_date2", ""),
            end_date2=data.get("end_date2", ""),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def productivity_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.analyze_productivity(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def suggest_categories_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.suggest_categories(
            browser=data.get("browser", get_default_browser()),
            limit=data.get("limit", 20),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def visualization_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.export_visualization(
            format_type=data.get("format_type", "chart_json"),
            period=data.get("period", "month"),
            browser=data.get("browser", get_default_browser()),
        )
        return JSONResponse(result)
    except Exception as e:
        return handle_service_error_http(e)


async def insights_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.generate_insights_report(
            period=data.get("period", "week"),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format_type", "markdown"),
        )
        if data.get("format_type") == "json":
            return JSONResponse(result)
        return JSONResponse({"report": result["summary_markdown"]})
    except Exception as e:
        return handle_service_error_http(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/compare-periods", compare_periods_endpoint, methods=["POST"]),
        Route("/api/productivity", productivity_endpoint, methods=["POST"]),
        Route("/api/suggest-categories", suggest_categories_endpoint, methods=["POST"]),
        Route("/api/visualization", visualization_endpoint, methods=["POST"]),
        Route("/api/insights", insights_endpoint, methods=["POST"]),
    ]
