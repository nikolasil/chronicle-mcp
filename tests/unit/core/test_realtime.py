"""Tests for SubscriptionManager in chronicle_mcp.core.realtime."""

from unittest.mock import MagicMock

import pytest

from chronicle_mcp.core.events import (
    EventType,
    HistoryEvent,
)
from chronicle_mcp.core.realtime import (
    EventBroadcaster,
    SubscriptionManager,
    get_subscription_manager,
    reset_subscription_manager,
)


class TestSubscriptionManager:
    """Tests for SubscriptionManager class."""

    @pytest.fixture
    def manager(self):
        """Create a fresh SubscriptionManager for each test."""
        return SubscriptionManager(max_subscriptions=10, max_queue_size=100)

    @pytest.fixture
    def callback(self):
        """Create a simple callback for testing."""
        return MagicMock()

    def test_subscribe_basic(self, manager, callback):
        """Test basic subscription creation."""
        sub_id = manager.subscribe(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        assert sub_id is not None
        assert len(sub_id) > 0
        assert manager.get_active_count() == 1

    def test_subscribe_multiple_browsers(self, manager, callback):
        """Test subscribing to multiple browsers."""
        sub_id1 = manager.subscribe(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        sub_id2 = manager.subscribe(
            browser="firefox",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        assert sub_id1 != sub_id2
        assert manager.get_active_count() == 2

    def test_subscribe_multiple_event_types(self, manager, callback):
        """Test subscribing to multiple event types."""
        sub_id = manager.subscribe(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED, EventType.BOOKMARK_ADDED],
            callback=callback,
        )
        assert sub_id is not None
        assert manager.get_active_count() == 1

    def test_subscribe_empty_event_types_raises(self, manager, callback):
        """Test that empty event_types raises ValueError."""
        with pytest.raises(ValueError, match="At least one event type is required"):
            manager.subscribe(
                browser="chrome",
                event_types=[],
                callback=callback,
            )

    def test_subscribe_max_reached_raises(self, manager, callback):
        """Test that max subscriptions raises RuntimeError."""
        manager = SubscriptionManager(max_subscriptions=2, max_queue_size=100)

        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        with pytest.raises(RuntimeError, match="Maximum subscriptions"):
            manager.subscribe(
                browser="edge", event_types=[EventType.HISTORY_ADDED], callback=callback
            )

    def test_unsubscribe_existing(self, manager, callback):
        """Test unsubscribing an existing subscription."""
        sub_id = manager.subscribe(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )
        assert manager.get_active_count() == 1

        result = manager.unsubscribe(sub_id)
        assert result is True
        assert manager.get_active_count() == 0

    def test_unsubscribe_nonexistent(self, manager):
        """Test unsubscribing a non-existent subscription returns False."""
        result = manager.unsubscribe("nonexistent-id")
        assert result is False

    def test_unsubscribe_all_no_filter(self, manager, callback):
        """Test unsubscribe_all without filter removes all subscriptions."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(browser="edge", event_types=[EventType.HISTORY_ADDED], callback=callback)

        assert manager.get_active_count() == 3
        count = manager.unsubscribe_all()
        assert count == 3
        assert manager.get_active_count() == 0

    def test_unsubscribe_all_with_browser_filter(self, manager, callback):
        """Test unsubscribe_all with browser filter."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="chrome", event_types=[EventType.BOOKMARK_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        assert manager.get_active_count() == 3
        count = manager.unsubscribe_all(browser="chrome")
        assert count == 2
        assert manager.get_active_count() == 1

    def test_publish_event_to_matching(self, manager, callback):
        """Test publish_event delivers to matching subscriptions."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
            data={"url": "https://example.com"},
        )
        sent_count = manager.publish_event(event)

        assert sent_count == 1
        callback.assert_called_once_with(event)

    def test_publish_event_no_match_browser(self, manager, callback):
        """Test publish_event does not deliver to non-matching browser."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="firefox",
            data={"url": "https://example.com"},
        )
        sent_count = manager.publish_event(event)

        assert sent_count == 0
        callback.assert_not_called()

    def test_publish_event_no_match_event_type(self, manager, callback):
        """Test publish_event does not deliver to non-matching event type."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        event = HistoryEvent(
            event_type=EventType.BOOKMARK_ADDED,
            browser="chrome",
            data={"url": "https://example.com"},
        )
        sent_count = manager.publish_event(event)

        assert sent_count == 0
        callback.assert_not_called()

    def test_publish_event_updates_stats(self, manager, callback):
        """Test publish_event updates EventStats."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )

        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
        )
        manager.publish_event(event)

        stats = manager.get_stats()
        assert stats.total_events == 1
        assert stats.events_by_type["history_added"] == 1
        assert stats.events_by_browser["chrome"] == 1
        assert stats.last_event_time is not None

    def test_publish_event_delivers_to_multiple_matching_subscriptions(self, manager):
        """Test publish_event delivers to all matching subscriptions (async callback test)."""
        received_events = []

        def callback1(event):
            received_events.append(("cb1", event))

        def callback2(event):
            received_events.append(("cb2", event))

        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback1
        )
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback2
        )

        event = HistoryEvent(
            event_type=EventType.HISTORY_ADDED,
            browser="chrome",
        )
        sent_count = manager.publish_event(event)

        assert sent_count == 2

        import time
        time.sleep(0.2)

        assert ("cb1", event) in received_events
        assert ("cb2", event) in received_events

    def test_get_subscription_existing(self, manager, callback):
        """Test get_subscription returns info for existing subscription."""
        sub_id = manager.subscribe(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=callback,
        )

        info = manager.get_subscription(sub_id)
        assert info is not None
        assert info.id == sub_id
        assert info.browser == "chrome"
        assert info.event_types == ["history_added"]

    def test_get_subscription_nonexistent(self, manager):
        """Test get_subscription returns None for non-existent subscription."""
        info = manager.get_subscription("nonexistent-id")
        assert info is None

    def test_get_subscriptions_no_filter(self, manager, callback):
        """Test get_subscriptions without filter returns all."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_DELETED], callback=callback
        )

        subs = manager.get_subscriptions()
        assert len(subs) == 2

    def test_get_subscriptions_browser_filter(self, manager, callback):
        """Test get_subscriptions with browser filter."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="chrome", event_types=[EventType.BOOKMARK_ADDED], callback=callback
        )

        subs = manager.get_subscriptions(browser="chrome")
        assert len(subs) == 2
        for sub in subs:
            assert sub.browser == "chrome"

    def test_get_subscriptions_event_type_filter(self, manager, callback):
        """Test get_subscriptions with event type filter."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_DELETED], callback=callback
        )

        subs = manager.get_subscriptions(event_type=EventType.HISTORY_DELETED)
        assert len(subs) == 1
        assert subs[0].browser == "firefox"

    def test_get_stats(self, manager, callback):
        """Test get_stats returns correct statistics."""
        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_DELETED], callback=callback
        )

        stats = manager.get_stats()
        assert stats.active_subscriptions == 2
        assert stats.total_events == 0

    def test_get_active_count(self, manager, callback):
        """Test get_active_count returns correct count."""
        assert manager.get_active_count() == 0

        manager.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        assert manager.get_active_count() == 1

        manager.subscribe(
            browser="firefox", event_types=[EventType.HISTORY_ADDED], callback=callback
        )
        assert manager.get_active_count() == 2

        manager.unsubscribe(manager.get_subscriptions()[0].id)
        assert manager.get_active_count() == 1


class TestGlobalSubscriptionManager:
    """Tests for global subscription manager functions."""

    def test_get_subscription_manager_returns_singleton(self):
        """Test get_subscription_manager returns same instance."""
        reset_subscription_manager()
        manager1 = get_subscription_manager()
        manager2 = get_subscription_manager()
        assert manager1 is manager2

    def test_reset_subscription_manager_clears_subscriptions(self):
        """Test reset_subscription_manager clears and recreates manager."""
        manager1 = get_subscription_manager()
        manager1.subscribe(
            browser="chrome", event_types=[EventType.HISTORY_ADDED], callback=lambda e: None
        )
        assert manager1.get_active_count() == 1

        reset_subscription_manager()
        manager2 = get_subscription_manager()

        assert manager2 is not manager1
        assert manager2.get_active_count() == 0


class TestEventBroadcaster:
    """Tests for EventBroadcaster class."""

    @pytest.fixture
    def broadcaster(self):
        """Create a broadcaster with a fresh manager."""
        manager = SubscriptionManager()
        return EventBroadcaster(manager), manager

    def test_broadcaster_connect(self, broadcaster):
        """Test EventBroadcaster.connect() creates connection."""
        broadcaster, manager = broadcaster

        async def test():
            conn_id = await broadcaster.connect(
                browser="chrome",
                event_types=[EventType.HISTORY_ADDED],
            )
            assert conn_id is not None
            assert manager.get_active_count() == 1

        import asyncio

        asyncio.run(test())

    def test_broadcaster_disconnect(self, broadcaster):
        """Test EventBroadcaster.disconnect() removes connection."""
        broadcaster, manager = broadcaster

        async def test():
            conn_id = await broadcaster.connect(
                browser="chrome",
                event_types=[EventType.HISTORY_ADDED],
            )
            assert manager.get_active_count() == 1

            await broadcaster.disconnect(conn_id)
            assert manager.get_active_count() == 0

        import asyncio

        asyncio.run(test())

    def test_broadcaster_disconnect_nonexistent(self, broadcaster):
        """Test disconnecting non-existent connection is safe."""
        broadcaster, _ = broadcaster

        async def test():
            await broadcaster.disconnect("nonexistent-id")

        import asyncio

        asyncio.run(test())
