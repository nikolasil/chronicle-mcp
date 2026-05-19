from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from chronicle_mcp.core import HistoryService

from ._shared import get_default_browser, handle_service_error_http


async def list_browsers_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_browsers()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def list_bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_bookmarks()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def list_downloads_endpoint(request: Request) -> JSONResponse:
    try:
        result = HistoryService.list_available_downloads()
        return JSONResponse({"browsers": result["browsers"]})
    except Exception as e:
        return handle_service_error_http(e)


async def bookmarks_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_bookmarks(
            query=data.get("query"),
            limit=data.get("limit", 50),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
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
    except Exception as e:
        return handle_service_error_http(e)


async def downloads_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json() if await request.body() else {}
        result = HistoryService.get_downloads(
            query=data.get("query"),
            limit=data.get("limit", 50),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
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
    except Exception as e:
        return handle_service_error_http(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/browsers", list_browsers_endpoint),
        Route("/api/bookmarks", list_bookmarks_endpoint),
        Route("/api/bookmarks/query", bookmarks_endpoint, methods=["POST"]),
        Route("/api/downloads", list_downloads_endpoint),
        Route("/api/downloads/query", downloads_endpoint, methods=["POST"]),
    ]
