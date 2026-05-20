"""Tests for webhooks module.

This module tests the WebhookManager and related webhook functionality.
"""

import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.ci_excluded

from chronicle_mcp.webhooks import (
    Webhook,
    WebhookEvent,
    WebhookManager,
    notify_history_deleted,
    notify_new_history,
    webhook_manager,
)


class TestWebhook:
    """Tests for Webhook dataclass."""

    def test_webhook_creation(self):
        """Test webhook creation with default values."""
        webhook = Webhook(
            id="test-id",
            url="https://example.com/webhook",
            events=["history.new", "history.deleted"],
            created_at=datetime.now(timezone.utc),
        )
        assert webhook.id == "test-id"
        assert webhook.url == "https://example.com/webhook"
        assert webhook.events == ["history.new", "history.deleted"]
        assert webhook.enabled is True
        assert webhook.secret is None
        assert webhook.failure_count == 0
        assert webhook.last_triggered is None

    def test_webhook_with_secret(self):
        """Test webhook with secret."""
        webhook = Webhook(
            id="test-id",
            url="https://example.com/webhook",
            events=["history.new"],
            created_at=datetime.now(timezone.utc),
            secret="my-secret-key",
        )
        assert webhook.secret == "my-secret-key"

    def test_webhook_disabled(self):
        """Test disabled webhook."""
        webhook = Webhook(
            id="test-id",
            url="https://example.com/webhook",
            events=["history.new"],
            created_at=datetime.now(timezone.utc),
            enabled=False,
        )
        assert webhook.enabled is False


class TestWebhookEvent:
    """Tests for WebhookEvent dataclass."""

    def test_event_creation(self):
        """Test webhook event creation."""
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome", "url": "https://example.com"},
            timestamp=datetime.now(timezone.utc),
            webhook_id="webhook-id",
        )
        assert event.id == "event-id"
        assert event.event_type == "history.new"
        assert event.payload["browser"] == "chrome"
        assert event.webhook_id == "webhook-id"


class TestWebhookManagerInitialization:
    """Tests for WebhookManager initialization."""

    def test_default_initialization(self):
        """Test default manager initialization."""
        manager = WebhookManager()
        assert manager.webhooks == {}
        assert isinstance(manager.event_queue, asyncio.Queue)
        assert manager._running is False
        assert manager._worker_task is None


class TestRegisterWebhook:
    """Tests for register_webhook method."""

    def test_register_basic(self):
        """Test basic webhook registration."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        assert webhook.id in manager.webhooks
        assert manager.webhooks[webhook.id] == webhook
        assert webhook.url == "https://example.com/webhook"
        assert webhook.events == ["history.new"]
        assert webhook.enabled is True

    def test_register_multiple_webhooks(self):
        """Test registering multiple webhooks."""
        manager = WebhookManager()
        webhook1 = manager.register_webhook(
            url="https://example.com/webhook1",
            events=["history.new"],
        )
        webhook2 = manager.register_webhook(
            url="https://example.com/webhook2",
            events=["history.deleted"],
        )
        assert len(manager.webhooks) == 2
        assert webhook1.id != webhook2.id

    def test_register_with_secret(self):
        """Test registering webhook with secret."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
            secret="my-secret",
        )
        assert webhook.secret == "my-secret"


class TestUnregisterWebhook:
    """Tests for unregister_webhook method."""

    def test_unregister_success(self):
        """Test successful unregistration."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        result = manager.unregister_webhook(webhook.id)
        assert result is True
        assert webhook.id not in manager.webhooks

    def test_unregister_nonexistent(self):
        """Test unregistering non-existent webhook."""
        manager = WebhookManager()
        result = manager.unregister_webhook("nonexistent-id")
        assert result is False

    def test_unregister_wrong_id(self):
        """Test unregistering with wrong ID."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        result = manager.unregister_webhook("wrong-id")
        assert result is False
        assert webhook.id in manager.webhooks


class TestGetWebhook:
    """Tests for get_webhook method."""

    def test_get_existing(self):
        """Test getting existing webhook."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        result = manager.get_webhook(webhook.id)
        assert result == webhook

    def test_get_nonexistent(self):
        """Test getting non-existent webhook."""
        manager = WebhookManager()
        result = manager.get_webhook("nonexistent-id")
        assert result is None


class TestListWebhooks:
    """Tests for list_webhooks method."""

    def test_list_empty(self):
        """Test listing when no webhooks."""
        manager = WebhookManager()
        result = manager.list_webhooks()
        assert result == []

    def test_list_multiple(self):
        """Test listing multiple webhooks."""
        manager = WebhookManager()
        webhook1 = manager.register_webhook(
            url="https://example.com/webhook1",
            events=["history.new"],
        )
        webhook2 = manager.register_webhook(
            url="https://example.com/webhook2",
            events=["history.deleted"],
        )
        result = manager.list_webhooks()
        assert len(result) == 2
        assert webhook1 in result
        assert webhook2 in result


class TestTriggerEvent:
    """Tests for trigger_event method."""

    def test_trigger_matching_event(self):
        """Test triggering event that matches webhook."""
        manager = WebhookManager()
        _webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        manager.trigger_event("history.new", {"browser": "chrome"})
        # Event should be queued
        assert manager.event_queue.qsize() == 1

    def test_trigger_non_matching_event(self):
        """Test triggering event that doesn't match webhook."""
        manager = WebhookManager()
        _webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        manager.trigger_event("history.deleted", {"browser": "chrome"})
        # Event should not be queued
        assert manager.event_queue.qsize() == 0

    def test_trigger_disabled_webhook(self):
        """Test triggering disabled webhook."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        # Disable the webhook after registration
        webhook.enabled = False
        manager.trigger_event("history.new", {"browser": "chrome"})
        # Event should not be queued for disabled webhook
        assert manager.event_queue.qsize() == 0

    def test_trigger_multiple_webhooks(self):
        """Test triggering event for multiple webhooks."""
        manager = WebhookManager()
        _webhook1 = manager.register_webhook(
            url="https://example.com/webhook1",
            events=["history.new"],
        )
        _webhook2 = manager.register_webhook(
            url="https://example.com/webhook2",
            events=["history.new"],
        )
        manager.trigger_event("history.new", {"browser": "chrome"})
        # Should queue one event per matching webhook
        assert manager.event_queue.qsize() == 2


class TestSendWebhook:
    """Tests for _send_webhook method."""

    @pytest.mark.asyncio
    async def test_send_success(self):
        """Test successful webhook delivery."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome"},
            timestamp=datetime.now(timezone.utc),
            webhook_id=webhook.id,
        )

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            result = await manager._send_webhook(webhook, event)
            assert result is True
            assert webhook.failure_count == 0
            assert webhook.last_triggered is not None

    @pytest.mark.asyncio
    async def test_send_failure(self):
        """Test failed webhook delivery."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome"},
            timestamp=datetime.now(timezone.utc),
            webhook_id=webhook.id,
        )

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_post.return_value = mock_response

            result = await manager._send_webhook(webhook, event)
            assert result is False
            assert webhook.failure_count == 1

    @pytest.mark.asyncio
    async def test_send_exception(self):
        """Test webhook delivery with exception."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome"},
            timestamp=datetime.now(timezone.utc),
            webhook_id=webhook.id,
        )

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.side_effect = Exception("Connection failed")

            result = await manager._send_webhook(webhook, event)
            assert result is False
            assert webhook.failure_count == 1

    @pytest.mark.asyncio
    async def test_send_with_secret(self):
        """Test webhook delivery with signature."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
            secret="my-secret",
        )
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome"},
            timestamp=datetime.now(timezone.utc),
            webhook_id=webhook.id,
        )

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            result = await manager._send_webhook(webhook, event)
            assert result is True
            # Verify signature header was added
            call_args = mock_post.call_args
            assert "headers" in call_args.kwargs
            assert "X-Signature" in call_args.kwargs["headers"]


class TestWebhookLifecycle:
    """Tests for webhook manager lifecycle."""

    @pytest.mark.asyncio
    async def test_start_stop(self):
        """Test starting and stopping the manager."""
        manager = WebhookManager()
        manager.start()
        assert manager._running is True
        assert manager._worker_task is not None

        await manager.stop()
        assert manager._running is False

    @pytest.mark.asyncio
    async def test_double_start(self):
        """Test starting manager twice."""
        manager = WebhookManager()
        manager.start()
        first_task = manager._worker_task

        manager.start()  # Should not create new task
        assert manager._worker_task == first_task

        await manager.stop()

    @pytest.mark.asyncio
    async def test_stop_without_start(self):
        """Test stopping without starting."""
        manager = WebhookManager()
        await manager.stop()  # Should not raise
        assert manager._running is False


class TestWebhookWorker:
    """Tests for webhook worker."""

    @pytest.mark.asyncio
    async def test_worker_processes_event(self):
        """Test worker processes queued event."""
        manager = WebhookManager()
        _webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )

        with patch.object(manager, "_send_webhook") as mock_send:
            mock_send.return_value = True
            manager.start()

            # Trigger event
            manager.trigger_event("history.new", {"browser": "chrome"})

            # Wait for processing
            await asyncio.sleep(0.1)

            mock_send.assert_called_once()

        await manager.stop()

    @pytest.mark.asyncio
    async def test_worker_disabled_webhook(self):
        """Test worker skips disabled webhook."""
        manager = WebhookManager()
        webhook = manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        # Disable the webhook after registration
        webhook.enabled = False

        # Manually add event to queue (bypass trigger_event filter)
        event = WebhookEvent(
            id="event-id",
            event_type="history.new",
            payload={"browser": "chrome"},
            timestamp=datetime.now(timezone.utc),
            webhook_id=webhook.id,
        )
        manager.event_queue.put_nowait(event)

        with patch.object(manager, "_send_webhook") as mock_send:
            manager.start()
            await asyncio.sleep(0.1)
            mock_send.assert_not_called()

        await manager.stop()


class TestNotifyFunctions:
    """Tests for notify helper functions."""

    def test_notify_new_history(self):
        """Test notify_new_history function."""
        with patch.object(webhook_manager, "trigger_event") as mock_trigger:
            notify_new_history("chrome", {"url": "https://example.com", "title": "Example"})
            mock_trigger.assert_called_once()
            call_args = mock_trigger.call_args
            assert call_args[0][0] == "history.new"
            payload = call_args[0][1]
            assert payload["browser"] == "chrome"
            assert "entry" in payload

    def test_notify_history_deleted(self):
        """Test notify_history_deleted function."""
        with patch.object(webhook_manager, "trigger_event") as mock_trigger:
            notify_history_deleted("chrome", "test query", 5)
            mock_trigger.assert_called_once()
            call_args = mock_trigger.call_args
            assert call_args[0][0] == "history.deleted"
            payload = call_args[0][1]
            assert payload["browser"] == "chrome"
            assert payload["query"] == "test query"
            assert payload["count"] == 5


class TestDefaultWebhookManager:
    """Tests for default webhook_manager instance."""

    def test_default_manager_exists(self):
        """Test default manager is initialized."""
        assert isinstance(webhook_manager, WebhookManager)

    def test_default_manager_usage(self):
        """Test default manager can be used."""
        webhook = webhook_manager.register_webhook(
            url="https://example.com/webhook",
            events=["history.new"],
        )
        assert webhook.id in webhook_manager.webhooks
        # Cleanup
        webhook_manager.unregister_webhook(webhook.id)
