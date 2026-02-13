"""Tests for core formatter functions."""

import json

import pytest

from chronicle_mcp.core.formatters import (
    format_advanced_search_results,
    format_available_browsers,
    format_browser_stats,
    format_delete_preview,
    format_delete_result,
    format_domain_search_results,
    format_domain_visits,
    format_error_message,
    format_export,
    format_most_visited_pages,
    format_recent_results,
    format_search_results,
    format_sync_preview,
    format_sync_result,
    format_top_domains,
)


class TestFormatSearchResults:
    """Tests for format_search_results function."""

    def test_markdown_format(self):
        rows = [
            ("Test Title", "https://example.com", "2024-01-01T10:00:00"),
        ]
        result = format_search_results(rows, "test query")
        assert "Test Title" in result
        assert "https://example.com" in result
        assert "2024-01-01T10:00:00" in result

    def test_json_format(self):
        rows = [
            ("Test Title", "https://example.com", "2024-01-01T10:00:00"),
        ]
        result = format_search_results(rows, "test query", "json")
        data = json.loads(result)
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Test Title"

    def test_empty_results_markdown(self):
        result = format_search_results([], "test query")
        assert "No history found for: test query" == result

    def test_empty_results_json(self):
        result = format_search_results([], "test query", "json")
        # When no results, it returns a plain text message even for JSON format
        assert "No history found" in result

    def test_multiple_rows(self):
        rows = [
            ("Title 1", "https://example1.com", "2024-01-01"),
            ("Title 2", "https://example2.com", "2024-01-02"),
        ]
        result = format_search_results(rows, "query")
        assert "Title 1" in result
        assert "Title 2" in result


class TestFormatRecentResults:
    """Tests for format_recent_results function."""

    def test_markdown_format(self):
        rows = [
            ("Test", "https://example.com", "2024-01-01T10:00:00"),
        ]
        result = format_recent_results(rows, 24)
        assert "History from last 24 hours" in result
        assert "Test" in result

    def test_json_format(self):
        rows = [
            ("Test", "https://example.com", "2024-01-01T10:00:00"),
        ]
        result = format_recent_results(rows, 24, "json")
        data = json.loads(result)
        assert data["count"] == 1

    def test_empty_results(self):
        result = format_recent_results([], 24)
        assert "No history found in the last 24 hours" == result


class TestFormatDomainVisits:
    """Tests for format_domain_visits function."""

    def test_format(self):
        result = format_domain_visits("github.com", "chrome", 42)
        assert "github.com" in result
        assert "chrome" in result
        assert "42" in result


class TestFormatTopDomains:
    """Tests for format_top_domains function."""

    def test_markdown_format(self):
        domains = [("github.com", 100), ("stackoverflow.com", 50)]
        result = format_top_domains(domains)
        assert "github.com" in result
        assert "100 visits" in result
        assert "stackoverflow.com" in result

    def test_json_format(self):
        domains = [("github.com", 100)]
        result = format_top_domains(domains, "json")
        data = json.loads(result)
        assert data["top_domains"][0]["domain"] == "github.com"
        assert data["top_domains"][0]["visits"] == 100

    def test_empty_domains(self):
        result = format_top_domains([])
        assert "No domain data found" == result


class TestFormatMostVisitedPages:
    """Tests for format_most_visited_pages function."""

    def test_markdown_format(self):
        pages = [("Home", "https://example.com", 50)]
        result = format_most_visited_pages(pages)
        assert "Home" in result
        assert "https://example.com" in result
        assert "50" in result

    def test_json_format(self):
        pages = [("Home", "https://example.com", 50)]
        result = format_most_visited_pages(pages, "json")
        data = json.loads(result)
        assert data["top_pages"][0]["title"] == "Home"
        assert data["top_pages"][0]["visits"] == 50

    def test_empty_pages(self):
        result = format_most_visited_pages([])
        assert "No page data found" == result


class TestFormatDomainSearchResults:
    """Tests for format_domain_search_results function."""

    def test_markdown_with_query(self):
        rows = [("Result", "https://github.com/test", "2024-01-01")]
        result = format_domain_search_results(rows, "github.com", "test")
        assert "github.com" in result
        assert "test" in result
        assert "Result" in result

    def test_markdown_without_query(self):
        rows = [("Result", "https://github.com/test", "2024-01-01")]
        result = format_domain_search_results(rows, "github.com", None)
        assert "github.com" in result
        assert "Result" in result

    def test_json_format(self):
        rows = [("Result", "https://github.com", "2024-01-01")]
        result = format_domain_search_results(rows, "github.com", None, "json")
        data = json.loads(result)
        assert data["domain"] == "github.com"
        assert data["count"] == 1

    def test_empty_results(self):
        result = format_domain_search_results([], "github.com", None)
        assert "No history found for domain: github.com" == result


class TestFormatAdvancedSearchResults:
    """Tests for format_advanced_search_results function."""

    def test_markdown_format(self):
        rows = [("Test", "https://example.com", "2024-01-01")]
        options = {"sort_by": "date"}
        result = format_advanced_search_results(rows, "query", "markdown", options)
        assert "Test" in result

    def test_json_format(self):
        rows = [("Test", "https://example.com", "2024-01-01")]
        options = {"sort_by": "date"}
        result = format_advanced_search_results(rows, "query", "json", options)
        data = json.loads(result)
        assert data["query"] == "query"
        assert data["options"]["sort_by"] == "date"


class TestFormatBrowserStats:
    """Tests for format_browser_stats function."""

    def test_format(self):
        stats = {
            "total_entries": 100,
            "total_visits": 500,
            "unique_urls": 80,
        }
        result = format_browser_stats(stats)
        data = json.loads(result)
        assert data["total_entries"] == 100
        assert data["total_visits"] == 500


class TestFormatExport:
    """Tests for format_export function."""

    def test_csv_format(self):
        rows = [
            {"title": "Test", "url": "https://example.com", "timestamp": "2024-01-01"},
        ]
        result = format_export(rows, "csv")
        assert "title,url,timestamp" in result
        assert "Test" in result
        assert "https://example.com" in result

    def test_json_format(self):
        rows = [
            {"title": "Test", "url": "https://example.com", "timestamp": "2024-01-01"},
        ]
        result = format_export(rows, "json")
        data = json.loads(result)
        assert data["exported_entries"] == 1
        assert data["entries"][0]["title"] == "Test"

    def test_empty_csv(self):
        result = format_export([], "csv")
        assert result == ""

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            format_export([], "xml")


class TestFormatDeletePreview:
    """Tests for format_delete_preview function."""

    def test_format(self):
        result = format_delete_preview("test", 5)
        assert "preview" in result.lower()
        assert "5 entries" in result
        assert "test" in result
        assert "confirm=true" in result


class TestFormatDeleteResult:
    """Tests for format_delete_result function."""

    def test_format(self):
        result = format_delete_result("test", "chrome", 5)
        assert "Deleted 5" in result
        assert "test" in result
        assert "chrome" in result


class TestFormatSyncPreview:
    """Tests for format_sync_preview function."""

    def test_format(self):
        result = format_sync_preview("chrome", "firefox", 100, "latest")
        assert "Dry run" in result
        assert "100 entries" in result
        assert "chrome" in result
        assert "firefox" in result
        assert "latest" in result


class TestFormatSyncResult:
    """Tests for format_sync_result function."""

    def test_format(self):
        result = format_sync_result("chrome", "firefox", 100, "latest")
        assert "Synced 100" in result
        assert "chrome" in result
        assert "firefox" in result


class TestFormatAvailableBrowsers:
    """Tests for format_available_browsers function."""

    def test_with_browsers(self):
        result = format_available_browsers(["chrome", "firefox"])
        assert "Available browsers: chrome, firefox" == result

    def test_empty_list(self):
        result = format_available_browsers([])
        assert "No browsers with history found" in result


class TestFormatErrorMessage:
    """Tests for format_error_message function."""

    def test_format(self):
        result = format_error_message("Something went wrong")
        assert "Error: Something went wrong" == result
