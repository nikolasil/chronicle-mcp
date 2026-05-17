"""Tests for MCP subscription tools.

These tests verify the subscription/unsubscription MCP tools work correctly.
"""

from chronicle_mcp.protocols.mcp import (
    get_subscription_status,
    subscribe_to_history,
    unsubscribe_from_history,
)


class TestSubscribeHistoryMCP:
    """Tests for subscribe_to_history MCP tool."""

    def test_subscribe_basic(self, monkeypatch):
        """Test basic subscription."""
        from chronicle_mcp.core import services

        def mock_subscribe(*args, **kwargs):
            return {
                "subscription_id": "test-sub-123",
                "browser": "chrome",
                "event_types": ["history_added", "history_deleted"],
                "status": "active",
                "message": "Subscribed to history changes",
            }

        monkeypatch.setattr(services.HistoryService, "subscribe_history_changes", mock_subscribe)

        result = subscribe_to_history(browser="chrome")
        assert "test-sub-123" in result
        assert "chrome" in result

    def test_subscribe_with_event_types(self, monkeypatch):
        """Test subscription with specific event types."""
        from chronicle_mcp.core import services

        def mock_subscribe(*args, **kwargs):
            return {
                "subscription_id": "test-sub-456",
                "browser": "chrome",
                "event_types": ["history_added"],
                "status": "active",
                "message": "Subscribed to history changes",
            }

        monkeypatch.setattr(services.HistoryService, "subscribe_history_changes", mock_subscribe)

        result = subscribe_to_history(browser="chrome", event_types=["history_added"])
        assert "test-sub-456" in result

    def test_subscribe_invalid_event_type(self, monkeypatch):
        """Test subscription with invalid event type."""
        from chronicle_mcp.core import services
        from chronicle_mcp.core.exceptions import ValidationError

        def mock_subscribe(*args, **kwargs):
            raise ValidationError("Invalid event type: invalid_type")

        monkeypatch.setattr(services.HistoryService, "subscribe_history_changes", mock_subscribe)

        result = subscribe_to_history(browser="chrome", event_types=["invalid_type"])
        assert "error" in result.lower() or "Error" in result

    def test_subscribe_unexpected_error(self, monkeypatch):
        """Test subscription with unexpected error."""
        from chronicle_mcp.core import services

        def mock_subscribe(*args, **kwargs):
            raise RuntimeError("Database error")

        monkeypatch.setattr(services.HistoryService, "subscribe_history_changes", mock_subscribe)

        result = subscribe_to_history(browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestUnsubscribeHistoryMCP:
    """Tests for unsubscribe_from_history MCP tool."""

    def test_unsubscribe_basic(self, monkeypatch):
        """Test basic unsubscription."""
        from chronicle_mcp.core import services

        def mock_unsubscribe(*args, **kwargs):
            return {
                "success": True,
                "subscription_id": "test-sub-123",
                "message": "Unsubscribed from history changes",
            }

        monkeypatch.setattr(
            services.HistoryService, "unsubscribe_history_changes", mock_unsubscribe
        )

        result = unsubscribe_from_history(subscription_id="test-sub-123")
        assert "test-sub-123" in result

    def test_unsubscribe_nonexistent(self, monkeypatch):
        """Test unsubscription of nonexistent subscription."""
        from chronicle_mcp.core import services
        from chronicle_mcp.core.exceptions import ServiceError

        def mock_unsubscribe(*args, **kwargs):
            raise ServiceError("Subscription not found")

        monkeypatch.setattr(
            services.HistoryService, "unsubscribe_history_changes", mock_unsubscribe
        )

        result = unsubscribe_from_history(subscription_id="nonexistent")
        assert "error" in result.lower() or "Error" in result or "not found" in result.lower()

    def test_unsubscribe_unexpected_error(self, monkeypatch):
        """Test unsubscription with unexpected error."""
        from chronicle_mcp.core import services

        def mock_unsubscribe(*args, **kwargs):
            raise Exception("Unexpected error")

        monkeypatch.setattr(
            services.HistoryService, "unsubscribe_history_changes", mock_unsubscribe
        )

        result = unsubscribe_from_history(subscription_id="test-sub-123")
        assert "error" in result.lower() or "Error" in result


class TestGetSubscriptionStatusMCP:
    """Tests for get_subscription_status MCP tool."""

    def test_get_status_with_subscription(self, monkeypatch):
        """Test getting status of existing subscription."""
        from chronicle_mcp.core import services

        def mock_get_status(*args, **kwargs):
            return {
                "subscription_id": "test-sub-123",
                "browser": "chrome",
                "event_types": ["history_added", "history_deleted"],
                "status": "active",
                "last_event": "2024-01-01T12:00:00Z",
                "event_count": 42,
            }

        monkeypatch.setattr(services.HistoryService, "get_subscription_status", mock_get_status)

        result = get_subscription_status(subscription_id="test-sub-123")
        assert "test-sub-123" in result
        assert "active" in result

    def test_get_status_nonexistent(self, monkeypatch):
        """Test getting status of nonexistent subscription."""
        from chronicle_mcp.core import services
        from chronicle_mcp.core.exceptions import ServiceError

        def mock_get_status(*args, **kwargs):
            raise ServiceError("Subscription not found")

        monkeypatch.setattr(services.HistoryService, "get_subscription_status", mock_get_status)

        result = get_subscription_status(subscription_id="nonexistent")
        assert "error" in result.lower() or "Error" in result or "not found" in result.lower()

    def test_get_status_unexpected_error(self, monkeypatch):
        """Test getting status with unexpected error."""
        from chronicle_mcp.core import services

        def mock_get_status(*args, **kwargs):
            raise RuntimeError("Database error")

        monkeypatch.setattr(services.HistoryService, "get_subscription_status", mock_get_status)

        result = get_subscription_status(subscription_id="test-sub-123")
        assert "error" in result.lower() or "Error" in result
