"""Analytics service layer for ChronicleMCP.

This module provides analytics and insights operations for browser history.
It handles productivity analysis, category suggestions, and visualization exports.
"""

import csv
import logging
from io import StringIO
from typing import Any

from chronicle_mcp.connection import (
    BrowserNotFoundError as ConnBrowserNotFoundError,
)
from chronicle_mcp.connection import (
    ConnectionError as ConnConnectionError,
)
from chronicle_mcp.connection import (
    DatabaseLockedError as ConnDatabaseLockedError,
)
from chronicle_mcp.connection import (
    PermissionDeniedError as ConnPermissionDeniedError,
)
from chronicle_mcp.connection import get_history_connection
from chronicle_mcp.core.categories import (
    CATEGORY_DESCRIPTIONS,
    CATEGORY_PATTERNS,
    calculate_productivity_score,
    categorize_url,
    generate_recommendations,
    get_category_breakdown,
)
from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
)
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_date_range,
    validate_format_type,
    validate_limit,
)
from chronicle_mcp.database import (
    get_browser_stats as db_get_browser_stats,
)
from chronicle_mcp.database import (
    get_category_stats,
    get_hourly_stats_for_period,
    get_uncategorized_urls,
    get_visit_patterns_by_hour,
)
from chronicle_mcp.database import (
    get_top_domains as db_get_top_domains,
)

logger = logging.getLogger(__name__)


def get_browser_stats(
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Get browser statistics.

    Args:
        browser: Browser to analyze
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with statistics and formatted message
    """
    from chronicle_mcp.core.formatters import format_browser_stats

    browser_lower = validate_browser(browser)
    format_clean = validate_format_type(format_type)

    stats = with_connection(browser_lower, db_get_browser_stats)

    return {"stats": stats, "message": format_browser_stats(stats, format_clean)}


def with_connection(browser: str, operation: Any) -> Any:
    """Execute an operation with a database connection.

    Args:
        browser: Browser name
        operation: Function that takes a connection and returns data

    Returns:
        Result of the operation

    Raises:
        BrowserNotFoundError: If browser not found
        DatabaseLockedError: If database is locked
        PermissionDeniedError: If permission denied
        DatabaseError: For other database errors
    """
    try:
        with get_history_connection(browser) as conn:
            return operation(conn)
    except ConnBrowserNotFoundError:
        raise BrowserNotFoundError(browser)
    except ConnDatabaseLockedError:
        raise DatabaseLockedError(browser)
    except ConnPermissionDeniedError:
        raise PermissionDeniedError(browser, "")
    except ConnConnectionError as e:
        logger.error(f"Connection error: {e.message}")
        raise DatabaseError(f"Failed to access {browser} history: {e.message}")
    except Exception as e:
        logger.exception("Unexpected database error")
        raise DatabaseError(f"Database operation failed: {e}")


def compare_time_periods(
    start_date1: str,
    end_date1: str,
    start_date2: str,
    end_date2: str,
    browser: str = "chrome",
) -> dict[str, Any]:
    """Compare browsing statistics between two time periods.

    Args:
        start_date1: Start date of first period (ISO format)
        end_date1: End date of first period (ISO format)
        start_date2: Start date of second period (ISO format)
        end_date2: End date of second period (ISO format)
        browser: Browser to analyze

    Returns:
        Dictionary with comparison data for both periods
    """
    browser_lower = validate_browser(browser)
    validate_date_range(start_date1, end_date1)
    validate_date_range(start_date2, end_date2)

    period1_stats = with_connection(
        browser_lower,
        lambda conn: get_hourly_stats_for_period(conn, start_date1, end_date1),
    )

    period2_stats = with_connection(
        browser_lower,
        lambda conn: get_hourly_stats_for_period(conn, start_date2, end_date2),
    )

    category_stats = with_connection(
        browser_lower,
        lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
    )

    total_delta = period2_stats["total_visits"] - period1_stats["total_visits"]
    unique_delta = period2_stats["unique_urls"] - period1_stats["unique_urls"]

    top_domains_period1 = set(d for d, _ in period1_stats.get("top_domains", []))
    top_domains_period2 = set(d for d, _ in period2_stats.get("top_domains", []))
    domains_gained = list(top_domains_period2 - top_domains_period1)[:5]
    domains_lost = list(top_domains_period1 - top_domains_period2)[:5]

    return {
        "period1": {
            "start": start_date1,
            "end": end_date1,
            "total_visits": period1_stats["total_visits"],
            "unique_urls": period1_stats["unique_urls"],
            "top_domains": period1_stats.get("top_domains", []),
        },
        "period2": {
            "start": start_date2,
            "end": end_date2,
            "total_visits": period2_stats["total_visits"],
            "unique_urls": period2_stats["unique_urls"],
            "top_domains": period2_stats.get("top_domains", []),
        },
        "changes": {
            "total_visits_delta": total_delta,
            "unique_urls_delta": unique_delta,
            "top_domains_gained": domains_gained,
            "top_domains_lost": domains_lost,
        },
        "category_breakdown": category_stats,
    }


def analyze_productivity(
    start_date: str | None = None,
    end_date: str | None = None,
    browser: str = "chrome",
) -> dict[str, Any]:
    """Analyze browsing productivity.

    Args:
        start_date: Optional start date (ISO format)
        end_date: Optional end date (ISO format)
        browser: Browser to analyze

    Returns:
        Dictionary with productivity score, breakdown, and recommendations
    """
    browser_lower = validate_browser(browser)

    category_stats = with_connection(
        browser_lower,
        lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
    )

    breakdown = get_category_breakdown(category_stats)
    score, grade = calculate_productivity_score(category_stats)

    top_domains = with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 10))

    recommendations = generate_recommendations(category_stats, top_domains)

    return {
        "productivity_score": score,
        "grade": grade,
        "category_breakdown": breakdown,
        "recommendations": recommendations,
        "browser": browser_lower,
        "period": {
            "start": start_date,
            "end": end_date,
        },
    }


def suggest_categories(
    browser: str = "chrome",
    limit: int = 20,
) -> dict[str, Any]:
    """Suggest categories for uncategorized URLs.

    Args:
        browser: Browser to analyze
        limit: Maximum number of suggestions

    Returns:
        Dictionary with uncategorized URLs that could be categorized
    """
    browser_lower = validate_browser(browser)
    limit_val = validate_limit(limit, 1, 100)

    uncategorized = with_connection(
        browser_lower,
        lambda conn: get_uncategorized_urls(conn, CATEGORY_PATTERNS, limit_val),
    )

    suggestions = []
    for title, url, visit_count in uncategorized:
        category = categorize_url(url)
        if category:
            suggestions.append(
                {
                    "title": title,
                    "url": url,
                    "visit_count": visit_count,
                    "suggested_category": category,
                }
            )

    return {
        "uncategorized": suggestions,
        "count": len(suggestions),
        "browser": browser_lower,
    }


def export_visualization(
    format_type: str = "chart_json",
    period: str = "month",
    browser: str = "chrome",
) -> dict[str, Any]:
    """Export data formatted for visualization.

    Args:
        format_type: 'chart_json' for Chart.js or 'csv'
        period: Time period - 'day', 'week', or 'month'
        browser: Browser to export from

    Returns:
        Dictionary with visualization-ready data
    """
    browser_lower = validate_browser(browser)

    category_stats = with_connection(
        browser_lower,
        lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
    )

    breakdown = get_category_breakdown(category_stats)

    visit_patterns = with_connection(browser_lower, lambda conn: get_visit_patterns_by_hour(conn))

    top_domains = with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 10))

    if format_type == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Category", "Count", "Percentage", "Weight"])

        for cat, data in breakdown.items():
            writer.writerow(
                [
                    cat,
                    data.get("count", 0),
                    data.get("percentage", 0),
                    data.get("weight", 0),
                ]
            )

        return {
            "content": output.getvalue(),
            "format": "csv",
            "period": period,
        }

    chart_data = {
        "charts": [
            {
                "type": "doughnut",
                "title": "Time by Category",
                "data": {
                    "labels": list(breakdown.keys()),
                    "datasets": [
                        {
                            "data": [breakdown[c].get("count", 0) for c in breakdown],
                            "backgroundColor": [
                                "#4CAF50",
                                "#2196F3",
                                "#FF9800",
                                "#E91E63",
                                "#9C27B0",
                                "#00BCD4",
                                "#795548",
                            ],
                        }
                    ],
                },
            },
            {
                "type": "bar",
                "title": "Top 10 Domains",
                "data": {
                    "labels": [d for d, _ in top_domains],
                    "datasets": [
                        {
                            "label": "Visits",
                            "data": [c for _, c in top_domains],
                            "backgroundColor": "#2196F3",
                        }
                    ],
                },
            },
            {
                "type": "bar",
                "title": "Activity by Hour",
                "data": {
                    "labels": list(range(24)),
                    "datasets": [
                        {
                            "label": "Visits",
                            "data": [visit_patterns.get(h, 0) for h in range(24)],
                            "backgroundColor": "#4CAF50",
                        }
                    ],
                },
            },
        ],
        "period": period,
        "category_breakdown": breakdown,
    }

    return {
        "charts": chart_data["charts"],
        "period": period,
        "category_breakdown": breakdown,
    }


def generate_insights_report(
    period: str = "week",
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Generate comprehensive browsing insights report.

    Args:
        period: Time period - 'day', 'week', or 'month'
        browser: Browser to analyze
        format_type: 'markdown' for text or 'json' for data

    Returns:
        Dictionary with summary markdown and detailed data
    """
    browser_lower = validate_browser(browser)

    stats = with_connection(browser_lower, db_get_browser_stats)
    productivity = analyze_productivity(browser=browser_lower)
    top_domains = with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 5))

    insights_parts = [
        f"# Browsing Insights Report ({period})",
        f"\n**Browser:** {browser_lower}",
        f"\n**Total Visits:** {stats.get('total_visits', 0)}",
        f"\n**Unique URLs:** {stats.get('unique_urls', 0)}",
        "\n## Productivity",
        f"\n**Score:** {productivity['productivity_score']}/100 ({productivity['grade']}",
    ]

    for category, data in productivity.get("category_breakdown", {}).items():
        desc = CATEGORY_DESCRIPTIONS.get(category, category)
        insights_parts.append(
            f"- **{category.title()}** ({desc}): "
            f"{data.get('count', 0)} visits ({data.get('percentage', 0)}%)"
        )

    insights_parts.append("\n## Top Domains")
    for domain, count in top_domains:
        insights_parts.append(f"- {domain}: {count} visits")

    insights_parts.append("\n## Recommendations")
    for rec in productivity.get("recommendations", []):
        insights_parts.append(f"- {rec}")

    summary_markdown = "\n".join(insights_parts)

    if format_type == "json":
        return {
            "summary_markdown": summary_markdown,
            "data": {
                "stats": stats,
                "productivity": productivity,
                "top_domains": top_domains,
            },
        }

    return {
        "summary_markdown": summary_markdown,
        "browser": browser_lower,
        "period": period,
    }
