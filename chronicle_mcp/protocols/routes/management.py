from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from chronicle_mcp.core import HistoryService

from ._shared import get_default_browser, handle_service_error_http, limiter


@limiter.limit("10/minute")
async def delete_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.delete_history(
            query=data.get("query", ""),
            limit=data.get("limit", 100),
            browser=data.get("browser", get_default_browser()),
            confirm=data.get("confirm", False),
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
    except Exception as e:
        return handle_service_error_http(e)


async def export_endpoint(request: Request) -> Response:
    try:
        data = await request.json()
        result = HistoryService.export_history(
            format_type=data.get("format_type", "csv"),
            limit=data.get("limit", 1000),
            query=data.get("query"),
            browser=data.get("browser", get_default_browser()),
        )

        content_type = "text/csv" if result["format"] == "csv" else "application/json"
        return Response(content=result["content"], media_type=content_type)
    except Exception as e:
        return handle_service_error_http(e)


async def sync_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.sync_history(
            source_browser=data.get("source_browser", ""),
            target_browser=data.get("target_browser", ""),
            merge_strategy=data.get("merge_strategy", "latest"),
            dry_run=data.get("dry_run", True),
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
    except Exception as e:
        return handle_service_error_http(e)


async def browser_stats_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_browser_stats(
            browser=data.get("browser", get_default_browser())
        )
        return JSONResponse(result["stats"])
    except Exception as e:
        return handle_service_error_http(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/delete", delete_endpoint, methods=["POST"]),
        Route("/api/export", export_endpoint, methods=["POST"]),
        Route("/api/sync", sync_endpoint, methods=["POST"]),
        Route("/api/stats", browser_stats_endpoint, methods=["POST"]),
    ]
