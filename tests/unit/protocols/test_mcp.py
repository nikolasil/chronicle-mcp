"""Tests for MCP protocol tools.

These tests verify the MCP tool functions for bookmarks and downloads.
"""

import pytest

pytestmark = pytest.mark.ci_excluded

from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
    ServiceError,
    ValidationError,
)
from chronicle_mcp.protocols.mcp import (
    count_visits,
    delete_history,
    export_history,
    get_bookmarks,
    get_browser_stats,
    get_downloads,
    get_most_visited_pages,
    get_recent_history,
    handle_service_error,
    list_available_bookmarks,
    list_available_browsers,
    list_available_downloads,
    list_top_domains,
    search_by_domain,
    search_history,
    search_history_advanced,
    search_history_by_date,
    sync_history,
)


class TestListAvailableBookmarksMCP:
    """Tests for list_available_bookmarks MCP tool."""

    def test_list_available_bookmarks(self):
        """Test listing available bookmarks."""
        result = list_available_bookmarks()
        assert isinstance(result, str)

    def test_list_available_bookmarks_error(self, monkeypatch):
        """Test error handling for list_available_bookmarks."""
        from chronicle_mcp.core import services

        def mock_list_available_bookmarks():
            raise Exception("Test error")

        monkeypatch.setattr(
            services.HistoryService, "list_available_bookmarks", mock_list_available_bookmarks
        )

        result = list_available_bookmarks()
        assert "error" in result.lower() or "Error" in result


class TestListAvailableDownloadsMCP:
    """Tests for list_available_downloads MCP tool."""

    def test_list_available_downloads(self):
        """Test listing available downloads."""
        result = list_available_downloads()
        assert isinstance(result, str)

    def test_list_available_downloads_error(self, monkeypatch):
        """Test error handling for list_available_downloads."""
        from chronicle_mcp.core import services

        def mock_list_available_downloads():
            raise Exception("Test error")

        monkeypatch.setattr(
            services.HistoryService, "list_available_downloads", mock_list_available_downloads
        )

        result = list_available_downloads()
        assert "error" in result.lower() or "Error" in result


class TestGetBookmarksMCP:
    """Tests for get_bookmarks MCP tool."""

    def test_get_bookmarks_not_found(self, monkeypatch):
        """Test get_bookmarks when browser not found."""
        from chronicle_mcp.core import services

        def mock_get_bookmarks(*args, **kwargs):
            raise BrowserNotFoundError("chrome")

        monkeypatch.setattr(services.HistoryService, "get_bookmarks", mock_get_bookmarks)

        result = get_bookmarks(browser="chrome")
        assert "could not find" in result.lower()

    def test_get_bookmarks_validation_error(self, monkeypatch):
        """Test get_bookmarks with validation error."""
        from chronicle_mcp.core import validation

        def mock_validate_browser(browser):
            raise validation.ValidationError(f"Invalid browser: {browser}")

        monkeypatch.setattr(validation, "validate_browser", mock_validate_browser)

        result = get_bookmarks(browser="invalid")
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

        result = get_bookmarks(query="github", browser="chrome")
        assert isinstance(result, str)

    def test_get_bookmarks_unexpected_error(self, monkeypatch):
        """Test get_bookmarks with unexpected error."""
        from chronicle_mcp.core import services

        def mock_get_bookmarks(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(services.HistoryService, "get_bookmarks", mock_get_bookmarks)

        result = get_bookmarks(browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestGetDownloadsMCP:
    """Tests for get_downloads MCP tool."""

    def test_get_downloads_not_found(self, monkeypatch):
        """Test get_downloads when browser not found."""
        from chronicle_mcp.core import services

        def mock_get_downloads(*args, **kwargs):
            raise BrowserNotFoundError("chrome")

        monkeypatch.setattr(services.HistoryService, "get_downloads", mock_get_downloads)

        result = get_downloads(browser="chrome")
        assert "could not find" in result.lower()

    def test_get_downloads_validation_error(self, monkeypatch):
        """Test get_downloads with validation error."""
        from chronicle_mcp.core import validation

        def mock_validate_browser(browser):
            raise validation.ValidationError(f"Invalid browser: {browser}")

        monkeypatch.setattr(validation, "validate_browser", mock_validate_browser)

        result = get_downloads(browser="invalid")
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

        result = get_downloads(query="pdf", browser="chrome")
        assert isinstance(result, str)

    def test_get_downloads_unexpected_error(self, monkeypatch):
        """Test get_downloads with unexpected error."""
        from chronicle_mcp.core import services

        def mock_get_downloads(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(services.HistoryService, "get_downloads", mock_get_downloads)

        result = get_downloads(browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestHandleServiceError:
    """Tests for handle_service_error function."""

    def test_validation_error(self):
        """Test handling ValidationError."""
        error = ValidationError("Invalid input", field="browser")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "Invalid input" in result

    def test_browser_not_found_error(self):
        """Test handling BrowserNotFoundError."""
        error = BrowserNotFoundError("chrome")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "chrome" in result

    def test_database_locked_error(self):
        """Test handling DatabaseLockedError."""
        error = DatabaseLockedError("firefox")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "firefox" in result

    def test_permission_denied_error(self):
        """Test handling PermissionDeniedError."""
        error = PermissionDeniedError("edge", "/path/to/db")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "edge" in result

    def test_database_error(self):
        """Test handling DatabaseError."""
        error = DatabaseError("Query failed")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "Query failed" in result

    def test_generic_service_error(self):
        """Test handling generic ServiceError."""
        error = ServiceError("Service failed", code="CUSTOM_ERROR")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "Service failed" in result

    def test_unexpected_error(self):
        """Test handling unexpected error."""
        error = RuntimeError("Unexpected crash")
        result = handle_service_error(error)
        assert "Error:" in result
        assert "unexpected error occurred" in result.lower()


class TestListAvailableBrowsersMCP:
    """Tests for list_available_browsers MCP tool."""

    def test_list_available_browsers(self, monkeypatch):
        """Test listing available browsers."""
        from chronicle_mcp.core import services

        def mock_list_available_browsers():
            return {
                "browsers": ["chrome", "firefox"],
                "message": "Available browsers: chrome, firefox",
            }

        monkeypatch.setattr(
            services.HistoryService, "list_available_browsers", mock_list_available_browsers
        )

        result = list_available_browsers()
        assert isinstance(result, str)
        assert "chrome" in result.lower() or "firefox" in result.lower()

    def test_list_available_browsers_error(self, monkeypatch):
        """Test error handling."""
        from chronicle_mcp.core import services

        def mock_list_available_browsers():
            raise Exception("Test error")

        monkeypatch.setattr(
            services.HistoryService, "list_available_browsers", mock_list_available_browsers
        )

        result = list_available_browsers()
        assert "error" in result.lower() or "Error" in result


class TestSearchHistoryMCP:
    """Tests for search_history MCP tool."""

    def test_search_history_basic(self, monkeypatch):
        """Test basic search."""
        from chronicle_mcp.core import services

        def mock_search_history(*args, **kwargs):
            return {
                "results": [("Test", "https://example.com", "2024-01-01")],
                "count": 1,
                "query": "test",
                "message": "Found 1 result for 'test'",
            }

        monkeypatch.setattr(services.HistoryService, "search_history", mock_search_history)

        result = search_history(query="test", limit=5, browser="chrome")
        assert isinstance(result, str)
        assert "test" in result.lower()

    def test_search_history_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_search_history(*args, **kwargs):
            raise ValidationError("Invalid browser")

        monkeypatch.setattr(services.HistoryService, "search_history", mock_search_history)

        result = search_history(query="test", browser="invalid")
        assert "error" in result.lower() or "Error" in result

    def test_search_history_browser_not_found(self, monkeypatch):
        """Test when browser not found."""
        from chronicle_mcp.core import services

        def mock_search_history(*args, **kwargs):
            raise BrowserNotFoundError("safari")

        monkeypatch.setattr(services.HistoryService, "search_history", mock_search_history)

        result = search_history(query="test", browser="safari")
        assert "could not find" in result.lower()


class TestGetRecentHistoryMCP:
    """Tests for get_recent_history MCP tool."""

    def test_get_recent_history_basic(self, monkeypatch):
        """Test getting recent history."""
        from chronicle_mcp.core import services

        def mock_get_recent_history(*args, **kwargs):
            return {
                "results": [("Test", "https://example.com", "2024-01-01")],
                "count": 1,
                "hours": 24,
                "message": "History from last 24 hours",
            }

        monkeypatch.setattr(services.HistoryService, "get_recent_history", mock_get_recent_history)

        result = get_recent_history(hours=24, limit=10, browser="chrome")
        assert isinstance(result, str)
        assert "24" in result

    def test_get_recent_history_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_get_recent_history(*args, **kwargs):
            raise ValidationError("Invalid hours")

        monkeypatch.setattr(services.HistoryService, "get_recent_history", mock_get_recent_history)

        result = get_recent_history(hours=0, browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestCountVisitsMCP:
    """Tests for count_visits MCP tool."""

    def test_count_visits_basic(self, monkeypatch):
        """Test counting visits."""
        from chronicle_mcp.core import services

        def mock_count_visits(*args, **kwargs):
            return {
                "domain": "github.com",
                "browser": "chrome",
                "count": 42,
                "message": "github.com has 42 visits in chrome",
            }

        monkeypatch.setattr(services.HistoryService, "count_visits", mock_count_visits)

        result = count_visits(domain="github.com", browser="chrome")
        assert isinstance(result, str)
        assert "github.com" in result
        assert "42" in result

    def test_count_visits_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_count_visits(*args, **kwargs):
            raise ValidationError("Invalid domain")

        monkeypatch.setattr(services.HistoryService, "count_visits", mock_count_visits)

        result = count_visits(domain="", browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestListTopDomainsMCP:
    """Tests for list_top_domains MCP tool."""

    def test_list_top_domains_basic(self, monkeypatch):
        """Test listing top domains."""
        from chronicle_mcp.core import services

        def mock_list_top_domains(*args, **kwargs):
            return {
                "domains": [("github.com", 100), ("stackoverflow.com", 50)],
                "count": 2,
                "message": "Top domains: github.com (100 visits)",
            }

        monkeypatch.setattr(services.HistoryService, "list_top_domains", mock_list_top_domains)

        result = list_top_domains(limit=10, browser="chrome")
        assert isinstance(result, str)

    def test_list_top_domains_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_list_top_domains(*args, **kwargs):
            raise ValidationError("Invalid limit")

        monkeypatch.setattr(services.HistoryService, "list_top_domains", mock_list_top_domains)

        result = list_top_domains(limit=0, browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestSearchHistoryByDateMCP:
    """Tests for search_history_by_date MCP tool."""

    def test_search_by_date_basic(self, monkeypatch):
        """Test searching by date."""
        from chronicle_mcp.core import services

        def mock_search_history_by_date(*args, **kwargs):
            return {
                "results": [("Test", "https://example.com", "2024-01-15")],
                "count": 1,
                "query": "test",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "message": "Found 1 result for 'test'",
            }

        monkeypatch.setattr(
            services.HistoryService, "search_history_by_date", mock_search_history_by_date
        )

        result = search_history_by_date(
            query="test",
            start_date="2024-01-01",
            end_date="2024-01-31",
            limit=10,
            browser="chrome",
        )
        assert isinstance(result, str)

    def test_search_by_date_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_search_history_by_date(*args, **kwargs):
            raise ValidationError("Invalid date")

        monkeypatch.setattr(
            services.HistoryService, "search_history_by_date", mock_search_history_by_date
        )

        result = search_history_by_date(
            query="test", start_date="invalid", end_date="2024-01-31", browser="chrome"
        )
        assert "error" in result.lower() or "Error" in result


class TestDeleteHistoryMCP:
    """Tests for delete_history MCP tool."""

    def test_delete_history_preview(self, monkeypatch):
        """Test delete in preview mode."""
        from chronicle_mcp.core import services

        def mock_delete_history(*args, **kwargs):
            return {
                "preview": True,
                "query": "test",
                "count": 5,
                "message": "Preview: 5 entries would be deleted",
            }

        monkeypatch.setattr(services.HistoryService, "delete_history", mock_delete_history)

        result = delete_history(query="test", limit=100, browser="chrome", confirm=False)
        assert isinstance(result, str)
        assert "preview" in result.lower()

    def test_delete_history_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_delete_history(*args, **kwargs):
            raise ValidationError("Empty query")

        monkeypatch.setattr(services.HistoryService, "delete_history", mock_delete_history)

        result = delete_history(query="", browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestSearchByDomainMCP:
    """Tests for search_by_domain MCP tool."""

    def test_search_by_domain_basic(self, monkeypatch):
        """Test searching by domain."""
        from chronicle_mcp.core import services

        def mock_search_by_domain(*args, **kwargs):
            return {
                "results": [("GitHub", "https://github.com/test", "2024-01-01")],
                "count": 1,
                "domain": "github.com",
                "query": None,
                "message": "Found 1 result in github.com",
            }

        monkeypatch.setattr(services.HistoryService, "search_by_domain", mock_search_by_domain)

        result = search_by_domain(domain="github.com", browser="chrome")
        assert isinstance(result, str)
        assert "github.com" in result.lower()

    def test_search_by_domain_with_query(self, monkeypatch):
        """Test with query parameter."""
        from chronicle_mcp.core import services

        def mock_search_by_domain(*args, **kwargs):
            return {
                "results": [("Claude", "https://github.com/anthropics/claude", "2024-01-01")],
                "count": 1,
                "domain": "github.com",
                "query": "claude",
                "message": "Found 1 result in github.com",
            }

        monkeypatch.setattr(services.HistoryService, "search_by_domain", mock_search_by_domain)

        result = search_by_domain(domain="github.com", query="claude", browser="chrome")
        assert isinstance(result, str)


class TestGetBrowserStatsMCP:
    """Tests for get_browser_stats MCP tool."""

    def test_get_browser_stats_basic(self, monkeypatch):
        """Test getting browser stats."""
        from chronicle_mcp.core import services

        def mock_get_browser_stats(*args, **kwargs):
            return {
                "stats": {
                    "total_entries": 1000,
                    "total_visits": 5000,
                    "unique_urls": 800,
                },
                "message": '{"total_entries": 1000, "total_visits": 5000}',
            }

        monkeypatch.setattr(services.HistoryService, "get_browser_stats", mock_get_browser_stats)

        result = get_browser_stats(browser="chrome")
        assert isinstance(result, str)

    def test_get_browser_stats_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_get_browser_stats(*args, **kwargs):
            raise ValidationError("Invalid browser")

        monkeypatch.setattr(services.HistoryService, "get_browser_stats", mock_get_browser_stats)

        result = get_browser_stats(browser="invalid")
        assert "error" in result.lower() or "Error" in result


class TestGetMostVisitedPagesMCP:
    """Tests for get_most_visited_pages MCP tool."""

    def test_get_most_visited_basic(self, monkeypatch):
        """Test getting most visited pages."""
        from chronicle_mcp.core import services

        def mock_get_most_visited_pages(*args, **kwargs):
            return {
                "pages": [("Home", "https://example.com", 50)],
                "count": 1,
                "message": "Most visited pages: Home (50 visits)",
            }

        monkeypatch.setattr(
            services.HistoryService, "get_most_visited_pages", mock_get_most_visited_pages
        )

        result = get_most_visited_pages(limit=10, browser="chrome")
        assert isinstance(result, str)

    def test_get_most_visited_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_get_most_visited_pages(*args, **kwargs):
            raise ValidationError("Invalid limit")

        monkeypatch.setattr(
            services.HistoryService, "get_most_visited_pages", mock_get_most_visited_pages
        )

        result = get_most_visited_pages(limit=0, browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestExportHistoryMCP:
    """Tests for export_history MCP tool."""

    def test_export_csv(self, monkeypatch):
        """Test exporting to CSV."""
        from chronicle_mcp.core import services

        def mock_export_history(*args, **kwargs):
            return {
                "content": "title,url,timestamp\nTest,https://example.com,2024-01-01",
                "format": "csv",
                "browser": "chrome",
            }

        monkeypatch.setattr(services.HistoryService, "export_history", mock_export_history)

        result = export_history(format_type="csv", limit=100, browser="chrome")
        assert isinstance(result, str)
        assert "title" in result or "csv" in result.lower()

    def test_export_json(self, monkeypatch):
        """Test exporting to JSON."""
        from chronicle_mcp.core import services

        def mock_export_history(*args, **kwargs):
            return {
                "content": '{"entries": [{"title": "Test"}]}',
                "format": "json",
                "browser": "chrome",
            }

        monkeypatch.setattr(services.HistoryService, "export_history", mock_export_history)

        result = export_history(format_type="json", limit=100, browser="chrome")
        assert isinstance(result, str)

    def test_export_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_export_history(*args, **kwargs):
            raise ValidationError("Invalid format")

        monkeypatch.setattr(services.HistoryService, "export_history", mock_export_history)

        result = export_history(format_type="xml", browser="chrome")
        assert "error" in result.lower() or "Error" in result


class TestSearchHistoryAdvancedMCP:
    """Tests for search_history_advanced MCP tool."""

    def test_advanced_search_basic(self, monkeypatch):
        """Test advanced search."""
        from chronicle_mcp.core import services

        def mock_search_history_advanced(*args, **kwargs):
            return {
                "results": [("Test", "https://example.com", "2024-01-01")],
                "count": 1,
                "query": "test",
                "options": {"sort_by": "date", "use_regex": False, "use_fuzzy": False},
                "message": "Found 1 result for 'test'",
            }

        monkeypatch.setattr(
            services.HistoryService, "search_history_advanced", mock_search_history_advanced
        )

        result = search_history_advanced(query="test", limit=10, browser="chrome")
        assert isinstance(result, str)

    def test_advanced_search_with_regex(self, monkeypatch):
        """Test with regex."""
        from chronicle_mcp.core import services

        def mock_search_history_advanced(*args, **kwargs):
            return {
                "results": [("GitHub", "https://github.com", "2024-01-01")],
                "count": 1,
                "query": "^https://.*github",
                "options": {"sort_by": "date", "use_regex": True, "use_fuzzy": False},
                "message": "Found 1 result",
            }

        monkeypatch.setattr(
            services.HistoryService, "search_history_advanced", mock_search_history_advanced
        )

        result = search_history_advanced(
            query="^https://.*github", limit=10, browser="chrome", use_regex=True
        )
        assert isinstance(result, str)

    def test_advanced_search_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_search_history_advanced(*args, **kwargs):
            raise ValidationError("Cannot use both regex and fuzzy")

        monkeypatch.setattr(
            services.HistoryService, "search_history_advanced", mock_search_history_advanced
        )

        result = search_history_advanced(
            query="test", browser="chrome", use_regex=True, use_fuzzy=True
        )
        assert "error" in result.lower() or "Error" in result


class TestSyncHistoryMCP:
    """Tests for sync_history MCP tool."""

    def test_sync_dry_run(self, monkeypatch):
        """Test sync in dry run mode."""
        from chronicle_mcp.core import services

        def mock_sync_history(*args, **kwargs):
            return {
                "dry_run": True,
                "source": "chrome",
                "target": "firefox",
                "entries_count": 100,
                "merge_strategy": "latest",
                "message": "Dry run: would sync 100 entries from chrome to firefox",
            }

        monkeypatch.setattr(services.HistoryService, "sync_history", mock_sync_history)

        result = sync_history(
            source_browser="chrome", target_browser="firefox", merge_strategy="latest", dry_run=True
        )
        assert isinstance(result, str)
        assert "dry run" in result.lower()

    def test_sync_validation_error(self, monkeypatch):
        """Test with validation error."""
        from chronicle_mcp.core import services

        def mock_sync_history(*args, **kwargs):
            raise ValidationError("Browsers must be different")

        monkeypatch.setattr(services.HistoryService, "sync_history", mock_sync_history)

        result = sync_history(
            source_browser="chrome", target_browser="chrome", merge_strategy="latest", dry_run=True
        )
        assert "error" in result.lower() or "Error" in result

    def test_sync_browser_not_found(self, monkeypatch):
        """Test when browser not found."""
        from chronicle_mcp.core import services

        def mock_sync_history(*args, **kwargs):
            raise BrowserNotFoundError("safari")

        monkeypatch.setattr(services.HistoryService, "sync_history", mock_sync_history)

        result = sync_history(
            source_browser="safari",
            target_browser="firefox",
            merge_strategy="latest",
            dry_run=True,
        )
        assert "could not find" in result.lower()
