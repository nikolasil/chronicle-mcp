"""Tests for event types and data classes in chronicle_mcp.core.events."""

from datetime import datetime, timezone

import pytest

from chronicle_mcp.core.events import (
    EventStats,
    EventType,
    HistoryEvent,
    Subscription,
    SubscriptionInfo,
)


class TestEventType:
    """Tests for EventType enum."""

    def test_event_type_values(self):
        """Test all EventType enum values exist."""
        assert EventType.HISTORY_ADDED.value == "history_added"
        assert EventType.HISTORY_DELETED.value == "history_deleted"
        assert EventType.HISTORY_UPDATED.value == "history_updated"
        assert EventType.BOOKMARK_ADDED.value == "bookmark_added"
        assert EventType.BOOKMARK_DELETED.value == "bookmark_deleted"
        assert EventType.BOOKMARK_UPDATED.value == "bookmark_updated"
        assert EventType.DOWNLOAD_ADDED.value == "download_added"
        assert EventType.DOWNLOAD_DELETED.value == "download_deleted"

    def test_event_type_is_string_enum(self):
        """Test EventType is a string enum."""
        assert isinstance(EventType.HISTORY_ADDED, str)
        assert EventType.HISTORY_ADDED == "history_added"

    def test_event_type_from_value(self):
        """Test creating EventType from string value."""
        assert EventType("history_added") == EventType.HISTORY_ADDED
        assert EventType("bookmark_deleted") == EventType.BOOKMARK_DELETED

    def test_event_type_invalid_value(self):
        """Test invalid EventType value raises ValueError."""
        with pytest.raises(ValueError):
            EventType("invalid_event_type")


class TestHistoryEvent:
    """Tests for HistoryEvent dataclass."""

    def test_history_event_creation(self):
        """Test creating a basic HistoryEvent."""
        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
        )
        assert event.event_type == EventType.HISTORY_ADDED
        assert event.browser == "chrome"
        assert event.timestamp is not None
        assert event.data == {}
        assert event.source_url is None
        assert event.visit_count == 0

    def test_history_event_with_all_fields(self):
        """Test creating HistoryEvent with all fields."""
        ts = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        event = HistoryEvent(
            event_type=EventType.HISTORY_DELETED,
            browser="firefox",
            timestamp=ts,
            data={"url": "https://example.com"},
            source_url="https://example.com/page",
            visit_count=5,
        )
        assert event.event_type == EventType.HISTORY_DELETED
        assert event.browser == "firefox"
        assert event.timestamp == ts
        assert event.data == {"url": "https://example.com"}
        assert event.source_url == "https://example.com/page"
        assert event.visit_count == 5

    def test_history_event_to_dict(self):
        """Test HistoryEvent.to_dict() method."""
        event = HistoryEvent(
            event_type=EventType.BOOKMARK_ADDED,
            browser="chrome",
            data={"title": "Test Bookmark"},
            visit_count=1,
        )
        result = event.to_dict()
        assert result["event_type"] == "bookmark_added"
        assert result["browser"] == "chrome"
        assert result["data"] == {"title": "Test Bookmark"}
        assert result["visit_count"] == 1
        assert "timestamp" in result


class TestSubscription:
    """Tests for Subscription dataclass."""

    def test_subscription_creation(self):
        """Test creating a basic Subscription."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id-123",
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        assert sub.id == "test-id-123"
        assert sub.browser == "chrome"
        assert sub.event_types == [EventType.HISTORY_ADDED]
        assert sub.callback is callback
        assert sub.created_at is not None
        assert sub.last_event is None
        assert sub.event_count == 0

    def test_subscription_matches_same_browser_and_event(self):
        """Test Subscription.matches() returns True for matching event."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id",
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED, EventType.HISTORY_DELETED],
            callback=callback,
        )
        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
        )
        assert sub.matches(event) is True

    def test_subscription_matches_different_browser(self):
        """Test Subscription.matches() returns False for different browser."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id",
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="firefox",
        )
        assert sub.matches(event) is False

    def test_subscription_matches_different_event_type(self):
        """Test Subscription.matches() returns False for different event type."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id",
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        event = HistoryEvent(
            event_type=EventType.BOOKMARK_ADDED,
            browser="chrome",
        )
        assert sub.matches(event) is False

    def test_subscription_matches_case_insensitive_browser(self):
        """Test Subscription.matches() is case-insensitive for browser."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id",
            browser="Chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
        )
        assert sub.matches(event) is True

    def test_subscription_mark_event(self):
        """Test Subscription.mark_event() updates last_event and event_count."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id",
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        assert sub.event_count == 0
        assert sub.last_event is None

        sub.mark_event()
        assert sub.event_count == 1
        assert sub.last_event is not None

        sub.mark_event()
        assert sub.event_count == 2


class TestSubscriptionInfo:
    """Tests for SubscriptionInfo dataclass."""

    def test_from_subscription(self):
        """Test SubscriptionInfo.from_subscription() class method."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id-456",
            browser="firefox",
            event_types=[EventType.HISTORY_ADDED, EventType.BOOKMARK_ADDED],
            callback=callback,
        )

        info = SubscriptionInfo.from_subscription(sub)

        assert info.id == "test-id-456"
        assert info.browser == "firefox"
        assert info.event_types == ["history_added", "bookmark_added"]
        assert info.created_at is not None
        assert info.last_event is None
        assert info.event_count == 0

    def test_from_subscription_with_marked_event(self):
        """Test from_subscription when subscription has received events."""
        callback = lambda e: None
        sub = Subscription(
            id="test-id-789",
            browser="edge",
            event_types=[EventType.DOWNLOAD_ADDED],
            callback=callback,
        )
        sub.mark_event()
        sub.mark_event()

        info = SubscriptionInfo.from_subscription(sub)

        assert info.id == "test-id-789"
        assert info.event_count == 2
        assert info.last_event is not None


class TestEventStats:
    """Tests for EventStats dataclass."""

    def test_event_stats_default_values(self):
        """Test EventStats with default values."""
        stats = EventStats()
        assert stats.total_events == 0
        assert stats.events_by_type == {}
        assert stats.events_by_browser == {}
        assert stats.active_subscriptions == 0
        assert stats.last_event_time is None

    def test_event_stats_with_values(self):
        """Test EventStats with populated values."""
        stats = EventStats(
            total_events=100,
            events_by_type={"history_added": 50, "bookmark_added": 50},
            events_by_browser={"chrome": 60, "firefox": 40},
            active_subscriptions=5,
            last_event_time="2024-01-15T10:30:00",
        )
        assert stats.total_events == 100
        assert stats.events_by_type["history_added"] == 50
        assert stats.events_by_browser["chrome"] == 60
        assert stats.active_subscriptions == 5

    def test_event_stats_to_dict(self):
        """Test EventStats.to_dict() method."""
        stats = EventStats(
            total_events=25,
            events_by_type={"history_added": 25},
            events_by_browser={"chrome": 25},
            active_subscriptions=2,
        )
        result = stats.to_dict()
        assert result["total_events"] == 25
        assert result["events_by_type"] == {"history_added": 25}
        assert result["events_by_browser"] == {"chrome": 25}
        assert result["active_subscriptions"] == 2
