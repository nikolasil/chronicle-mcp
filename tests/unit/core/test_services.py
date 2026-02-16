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
