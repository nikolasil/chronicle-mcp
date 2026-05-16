"""Event types for real-time history updates."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EventType(str, Enum):
    """Types of history change events."""

    HISTORY_ADDED = "history_added"
    HISTORY_DELETED = "history_deleted"
    HISTORY_UPDATED = "history_updated"
    BOOKMARK_ADDED = "bookmark_added"
    BOOKMARK_DELETED = "bookmark_deleted"
    BOOKMARK_UPDATED = "bookmark_updated"
    DOWNLOAD_ADDED = "download_added"
    DOWNLOAD_DELETED = "download_deleted"


@dataclass
class HistoryEvent:
    """Represents a history change event."""

    event_type: EventType
    browser: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: dict[str, Any] = field(default_factory=dict)
    source_url: str | None = None
    visit_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "browser": self.browser,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "source_url": self.source_url,
            "visit_count": self.visit_count,
        }


@dataclass
class Subscription:
    """Represents a client subscription to history events."""

    id: str
    browser: str
    event_types: list[EventType]
    callback: Callable[[HistoryEvent], None]
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_event: datetime | None = None
    event_count: int = 0

    def matches(self, event: HistoryEvent) -> bool:
        """Check if this subscription matches the given event."""
        if event.browser.lower() != self.browser.lower():
            return False
        return event.event_type in self.event_types

    def mark_event(self) -> None:
        """Mark that an event was sent to this subscription."""
        self.last_event = datetime.utcnow()
        self.event_count += 1


@dataclass
class SubscriptionInfo:
    """Public information about a subscription (excludes callback)."""

    id: str
    browser: str
    event_types: list[str]
    created_at: str
    last_event: str | None = None
    event_count: int = 0

    @classmethod
    def from_subscription(cls, sub: Subscription) -> "SubscriptionInfo":
        """Create info object from subscription."""
        return cls(
            id=sub.id,
            browser=sub.browser,
            event_types=[et.value for et in sub.event_types],
            created_at=sub.created_at.isoformat(),
            last_event=sub.last_event.isoformat() if sub.last_event else None,
            event_count=sub.event_count,
        )


@dataclass
class EventStats:
    """Statistics about events."""

    total_events: int = 0
    events_by_type: dict[str, int] = field(default_factory=dict)
    events_by_browser: dict[str, int] = field(default_factory=dict)
    active_subscriptions: int = 0
    last_event_time: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_events": self.total_events,
            "events_by_type": self.events_by_type,
            "events_by_browser": self.events_by_browser,
            "active_subscriptions": self.active_subscriptions,
            "last_event_time": self.last_event_time,
        }
