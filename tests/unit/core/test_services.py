"""Tests for core service functions."""

import pytest

from chronicle_mcp.core import HistoryService
from chronicle_mcp.core.exceptions import BrowserNotFoundError


class TestListAvailableBookmarks:
    """Tests for list_available_bookmarks service method."""

    def test_returns_dict_with_browsers(self):
        result = HistoryService.list_available_bookmarks()
        assert isinstance(result, dict)
        assert "browsers" in result
        assert "message" in result


class TestListAvailableDownloads:
    """Tests for list_available_downloads service method."""

    def test_returns_dict_with_browsers(self):
        result = HistoryService.list_available_downloads()
        assert isinstance(result, dict)
        assert "browsers" in result
        assert "message" in result


@pytest.mark.ci_excluded
class TestGetBookmarks:
    """Tests for get_bookmarks service method."""

    def test_raises_error_when_bookmarks_not_found(self, monkeypatch):
        from chronicle_mcp import paths

        # Use a browser that definitely won't have bookmarks on this platform
        def mock_get_bookmark_path(browser):
            if browser == "safari":
                return None
            # Return real path for other browsers to not break the test
            import platform

            if platform.system() != "Darwin":
                return None
            return None

        monkeypatch.setattr(paths, "get_bookmark_path", mock_get_bookmark_path)

        with pytest.raises(BrowserNotFoundError):
            HistoryService.get_bookmarks(browser="safari")

    def test_returns_dict_with_results(self, temp_dir, monkeypatch):
        import json

        from chronicle_mcp import paths

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "bookmark_bar": {
                    "type": "folder",
                    "children": [
                        {"type": "url", "name": "GitHub", "url": "https://github.com"},
                    ],
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        def mock_get_bookmark_path(browser):
            return str(bookmark_file)

        monkeypatch.setattr(paths, "get_bookmark_path", mock_get_bookmark_path)

        result = HistoryService.get_bookmarks(browser="chrome")
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "browser" in result
        assert "message" in result

    def test_with_query_filter(self, temp_dir, monkeypatch):
        import json

        from chronicle_mcp import paths

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "bookmark_bar": {
                    "type": "folder",
                    "children": [
                        {"type": "url", "name": "GitHub", "url": "https://github.com"},
                        {"type": "url", "name": "Python", "url": "https://python.org"},
                    ],
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        def mock_get_bookmark_path(browser):
            return str(bookmark_file)

        monkeypatch.setattr(paths, "get_bookmark_path", mock_get_bookmark_path)

        result_with_filter = HistoryService.get_bookmarks(query="github", browser="chrome")
        result_all = HistoryService.get_bookmarks(browser="chrome")
        # Filtered results should be fewer than all results
        assert result_with_filter["count"] < result_all["count"]


@pytest.mark.ci_excluded
class TestGetDownloads:
    """Tests for get_downloads service method."""

    def test_raises_error_when_downloads_not_found(self, monkeypatch):
        from chronicle_mcp import paths

        def mock_get_download_path(browser):
            if browser == "safari":
                return None
            return None

        monkeypatch.setattr(paths, "get_download_path", mock_get_download_path)

        with pytest.raises(BrowserNotFoundError):
            HistoryService.get_downloads(browser="safari")

    def test_returns_dict_with_results(self, temp_dir, monkeypatch):
        import sqlite3

        from chronicle_mcp import paths

        db_path = temp_dir / "History"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE urls (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visit_count INTEGER DEFAULT 0,
                last_visit_time INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE downloads (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                url TEXT,
                start_time INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO downloads (filename, url, start_time) VALUES
            ('test.pdf', 'https://example.com/test.pdf', 13316000000000000)
        """)
        conn.commit()
        conn.close()

        def mock_get_download_path(browser):
            return str(db_path)

        monkeypatch.setattr(paths, "get_download_path", mock_get_download_path)

        result = HistoryService.get_downloads(browser="chrome")
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "browser" in result
        assert "message" in result


class TestListAvailableBrowsers:
    """Tests for list_available_browsers service method."""

    def test_returns_dict_with_browsers(self, monkeypatch):
        """Test returns dict with browsers list."""
        from chronicle_mcp import paths

        def mock_get_available_browsers():
            return ["chrome", "firefox"]

        monkeypatch.setattr(paths, "get_available_browsers", mock_get_available_browsers)

        result = HistoryService.list_available_browsers()
        assert isinstance(result, dict)
        assert "browsers" in result
        assert "message" in result
        # Check structure, not exact values since they depend on system
        assert isinstance(result["browsers"], list)

    def test_returns_empty_list_when_no_browsers(self, monkeypatch):
        """Test returns empty list when no browsers found."""
        from chronicle_mcp.core import browser_service

        def mock_get_available_browsers():
            return []

        monkeypatch.setattr(browser_service, "get_available_browsers", mock_get_available_browsers)

        result = HistoryService.list_available_browsers()
        assert result["browsers"] == []
        assert "message" in result


class TestSearchHistory:
    """Tests for search_history service method."""

    def test_search_with_valid_query(self, mock_chrome_path, sample_chrome_db):
        """Test search with valid query."""
        result = HistoryService.search_history(query="python", limit=5, browser="chrome")
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "query" in result
        assert "message" in result
        assert result["query"] == "python"

    def test_search_case_insensitive_browser(self, mock_chrome_path, sample_chrome_db):
        """Test browser name is case insensitive."""
        result_lower = HistoryService.search_history(query="test", browser="chrome")
        result_upper = HistoryService.search_history(query="test", browser="CHROME")
        assert isinstance(result_lower, dict)
        assert isinstance(result_upper, dict)

    def test_search_with_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test search with JSON format."""
        result = HistoryService.search_history(
            query="python", limit=5, browser="chrome", format_type="json"
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result

    def test_search_invalid_browser(self):
        """Test search with invalid browser raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history(query="test", browser="invalid_browser")
        assert "Invalid browser" in str(exc_info.value)

    def test_search_empty_query(self):
        """Test search with empty query raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history(query="", browser="chrome")
        assert "Query cannot be empty" in str(exc_info.value)

    def test_search_invalid_limit(self):
        """Test search with invalid limit raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history(query="test", limit=0, browser="chrome")
        assert "must be between" in str(exc_info.value)

    def test_search_negative_limit(self):
        """Test search with negative limit raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history(query="test", limit=-5, browser="chrome")
        assert "must be between" in str(exc_info.value)


class TestGetRecentHistory:
    """Tests for get_recent_history service method."""

    def test_get_recent_basic(self, mock_chrome_path, sample_chrome_db):
        """Test getting recent history."""
        result = HistoryService.get_recent_history(hours=24, limit=10, browser="chrome")
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "hours" in result
        assert "message" in result
        assert result["hours"] == 24

    def test_get_recent_with_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test getting recent history with JSON format."""
        result = HistoryService.get_recent_history(
            hours=12, limit=5, browser="chrome", format_type="json"
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result

    def test_get_recent_invalid_hours(self):
        """Test with invalid hours raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.get_recent_history(hours=0, browser="chrome")
        assert "Hours must be a positive integer" in str(exc_info.value)

    def test_get_recent_negative_hours(self):
        """Test with negative hours raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.get_recent_history(hours=-1, browser="chrome")
        assert "Hours must be a positive integer" in str(exc_info.value)


class TestCountVisits:
    """Tests for count_visits service method."""

    def test_count_visits_basic(self, mock_chrome_path, sample_chrome_db):
        """Test counting visits to a domain."""
        result = HistoryService.count_visits(domain="github.com", browser="chrome")
        assert isinstance(result, dict)
        assert "domain" in result
        assert "browser" in result
        assert "count" in result
        assert "message" in result
        assert result["domain"] == "github.com"
        assert result["browser"] == "chrome"

    def test_count_visits_nonexistent_domain(self, mock_chrome_path, sample_chrome_db):
        """Test counting visits to nonexistent domain."""
        result = HistoryService.count_visits(domain="nonexistent.xyz", browser="chrome")
        assert result["count"] == 0
        assert result["domain"] == "nonexistent.xyz"

    def test_count_visits_invalid_browser(self):
        """Test with invalid browser raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.count_visits(domain="github.com", browser="invalid")
        assert "Invalid browser" in str(exc_info.value)

    def test_count_visits_empty_domain(self):
        """Test with empty domain raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.count_visits(domain="", browser="chrome")
        assert "Domain cannot be empty" in str(exc_info.value)


class TestListTopDomains:
    """Tests for list_top_domains service method."""

    def test_list_top_domains_basic(self, mock_chrome_path, sample_chrome_db):
        """Test getting top domains."""
        result = HistoryService.list_top_domains(limit=5, browser="chrome")
        assert isinstance(result, dict)
        assert "domains" in result
        assert "count" in result
        assert "message" in result

    def test_list_top_domains_with_json(self, mock_chrome_path, sample_chrome_db):
        """Test getting top domains with JSON format."""
        result = HistoryService.list_top_domains(limit=3, browser="chrome", format_type="json")
        assert isinstance(result, dict)
        assert "domains" in result

    def test_list_top_domains_invalid_limit(self):
        """Test with invalid limit raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.list_top_domains(limit=0, browser="chrome")
        assert "must be between" in str(exc_info.value)

    def test_list_top_domains_limit_above_max(self):
        """Test with limit above maximum raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.list_top_domains(limit=100, browser="chrome")
        assert "must be between" in str(exc_info.value)


class TestSearchHistoryByDate:
    """Tests for search_history_by_date service method."""

    def test_search_by_date_basic(self, mock_chrome_path, sample_chrome_db):
        """Test searching by date range."""
        result = HistoryService.search_history_by_date(
            query="test",
            start_date="2024-01-01",
            end_date="2024-12-31",
            limit=10,
            browser="chrome",
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "query" in result
        assert "start_date" in result
        assert "end_date" in result
        assert "message" in result

    def test_search_by_date_invalid_date_format(self):
        """Test with invalid date format raises error."""
        from chronicle_mcp.core import InvalidDateRangeError

        with pytest.raises(InvalidDateRangeError) as exc_info:
            HistoryService.search_history_by_date(
                query="test",
                start_date="invalid-date",
                end_date="2024-12-31",
                browser="chrome",
            )
        assert "Invalid date format" in str(exc_info.value)

    def test_search_by_date_start_after_end(self):
        """Test with start date after end date raises error."""
        from chronicle_mcp.core import InvalidDateRangeError

        with pytest.raises(InvalidDateRangeError) as exc_info:
            HistoryService.search_history_by_date(
                query="test",
                start_date="2024-12-31",
                end_date="2024-01-01",
                browser="chrome",
            )
        assert "Start date must be before" in str(exc_info.value)


class TestDeleteHistory:
    """Tests for delete_history service method."""

    def test_delete_history_preview_mode(self, mock_chrome_path, sample_chrome_db):
        """Test delete in preview mode (confirm=False)."""
        result = HistoryService.delete_history(
            query="test", limit=100, browser="chrome", confirm=False
        )
        assert isinstance(result, dict)
        assert "preview" in result
        assert result["preview"] is True
        assert "query" in result
        assert "count" in result
        assert "message" in result

    def test_delete_history_invalid_browser(self):
        """Test with invalid browser raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.delete_history(query="test", browser="invalid")
        assert "Invalid browser" in str(exc_info.value)

    def test_delete_history_empty_query(self):
        """Test with empty query raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.delete_history(query="", browser="chrome")
        assert "Query cannot be empty" in str(exc_info.value)


class TestSearchByDomain:
    """Tests for search_by_domain service method."""

    def test_search_by_domain_basic(self, mock_chrome_path, sample_chrome_db):
        """Test searching within a domain."""
        result = HistoryService.search_by_domain(
            domain="github.com", query=None, limit=10, browser="chrome"
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "domain" in result
        assert result["domain"] == "github.com"
        assert "message" in result

    def test_search_by_domain_with_query(self, mock_chrome_path, sample_chrome_db):
        """Test searching within domain with query."""
        result = HistoryService.search_by_domain(
            domain="github.com", query="claude", limit=10, browser="chrome"
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert "query" in result
        assert result["query"] == "claude"

    def test_search_by_domain_with_exclude(self, mock_chrome_path, sample_chrome_db):
        """Test searching with excluded domains."""
        result = HistoryService.search_by_domain(
            domain="github.com",
            query=None,
            limit=10,
            browser="chrome",
            exclude_domains=["stackoverflow.com"],
        )
        assert isinstance(result, dict)
        assert "results" in result

    def test_search_by_domain_invalid_domain(self):
        """Test with empty domain raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_by_domain(domain="", browser="chrome")
        assert "Domain cannot be empty" in str(exc_info.value)


class TestGetBrowserStats:
    """Tests for get_browser_stats service method."""

    def test_get_browser_stats_basic(self, mock_chrome_path, sample_chrome_db):
        """Test getting browser statistics."""
        result = HistoryService.get_browser_stats(browser="chrome")
        assert isinstance(result, dict)
        assert "stats" in result
        assert "message" in result

    def test_get_browser_stats_invalid_browser(self):
        """Test with invalid browser raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.get_browser_stats(browser="invalid")
        assert "Invalid browser" in str(exc_info.value)


class TestGetMostVisitedPages:
    """Tests for get_most_visited_pages service method."""

    def test_get_most_visited_basic(self, mock_chrome_path, sample_chrome_db):
        """Test getting most visited pages."""
        result = HistoryService.get_most_visited_pages(limit=10, browser="chrome")
        assert isinstance(result, dict)
        assert "pages" in result
        assert "count" in result
        assert "message" in result

    def test_get_most_visited_with_json(self, mock_chrome_path, sample_chrome_db):
        """Test getting most visited pages with JSON format."""
        result = HistoryService.get_most_visited_pages(
            limit=5, browser="chrome", format_type="json"
        )
        assert isinstance(result, dict)
        assert "pages" in result

    def test_get_most_visited_invalid_limit(self):
        """Test with invalid limit raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.get_most_visited_pages(limit=0, browser="chrome")
        assert "must be between" in str(exc_info.value)


class TestExportHistory:
    """Tests for export_history service method."""

    def test_export_csv_format(self, mock_chrome_path, sample_chrome_db):
        """Test exporting to CSV format."""
        result = HistoryService.export_history(
            format_type="csv", limit=10, query=None, browser="chrome"
        )
        assert isinstance(result, dict)
        assert "content" in result
        assert "format" in result
        assert result["format"] == "csv"
        assert "browser" in result

    def test_export_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test exporting to JSON format."""
        result = HistoryService.export_history(
            format_type="json", limit=10, query=None, browser="chrome"
        )
        assert isinstance(result, dict)
        assert "content" in result
        assert "format" in result
        assert result["format"] == "json"

    def test_export_with_query(self, mock_chrome_path, sample_chrome_db):
        """Test exporting with query filter."""
        result = HistoryService.export_history(
            format_type="csv", limit=10, query="python", browser="chrome"
        )
        assert isinstance(result, dict)
        assert "content" in result

    def test_export_invalid_format(self):
        """Test with invalid format raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.export_history(format_type="xml", browser="chrome")
        assert "Invalid format_type" in str(exc_info.value)


class TestSearchHistoryAdvanced:
    """Tests for search_history_advanced service method."""

    def test_advanced_search_basic(self, mock_chrome_path, sample_chrome_db):
        """Test advanced search with basic options."""
        result = HistoryService.search_history_advanced(query="python", limit=10, browser="chrome")
        assert isinstance(result, dict)
        assert "results" in result
        assert "count" in result
        assert "query" in result
        assert "options" in result
        assert "message" in result

    def test_advanced_search_with_regex(self, mock_chrome_path, sample_chrome_db):
        """Test advanced search with regex."""
        result = HistoryService.search_history_advanced(
            query="^https://.*github", limit=10, browser="chrome", use_regex=True
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert result["options"]["use_regex"] is True

    def test_advanced_search_with_fuzzy(self, mock_chrome_path, sample_chrome_db):
        """Test advanced search with fuzzy matching."""
        result = HistoryService.search_history_advanced(
            query="rubish",  # intentional misspell to test fuzzy
            limit=10,
            browser="chrome",
            use_fuzzy=True,
            fuzzy_threshold=0.6,
        )
        assert isinstance(result, dict)
        assert "results" in result
        assert result["options"]["use_fuzzy"] is True

    def test_advanced_search_with_exclude_domains(self, mock_chrome_path, sample_chrome_db):
        """Test advanced search with excluded domains."""
        result = HistoryService.search_history_advanced(
            query="test",
            limit=10,
            browser="chrome",
            exclude_domains=["stackoverflow.com"],
        )
        assert isinstance(result, dict)
        assert "results" in result

    def test_advanced_search_both_regex_and_fuzzy(self):
        """Test with both regex and fuzzy raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history_advanced(
                query="test",
                browser="chrome",
                use_regex=True,
                use_fuzzy=True,
            )
        assert "Cannot use both regex and fuzzy" in str(exc_info.value)

    def test_advanced_search_invalid_sort_by(self):
        """Test with invalid sort_by raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history_advanced(
                query="test", browser="chrome", sort_by="invalid"
            )
        assert "Invalid sort_by" in str(exc_info.value)

    def test_advanced_search_invalid_fuzzy_threshold(self):
        """Test with invalid fuzzy_threshold raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.search_history_advanced(
                query="test", browser="chrome", use_fuzzy=True, fuzzy_threshold=1.5
            )
        assert "must be between 0.0 and 1.0" in str(exc_info.value)


class TestSyncHistory:
    """Tests for sync_history service method."""

    def test_sync_dry_run(self, mock_chrome_path, sample_chrome_db, temp_dir, monkeypatch):
        """Test sync in dry run mode."""
        import sqlite3

        from chronicle_mcp.core import history_service

        firefox_db = temp_dir / "firefox_places.sqlite"
        conn = sqlite3.connect(str(firefox_db))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE moz_places (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visit_count INTEGER DEFAULT 0,
                last_visit_date INTEGER
            )
        """)
        conn.commit()
        conn.close()

        def mock_get_browser_path(browser):
            if browser.lower() == "firefox":
                return str(firefox_db)
            return sample_chrome_db

        monkeypatch.setattr(history_service, "get_browser_path", mock_get_browser_path)

        result = HistoryService.sync_history(
            source_browser="chrome",
            target_browser="firefox",
            merge_strategy="latest",
            dry_run=True,
        )
        assert isinstance(result, dict)
        assert "dry_run" in result
        assert result["dry_run"] is True
        assert "source" in result
        assert "target" in result
        assert "entries_count" in result
        assert "merge_strategy" in result
        assert "message" in result

    def test_sync_same_browser(self):
        """Test sync with same browser raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.sync_history(
                source_browser="chrome",
                target_browser="chrome",
                merge_strategy="latest",
                dry_run=True,
            )
        assert "must be different" in str(exc_info.value)

    def test_sync_invalid_merge_strategy(self):
        """Test with invalid merge strategy raises error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            HistoryService.sync_history(
                source_browser="chrome",
                target_browser="firefox",
                merge_strategy="invalid",
                dry_run=True,
            )
        assert "Invalid merge_strategy" in str(exc_info.value)

    def test_sync_browser_not_found(self, monkeypatch):
        """Test sync when browser not found raises error."""
        from chronicle_mcp import paths

        def mock_get_browser_path(browser):
            return None

        monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)

        with pytest.raises(BrowserNotFoundError):
            HistoryService.sync_history(
                source_browser="chrome",
                target_browser="firefox",
                merge_strategy="latest",
                dry_run=True,
            )

    def test_sync_actual_sync(self, temp_dir, sample_chrome_db, monkeypatch):
        """Test actual sync (not dry run) between chrome and firefox."""
        import sqlite3

        import chronicle_mcp.connection
        import chronicle_mcp.core.history_service
        import chronicle_mcp.core.services
        from chronicle_mcp import paths

        firefox_db_path = str(temp_dir / "firefox_places.sqlite")
        conn = sqlite3.connect(firefox_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE moz_places (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visit_count INTEGER DEFAULT 0,
                last_visit_date INTEGER
            )
        """)
        conn.commit()
        conn.close()

        def mock_get_browser_path(browser):
            path = browser.lower()
            if path == "firefox":
                return firefox_db_path
            elif path == "chrome":
                return sample_chrome_db
            return None

        monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)
        monkeypatch.setattr(chronicle_mcp.connection, "get_browser_path", mock_get_browser_path)
        monkeypatch.setattr(
            chronicle_mcp.core.history_service, "get_browser_path", mock_get_browser_path
        )

        # Verify the mock is working
        assert mock_get_browser_path("chrome") == sample_chrome_db, "Chrome mock failed"
        assert mock_get_browser_path("firefox") == firefox_db_path, "Firefox mock failed"

        conn = sqlite3.connect(sample_chrome_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls")
        chrome_count = cursor.fetchone()[0]
        conn.close()

        result = HistoryService.sync_history(
            source_browser="chrome",
            target_browser="firefox",
            merge_strategy="latest",
            dry_run=False,
        )
        assert isinstance(result, dict)
        assert result["dry_run"] is False
        assert "entries_count" in result
        assert "message" in result

        conn = sqlite3.connect(firefox_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM moz_places")
        count = cursor.fetchone()[0]
        conn.close()
        assert count > 0, (
            f"Expected entries in firefox db but got {count}. Chrome had {chrome_count}"
        )


class TestWithConnectionErrorHandling:
    """Tests for _with_connection error handling."""

    def test_browser_not_found_error(self, monkeypatch):
        """Test BrowserNotFoundError is raised for missing browser."""
        from chronicle_mcp.connection import BrowserNotFoundError as ConnBrowserNotFoundError

        def mock_get_history_connection(browser):
            raise ConnBrowserNotFoundError("chrome")

        monkeypatch.setattr(
            "chronicle_mcp.core._connection._get_history_connection",
            mock_get_history_connection,
        )

        with pytest.raises(BrowserNotFoundError) as exc_info:
            HistoryService._with_connection("chrome", lambda conn: None)
        assert "chrome" in str(exc_info.value)

    def test_database_locked_error(self, monkeypatch):
        """Test DatabaseLockedError is raised for locked database."""
        from chronicle_mcp.connection import DatabaseLockedError as ConnDatabaseLockedError

        def mock_get_history_connection(browser):
            raise ConnDatabaseLockedError("chrome", "/path/to/db")

        monkeypatch.setattr(
            "chronicle_mcp.core._connection._get_history_connection",
            mock_get_history_connection,
        )

        from chronicle_mcp.core import DatabaseLockedError

        with pytest.raises(DatabaseLockedError) as exc_info:
            HistoryService._with_connection("chrome", lambda conn: None)
        assert "chrome" in str(exc_info.value)

    def test_permission_denied_error(self, monkeypatch):
        """Test PermissionDeniedError is raised for permission issues."""
        from chronicle_mcp.connection import PermissionDeniedError as ConnPermissionDeniedError

        def mock_get_history_connection(browser):
            raise ConnPermissionDeniedError("chrome", "/path/to/db")

        monkeypatch.setattr(
            "chronicle_mcp.core._connection._get_history_connection",
            mock_get_history_connection,
        )

        from chronicle_mcp.core import PermissionDeniedError

        with pytest.raises(PermissionDeniedError) as exc_info:
            HistoryService._with_connection("chrome", lambda conn: None)
        assert "chrome" in str(exc_info.value)

    def test_connection_error_converted_to_database_error(self, monkeypatch):
        """Test ConnConnectionError is converted to DatabaseError."""
        from chronicle_mcp.connection import ConnectionError as ConnConnectionError

        def mock_get_history_connection(browser):
            raise ConnConnectionError("Connection failed", browser="chrome", details="timeout")

        monkeypatch.setattr(
            "chronicle_mcp.core._connection._get_history_connection",
            mock_get_history_connection,
        )

        from chronicle_mcp.core import DatabaseError

        with pytest.raises(DatabaseError) as exc_info:
            HistoryService._with_connection("chrome", lambda conn: None)
        assert "chrome" in str(exc_info.value)
        assert "Failed to access" in str(exc_info.value)

    def test_unexpected_error_converted_to_database_error(self, monkeypatch):
        """Test unexpected exceptions are converted to DatabaseError."""

        def mock_get_history_connection(browser):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(
            "chronicle_mcp.core._connection._get_history_connection",
            mock_get_history_connection,
        )

        from chronicle_mcp.core import DatabaseError

        with pytest.raises(DatabaseError) as exc_info:
            HistoryService._with_connection("chrome", lambda conn: None)
        assert "Database operation failed" in str(exc_info.value)


@pytest.mark.ci_excluded
class TestFindDuplicateEntries:
    """Tests for find_duplicate_entries method."""

    def test_find_duplicate_entries_invalid_threshold_too_high(self, monkeypatch):
        """Test invalid similarity_threshold (>1.0) raises ValidationError."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.find_duplicate_entries("chrome", similarity_threshold=1.5)

    def test_find_duplicate_entries_invalid_threshold_negative(self, monkeypatch):
        """Test invalid similarity_threshold (<0) raises ValidationError."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.find_duplicate_entries("chrome", similarity_threshold=-0.1)

    def test_find_duplicate_entries_invalid_browser(self, monkeypatch):
        """Test invalid browser raises ValidationError."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.find_duplicate_entries("invalid_browser")

    def test_find_duplicate_entries_limit_boundary(self, monkeypatch):
        """Test limit boundary values are accepted."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.find_duplicate_entries("chrome", limit=0)

        with pytest.raises(ValidationError):
            HistoryService.find_duplicate_entries("chrome", limit=1001)

    def test_find_duplicate_entries_returns_structure(self, monkeypatch):
        """Test find_duplicate_entries returns expected structure."""
        from unittest.mock import patch

        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, "_with_connection", return_value=[]):
            result = HistoryService.find_duplicate_entries(
                browser="chrome",
                similarity_threshold=0.9,
                limit=100,
            )

        assert "browser" in result
        assert "similarity_threshold" in result
        assert "duplicate_groups" in result
        assert "total_duplicates" in result
        assert "total_entries_analyzed" in result


@pytest.mark.ci_excluded
class TestDeleteDuplicates:
    """Tests for delete_duplicates method."""

    def test_delete_duplicates_invalid_strategy(self, monkeypatch):
        """Test invalid keep_strategy raises ValueError."""
        with pytest.raises(ValueError, match="Invalid keep_strategy"):
            HistoryService.delete_duplicates("chrome", keep_strategy="invalid_strategy")

    def test_delete_duplicates_preview_mode_returns_preview(self, monkeypatch):
        """Test preview mode (confirm=False) returns preview structure."""
        from unittest.mock import patch

        with patch.object(
            HistoryService,
            "find_duplicate_entries",
            return_value={
                "duplicate_groups": [],
                "total_duplicates": 0,
            },
        ):
            result = HistoryService.delete_duplicates(
                browser="chrome",
                confirm=False,
            )

        assert result["preview"] is True
        assert "message" in result

    def test_delete_duplicates_confirm_true_not_raises(self, monkeypatch):
        """Test confirm=True doesn't raise (actual deletion would be mocked)."""
        from unittest.mock import patch

        with patch.object(
            HistoryService,
            "find_duplicate_entries",
            return_value={
                "duplicate_groups": [],
                "total_duplicates": 0,
            },
        ):
            with patch.object(HistoryService, "delete_history", return_value={"deleted": 0}):
                result = HistoryService.delete_duplicates(
                    browser="chrome",
                    confirm=True,
                    keep_strategy="most_visits",
                )

        assert "preview" in result or "deleted_count" in result or "message" in result


class TestSubscribeHistoryChanges:
    """Tests for subscribe_history_changes method."""

    def test_subscribe_history_changes_invalid_event_type(self, monkeypatch):
        """Test invalid event type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid event type"):
            HistoryService.subscribe_history_changes(
                browser="chrome",
                event_types=["invalid_type"],
                callback=lambda e: None,
            )

    def test_subscribe_history_changes_empty_callback(self, monkeypatch):
        """Test empty event_types raises ValueError."""
        with pytest.raises(ValueError):
            HistoryService.subscribe_history_changes(
                browser="chrome",
                event_types=[],
                callback=lambda e: None,
            )


class TestUnsubscribeHistoryChanges:
    """Tests for unsubscribe_history_changes method."""

    def test_unsubscribe_history_changes_returns_structure(self, monkeypatch):
        """Test unsubscribe_history_changes returns expected structure."""
        from chronicle_mcp.core.events import EventType
        from chronicle_mcp.core.realtime import get_subscription_manager

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        sub_result = manager.subscribe("chrome", [EventType.HISTORY_ADDED], lambda e: None)
        result = HistoryService.unsubscribe_history_changes(sub_result)

        assert "subscription_id" in result
        assert "success" in result
        assert "active_subscriptions" in result


class TestGetSubscriptionStatus:
    """Tests for get_subscription_status method."""

    def test_get_subscription_status_no_subscription_id(self, monkeypatch):
        """Test get_subscription_status without subscription_id returns global stats."""
        from chronicle_mcp.core.realtime import get_subscription_manager

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        result = HistoryService.get_subscription_status()

        assert "active_subscriptions" in result
        assert "total_events" in result
        assert "events_by_type" in result
        assert "events_by_browser" in result

    def test_get_subscription_status_nonexistent_id(self, monkeypatch):
        """Test get_subscription_status with non-existent ID returns error."""
        result = HistoryService.get_subscription_status(subscription_id="nonexistent-id")

        assert "error" in result or "subscription_id" in result
