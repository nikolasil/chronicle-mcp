"""Tests for MCP protocol tools.

These tests verify the MCP tool functions for bookmarks and downloads.
"""

from chronicle_mcp.core.exceptions import BrowserNotFoundError
from chronicle_mcp.protocols.mcp import (
    get_bookmarks,
    get_downloads,
    list_available_bookmarks,
    list_available_downloads,
)


class TestListAvailableBookmarksMCP:
    """Tests for list_available_bookmarks MCP tool."""

    def test_list_available_bookmarks(self):
        """Test listing available bookmarks."""
        # Access the underlying function via .fn attribute
        result = list_available_bookmarks.fn()
        assert isinstance(result, str)

    def test_list_available_bookmarks_error(self, monkeypatch):
        """Test error handling for list_available_bookmarks."""
        from chronicle_mcp.core import services

        def mock_list_available_bookmarks():
            raise Exception("Test error")

        monkeypatch.setattr(
            services.HistoryService, "list_available_bookmarks", mock_list_available_bookmarks
        )

        result = list_available_bookmarks.fn()
        assert "error" in result.lower() or "Error" in result


class TestListAvailableDownloadsMCP:
    """Tests for list_available_downloads MCP tool."""

    def test_list_available_downloads(self):
        """Test listing available downloads."""
        result = list_available_downloads.fn()
        assert isinstance(result, str)

    def test_list_available_downloads_error(self, monkeypatch):
        """Test error handling for list_available_downloads."""
        from chronicle_mcp.core import services

        def mock_list_available_downloads():
            raise Exception("Test error")

        monkeypatch.setattr(
            services.HistoryService, "list_available_downloads", mock_list_available_downloads
        )

        result = list_available_downloads.fn()
        assert "error" in result.lower() or "Error" in result


class TestGetBookmarksMCP:
    """Tests for get_bookmarks MCP tool."""

    def test_get_bookmarks_not_found(self, monkeypatch):
        """Test get_bookmarks when browser not found."""
        from chronicle_mcp.core import services

        def mock_get_bookmarks(*args, **kwargs):
            raise BrowserNotFoundError("chrome")

        monkeypatch.setattr(services.HistoryService, "get_bookmarks", mock_get_bookmarks)

        result = get_bookmarks.fn(browser="chrome")
        assert "could not find" in result.lower()

    def test_get_bookmarks_validation_error(self, monkeypatch):
        """Test get_bookmarks with validation error."""
        from chronicle_mcp.core import validation

        def mock_validate_browser(browser):
            raise validation.ValidationError(f"Invalid browser: {browser}")

        monkeypatch.setattr(validation, "validate_browser", mock_validate_browser)

        result = get_bookmarks.fn(browser="invalid")
        assert "invalid" in result.lower() or "Invalid" in result

    def test_get_bookmarks_with_query(self, monkeypatch):
        """Test get_bookmarks with query parameter."""
        from chronicle_mcp.core import services

        def mock_get_bookmarks(*args, **kwargs):
            return {
                "results": [("GitHub", "https://github.com")],
                "count": 1,
                "browser": "chrome",
                "message": "Found 1 bookmarks",
            }

        monkeypatch.setattr(services.HistoryService, "get_bookmarks", mock_get_bookmarks)

        result = get_bookmarks.fn(query="github", browser="chrome")
        assert isinstance(result, str)

    def test_get_bookmarks_unexpected_error(self, monkeypatch):
        """Test get_bookmarks with unexpected error."""
        from chronicle_mcp.core import services

        def mock_get_bookmarks(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(services.HistoryService, "get_bookmarks", mock_get_bookmarks)

        result = get_bookmarks.fn(browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestGetDownloadsMCP:
    """Tests for get_downloads MCP tool."""

    def test_get_downloads_not_found(self, monkeypatch):
        """Test get_downloads when browser not found."""
        from chronicle_mcp.core import services

        def mock_get_downloads(*args, **kwargs):
            raise BrowserNotFoundError("chrome")

        monkeypatch.setattr(services.HistoryService, "get_downloads", mock_get_downloads)

        result = get_downloads.fn(browser="chrome")
        assert "could not find" in result.lower()

    def test_get_downloads_validation_error(self, monkeypatch):
        """Test get_downloads with validation error."""
        from chronicle_mcp.core import validation

        def mock_validate_browser(browser):
            raise validation.ValidationError(f"Invalid browser: {browser}")

        monkeypatch.setattr(validation, "validate_browser", mock_validate_browser)

        result = get_downloads.fn(browser="invalid")
        assert "invalid" in result.lower() or "Invalid" in result

    def test_get_downloads_with_query(self, monkeypatch):
        """Test get_downloads with query parameter."""
        from chronicle_mcp.core import services

        def mock_get_downloads(*args, **kwargs):
            return {
                "results": [("test.pdf", "https://example.com/test.pdf", "2024-01-01")],
                "count": 1,
                "browser": "chrome",
                "message": "Found 1 downloads",
            }

        monkeypatch.setattr(services.HistoryService, "get_downloads", mock_get_downloads)

        result = get_downloads.fn(query="pdf", browser="chrome")
        assert isinstance(result, str)

    def test_get_downloads_unexpected_error(self, monkeypatch):
        """Test get_downloads with unexpected error."""
        from chronicle_mcp.core import services

        def mock_get_downloads(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(services.HistoryService, "get_downloads", mock_get_downloads)

        result = get_downloads.fn(browser="chrome")
        assert "error" in result.lower() or "Error" in result
