from . import analytics, browsing, health, management, search, subscriptions
from ._shared import limiter

all_routes = (
    health.get_routes()
    + search.get_routes()
    + management.get_routes()
    + browsing.get_routes()
    + analytics.get_routes()
    + subscriptions.get_routes()
)

__all__ = [
    "all_routes",
    "health",
    "search",
    "management",
    "browsing",
    "analytics",
    "subscriptions",
    "limiter",
]
