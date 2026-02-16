import os
from pathlib import Path

from chronicle_mcp.paths import (
    BOOKMARK_PATHS,
    BROWSER_PATHS,
    DOWNLOAD_PATHS,
    expand_path,
    find_glob_path,
    get_all_browser_paths,
    get_available_bookmarks,
    get_available_browsers,
    get_available_downloads,
    get_bookmark_path,
    get_browser_path,
    get_download_path,
)


class TestPathDetection:
    """Tests for browser path detection functionality."""

    def test_expand_path_home_directory(self):
        """Test that home directory expansion works."""
        result = expand_path("~/test/path")
        assert result.endswith("/test/path") or result.endswith("\\test\\path")
        assert not result.startswith("~")

    def test_expand_path_environment_variables(self, monkeypatch):
        """Test that environment variable expansion works."""
        monkeypatch.setenv("TEST_VAR", "expanded_value")
        result = expand_path("$TEST_VAR/path")
        assert "expanded_value" in result

    def test_find_glob_path_single_match(self, temp_dir):
        """Test glob pattern matching with single result."""
        test_file = os.path.join(temp_dir, "test.db")
        Path(test_file).touch()

        result = find_glob_path(os.path.join(temp_dir, "*.db"))
        assert result == test_file

    def test_find_glob_path_no_match(self, temp_dir):
        """Test glob pattern with no matches returns None."""
        result = find_glob_path(os.path.join(temp_dir, "nonexistent/*.db"))
        assert result is None

    def test_get_browser_path_invalid_browser(self):
        """Test that invalid browser returns None."""
        result = get_browser_path("invalid_browser")
        assert result is None

    def test_get_browser_path_case_insensitive(self):
        """Test that browser names are case insensitive."""
        result_lower = get_browser_path("chrome")
        result_upper = get_browser_path("CHROME")
        result_mixed = get_browser_path("Chrome")

        assert result_lower == result_upper == result_mixed

    def test_get_available_browsers_none_found(self, monkeypatch):
        """Test get_available_browsers when no browsers are found."""
        import chronicle_mcp.paths as paths

        monkeypatch.setattr(paths, "get_browser_path", lambda b: None)

        result = get_available_browsers()
        assert result == []

    def test_get_all_browser_paths_structure(self):
        """Test that get_all_browser_paths returns correct structure."""
        result = get_all_browser_paths()

        assert isinstance(result, dict)
        for browser in BROWSER_PATHS:
            assert browser in result
            assert result[browser] is None or isinstance(result[browser], str)


class TestBookmarkPathDetection:
    """Tests for bookmark path detection."""

    def test_get_bookmark_path_invalid_browser(self):
        """Test that invalid browser returns None for bookmarks."""
        result = get_bookmark_path("invalid_browser")
        assert result is None

    def test_get_bookmark_path_case_insensitive(self):
        """Test that bookmark path is case insensitive."""
        result_lower = get_bookmark_path("chrome")
        result_upper = get_bookmark_path("CHROME")
        assert result_lower == result_upper

    def test_get_available_bookmarks_none_found(self, monkeypatch):
        """Test get_available_bookmarks when no browsers found."""
        import chronicle_mcp.paths as paths

        monkeypatch.setattr(paths, "get_bookmark_path", lambda b: None)

        result = get_available_bookmarks()
        assert result == []

    def test_bookmark_paths_all_browsers(self):
        """Test that all browsers have bookmark paths defined."""
        for browser in BOOKMARK_PATHS:
            assert browser in BOOKMARK_PATHS
            assert isinstance(BOOKMARK_PATHS[browser], dict)


class TestDownloadPathDetection:
    """Tests for download path detection."""

    def test_get_download_path_invalid_browser(self):
        """Test that invalid browser returns None for downloads."""
        result = get_download_path("invalid_browser")
        assert result is None

    def test_get_download_path_case_insensitive(self):
        """Test that download path is case insensitive."""
        result_lower = get_download_path("chrome")
        result_upper = get_download_path("CHROME")
        assert result_lower == result_upper

    def test_get_available_downloads_none_found(self, monkeypatch):
        """Test get_available_downloads when no browsers found."""
        import chronicle_mcp.paths as paths

        monkeypatch.setattr(paths, "get_download_path", lambda b: None)

        result = get_available_downloads()
        assert result == []

    def test_download_paths_all_browsers(self):
        """Test that all browsers have download paths defined."""
        for browser in DOWNLOAD_PATHS:
            assert browser in DOWNLOAD_PATHS
            assert isinstance(DOWNLOAD_PATHS[browser], dict)
