from collections.abc import Callable
from typing import Any

from chronicle_mcp.core.events import EventType
from chronicle_mcp.core.realtime import get_subscription_manager
from chronicle_mcp.core.validation import validate_browser


class SubscriptionService:
    @classmethod
    def subscribe_history_changes(
        cls,
        browser: str,
        event_types: list[str],
        callback: Callable[[Any], None] | None = None,
    ) -> dict[str, Any]:
        """Subscribe to history changes for a browser.

        Args:
            browser: Browser to subscribe to
            event_types: List of event types ('history_added', 'history_deleted', etc.)
            callback: Callback function to receive events

        Returns:
            Dictionary with subscription_id and stats
        """
        browser_lower = validate_browser(browser)

        event_type_enums = []
        for et in event_types:
            try:
                event_type_enums.append(EventType(et))
            except ValueError:
                raise ValueError(f"Invalid event type: {et}")

        manager = get_subscription_manager()
        subscription_id = manager.subscribe(
            browser_lower, event_type_enums, callback if callback is not None else lambda e: None
        )
        stats = manager.get_stats()

        return {
            "subscription_id": subscription_id,
            "browser": browser_lower,
            "event_types": event_types,
            "active_subscriptions": stats.active_subscriptions,
            "total_events": stats.total_events,
        }

    @classmethod
    def unsubscribe_history_changes(cls, subscription_id: str) -> dict[str, Any]:
        """Unsubscribe from history changes.

        Args:
            subscription_id: Subscription ID to remove

        Returns:
            Dictionary with success status
        """
        manager = get_subscription_manager()
        success = manager.unsubscribe(subscription_id)

        return {
            "subscription_id": subscription_id,
            "success": success,
            "active_subscriptions": manager.get_active_count(),
        }

    @classmethod
    def get_subscription_status(cls, subscription_id: str | None = None) -> dict[str, Any]:
        """Get subscription status.

        Args:
            subscription_id: Optional specific subscription ID

        Returns:
            Dictionary with subscription info or global stats
        """
        manager = get_subscription_manager()

        if subscription_id:
            info = manager.get_subscription(subscription_id)
            if info:
                return {
                    "subscription_id": info.id,
                    "browser": info.browser,
                    "event_types": info.event_types,
                    "created_at": info.created_at,
                    "last_event": info.last_event,
                    "event_count": info.event_count,
                }
            return {"error": "Subscription not found"}

        stats = manager.get_stats()
        subscriptions = manager.get_subscriptions()

        return {
            "active_subscriptions": stats.active_subscriptions,
            "total_events": stats.total_events,
            "events_by_type": stats.events_by_type,
            "events_by_browser": stats.events_by_browser,
            "last_event_time": stats.last_event_time,
            "subscriptions": [
                {
                    "id": s.id,
                    "browser": s.browser,
                    "event_types": s.event_types,
                    "event_count": s.event_count,
                }
                for s in subscriptions
            ],
        }
