from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from chronicle_mcp.core import HistoryService

from ._shared import get_default_browser, handle_service_error_http, limiter


@limiter.limit("30/minute")
async def search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history(
            query=data.get("query", ""),
            limit=data.get("limit", 5),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("30/minute")
async def recent_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.get_recent_history(
            hours=data.get("hours", 24),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


@limiter.limit("30/minute")
async def count_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.count_visits(
            domain=data.get("domain", ""), browser=data.get("browser", get_default_browser())
        )
        return JSONResponse(
            {"domain": result["domain"], "browser": result["browser"], "count": result["count"]}
        )
    except Exception as e:
        return handle_service_error_http(e)


async def top_domains_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.list_top_domains(
            limit=data.get("limit", 10),
            browser=data.get("browser", get_default_browser()),
            format_type="json",
        )
        return JSONResponse({"domains": [{"domain": d, "visits": v} for d, v in result["domains"]]})
    except Exception as e:
        return handle_service_error_http(e)


async def search_date_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history_by_date(
            query=data.get("query", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            limit=data.get("limit", 10),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
        )

        if data.get("format") == "json":
            return JSONResponse({"results": result["results"], "count": result["count"]})
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def domain_search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_by_domain(
            domain=data.get("domain", ""),
            query=data.get("query"),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains"),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "domain": result["domain"],
                    "results": [
                        {"title": title, "url": url, "timestamp": ts}
                        for title, url, ts in result["results"]
                    ],
                    "count": result["count"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


async def most_visited_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.get_most_visited_pages(
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type="json",
        )
        return JSONResponse(
            {
                "pages": [
                    {"title": title, "url": url, "visits": visits}
                    for title, url, visits in result["pages"]
                ]
            }
        )
    except Exception as e:
        return handle_service_error_http(e)


async def advanced_search_endpoint(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        result = HistoryService.search_history_advanced(
            query=data.get("query", ""),
            limit=data.get("limit", 20),
            browser=data.get("browser", get_default_browser()),
            format_type=data.get("format", "markdown"),
            exclude_domains=data.get("exclude_domains"),
            sort_by=data.get("sort_by", "date"),
            use_regex=data.get("use_regex", False),
            use_fuzzy=data.get("use_fuzzy", False),
            fuzzy_threshold=data.get("fuzzy_threshold", 0.6),
        )

        if data.get("format") == "json":
            return JSONResponse(
                {
                    "query": result["query"],
                    "results": [
                        {"title": title, "url": url, "timestamp": ts}
                        for title, url, ts in result["results"]
                    ],
                    "count": result["count"],
                    "options": result["options"],
                }
            )
        return JSONResponse({"results": result["message"]})
    except Exception as e:
        return handle_service_error_http(e)


def get_routes() -> list[Route]:
    return [
        Route("/api/search", search_endpoint, methods=["POST"]),
        Route("/api/recent", recent_endpoint, methods=["POST"]),
        Route("/api/count", count_endpoint, methods=["POST"]),
        Route("/api/top-domains", top_domains_endpoint, methods=["POST"]),
        Route("/api/search-date", search_date_endpoint, methods=["POST"]),
        Route("/api/domain-search", domain_search_endpoint, methods=["POST"]),
        Route("/api/most-visited", most_visited_endpoint, methods=["POST"]),
        Route("/api/advanced-search", advanced_search_endpoint, methods=["POST"]),
    ]
