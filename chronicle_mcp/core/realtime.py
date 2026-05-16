"""Real-time history update subscription manager.

This module provides WebSocket/SSE-based subscription for real-time
history change notifications.
"""

import asyncio
import logging
import threading
import uuid
from collections import defaultdict
from collections.abc import AsyncIterator, Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from chronicle_mcp.core.events import (
    EventStats,
    EventType,
    HistoryEvent,
    Subscription,
    SubscriptionInfo,
)

logger = logging.getLogger(__name__)


class SubscriptionManager:
    """Manages subscriptions for real-time history updates.

    This class is thread-safe and supports multiple concurrent subscribers.
    """

    def __init__(self, max_subscriptions: int = 100, max_queue_size: int = 1000):
        """Initialize subscription manager.

        Args:
            max_subscriptions: Maximum number of concurrent subscriptions
            max_queue_size: Maximum queue size per subscription
        """
        self._subscriptions: dict[str, Subscription] = {}
        self._browser_subscriptions: dict[str, set[str]] = defaultdict(set)
        self._lock = threading.RLock()
        self._max_subscriptions = max_subscriptions
        self._max_queue_size = max_queue_size
        self._stats = EventStats()
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="event_handler_")

    def subscribe(
        self,
        browser: str,
        event_types: list[EventType],
        callback: Callable[[HistoryEvent], None],
    ) -> str:
        """Subscribe to history events.

        Args:
            browser: Browser name to subscribe to
            event_types: List of event types to receive
            callback: Callback function to receive events

        Returns:
            Subscription ID

        Raises:
            ValueError: If no event types provided
            RuntimeError: If max subscriptions reached
        """
        if not event_types:
            raise ValueError("At least one event type is required")

        with self._lock:
            if len(self._subscriptions) >= self._max_subscriptions:
                raise RuntimeError(f"Maximum subscriptions ({self._max_subscriptions}) reached")

            sub_id = str(uuid.uuid4())
            subscription = Subscription(
                id=sub_id,
                browser=browser,
                event_types=event_types,
                callback=callback,
            )
            self._subscriptions[sub_id] = subscription
            self._browser_subscriptions[browser.lower()].add(sub_id)
            self._stats.active_subscriptions = len(self._subscriptions)

            logger.info(f"Created subscription {sub_id} for browser {browser}")
            return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from history events.

        Args:
            subscription_id: ID of subscription to remove

        Returns:
            True if subscription was found and removed
        """
        with self._lock:
            if subscription_id not in self._subscriptions:
                return False

            subscription = self._subscriptions[subscription_id]
            del self._subscriptions[subscription_id]
            self._browser_subscriptions[subscription.browser.lower()].discard(subscription_id)
            self._stats.active_subscriptions = len(self._subscriptions)

            logger.info(f"Removed subscription {subscription_id}")
            return True

    def unsubscribe_all(self, browser: str | None = None) -> int:
        """Unsubscribe all subscriptions.

        Args:
            browser: Optional browser filter. If None, removes all.

        Returns:
            Number of subscriptions removed
        """
        with self._lock:
            if browser is None:
                count = len(self._subscriptions)
                self._subscriptions.clear()
                self._browser_subscriptions.clear()
            else:
                sub_ids = list(self._browser_subscriptions.get(browser.lower(), set()))
                count = len(sub_ids)
                for sub_id in sub_ids:
                    if sub_id in self._subscriptions:
                        del self._subscriptions[sub_id]
                self._browser_subscriptions[browser.lower()].clear()

            self._stats.active_subscriptions = len(self._subscriptions)
            return count

    def publish_event(self, event: HistoryEvent) -> int:
        """Publish an event to matching subscriptions.

        Args:
            event: Event to publish

        Returns:
            Number of subscriptions that received the event
        """
        with self._lock:
            matching_subs = [sub for sub in self._subscriptions.values() if sub.matches(event)]

        sent_count = 0
        for subscription in matching_subs:
            try:
                self._executor.submit(subscription.callback, event)
                subscription.mark_event()
                sent_count += 1

                self._stats.total_events += 1
                etype = event.event_type.value
                self._stats.events_by_type[etype] = self._stats.events_by_type.get(etype, 0) + 1
                browser = event.browser.lower()
                self._stats.events_by_browser[browser] = (
                    self._stats.events_by_browser.get(browser, 0) + 1
                )
                self._stats.last_event_time = datetime.utcnow().isoformat()

            except Exception as e:
                logger.warning(f"Failed to deliver event to subscription {subscription.id}: {e}")

        return sent_count

    def get_subscription(self, subscription_id: str) -> SubscriptionInfo | None:
        """Get information about a subscription.

        Args:
            subscription_id: ID of subscription

        Returns:
            SubscriptionInfo or None if not found
        """
        with self._lock:
            sub = self._subscriptions.get(subscription_id)
            return SubscriptionInfo.from_subscription(sub) if sub else None

    def get_subscriptions(
        self,
        browser: str | None = None,
        event_type: EventType | None = None,
    ) -> list[SubscriptionInfo]:
        """Get list of subscriptions with optional filtering.

        Args:
            browser: Optional browser filter
            event_type: Optional event type filter

        Returns:
            List of matching SubscriptionInfo objects
        """
        with self._lock:
            subs = list(self._subscriptions.values())

        if browser is not None:
            subs = [s for s in subs if s.browser.lower() == browser.lower()]

        if event_type is not None:
            subs = [s for s in subs if event_type in s.event_types]

        return [SubscriptionInfo.from_subscription(s) for s in subs]

    def get_stats(self) -> EventStats:
        """Get event statistics.

        Returns:
            EventStats object
        """
        with self._lock:
            return EventStats(
                total_events=self._stats.total_events,
                events_by_type=dict(self._stats.events_by_type),
                events_by_browser=dict(self._stats.events_by_browser),
                active_subscriptions=len(self._subscriptions),
                last_event_time=self._stats.last_event_time,
            )

    def get_active_count(self) -> int:
        """Get count of active subscriptions."""
        with self._lock:
            return len(self._subscriptions)


class EventBroadcaster:
    """Broadcasts events to multiple async consumers (SSE/WebSocket)."""

    def __init__(self, subscription_manager: SubscriptionManager):
        """Initialize broadcaster.

        Args:
            subscription_manager: Manager to use for subscriptions
        """
        self._manager = subscription_manager
        self._queues: dict[str, asyncio.Queue] = {}
        self._lock = asyncio.Lock()

    async def connect(
        self,
        browser: str,
        event_types: list[EventType],
    ) -> str:
        """Connect an async consumer.

        Args:
            browser: Browser to subscribe to
            event_types: Event types to receive

        Returns:
            Connection ID
        """
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)

        def sync_callback(event: HistoryEvent) -> None:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass

        loop = asyncio.get_event_loop()
        conn_id = await loop.run_in_executor(
            None,
            lambda: self._manager.subscribe(browser, event_types, sync_callback),
        )

        async with self._lock:
            self._queues[conn_id] = queue

        return conn_id

    async def disconnect(self, connection_id: str) -> None:
        """Disconnect an async consumer.

        Args:
            connection_id: Connection ID returned from connect
        """
        async with self._lock:
            if connection_id in self._queues:
                del self._queues[connection_id]

        await asyncio.get_event_loop().run_in_executor(
            None, self._manager.unsubscribe, connection_id
        )

    async def get_event(self, connection_id: str, timeout: float = 30.0) -> HistoryEvent | None:
        """Get next event for a connection.

        Args:
            connection_id: Connection ID
            timeout: Timeout in seconds

        Returns:
            HistoryEvent or None if timeout
        """
        async with self._lock:
            queue = self._queues.get(connection_id)

        if queue is None:
            return None

        try:
            return await asyncio.wait_for(queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def stream_events(self, connection_id: str) -> AsyncIterator[HistoryEvent]:
        """Async generator for streaming events.

        Args:
            connection_id: Connection ID

        Yields:
            HistoryEvent objects
        """
        while True:
            event = await self.get_event(connection_id, timeout=60.0)
            if event is None:
                break
            yield event


_global_subscription_manager: SubscriptionManager | None = None


def get_subscription_manager() -> SubscriptionManager:
    """Get the global subscription manager instance."""
    global _global_subscription_manager
    if _global_subscription_manager is None:
        _global_subscription_manager = SubscriptionManager()
    return _global_subscription_manager


def reset_subscription_manager() -> None:
    """Reset the global subscription manager (for testing)."""
    global _global_subscription_manager
    if _global_subscription_manager is not None:
        _global_subscription_manager.unsubscribe_all()
    _global_subscription_manager = None
