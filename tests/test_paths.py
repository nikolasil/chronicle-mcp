import pytest
import os
import tempfile
from pathlib import Path


class TestPathDetection:
    """Tests for browser path detection functionality."""

    def test_expand_path_home_directory(self):
        """Test that home directory expansion works."""
        from chronicle_mcp.paths import expand_path

        result = expand_path("~/test/path")
        assert result.endswith("/test/path")
        assert not result.startswith("~")

    def test_expand_path_environment_variables(self, monkeypatch):
        """Test that environment variable expansion works."""
        from chronicle_mcp.paths import expand_path

        monkeypatch.setenv("TEST_VAR", "expanded_value")
        result = expand_path("$TEST_VAR/path")
        assert "expanded_value" in result

    def test_find_glob_path_single_match(self, temp_dir):
        """Test glob pattern matching with single result."""
        from chronicle_mcp.paths import find_glob_path

        test_file = os.path.join(temp_dir, "test.db")
        Path(test_file).touch()

        result = find_glob_path(os.path.join(temp_dir, "*.db"))
        assert result == test_file

    def test_find_glob_path_no_match(self, temp_dir):
        """Test glob pattern with no matches returns None."""
        from chronicle_mcp.paths import find_glob_path

        result = find_glob_path(os.path.join(temp_dir, "nonexistent/*.db"))
        assert result is None

    def test_get_browser_path_invalid_browser(self):
        """Test that invalid browser returns None."""
        from chronicle_mcp.paths import get_browser_path

        result = get_browser_path("invalid_browser")
        assert result is None

    def test_get_browser_path_case_insensitive(self):
        """Test that browser names are case insensitive."""
        from chronicle_mcp.paths import get_browser_path

        result_lower = get_browser_path("chrome")
        result_upper = get_browser_path("CHROME")
        result_mixed = get_browser_path("Chrome")

        assert result_lower == result_upper == result_mixed

    def test_get_available_browsers_none_found(self, monkeypatch):
        """Test get_available_browsers when no browsers are found."""
        from chronicle_mcp import paths

        monkeypatch.setattr(paths, "get_browser_path", lambda b: None)

        result = paths.get_available_browsers()
        assert result == []

    def test_get_all_browser_paths_structure(self):
        """Test that get_all_browser_paths returns correct structure."""
        from chronicle_mcp.paths import get_all_browser_paths, BROWSER_PATHS

        result = get_all_browser_paths()

        assert isinstance(result, dict)
        for browser in BROWSER_PATHS:
            assert browser in result
            assert result[browser] is None or isinstance(result[browser], str)
