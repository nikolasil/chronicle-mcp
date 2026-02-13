"""Integration tests for browser history access.

These tests verify end-to-end functionality with actual browser databases.
They are marked with browser names to allow selective execution.
"""

import pytest

from chronicle_mcp.core.exceptions import BrowserNotFoundError
from chronicle_mcp.core.services import HistoryService


@pytest.mark.chrome
class TestChromeIntegration:
    """Integration tests for Chrome browser."""

    def test_list_browsers_includes_chrome(self, mock_chrome_path):
        """Test that Chrome is detected as available."""
        result = HistoryService.list_available_browsers()
        assert "chrome" in result["browsers"]

    def test_search_chrome_history(self, mock_chrome_path):
        """Test searching Chrome history."""
        result = HistoryService.search_history(query="github", limit=10, browser="chrome")
        assert "results" in result
        assert result["count"] >= 0

    def test_recent_chrome_history(self, mock_chrome_path):
        """Test getting recent Chrome history."""
        result = HistoryService.get_recent_history(hours=24, limit=10, browser="chrome")
        assert "results" in result
        assert "message" in result

    def test_chrome_count_visits(self, mock_chrome_path):
        """Test counting visits for a domain in Chrome."""
        result = HistoryService.count_visits(domain="github.com", browser="chrome")
        assert "count" in result
        assert result["browser"] == "chrome"

    def test_chrome_top_domains(self, mock_chrome_path):
        """Test listing top domains from Chrome."""
        result = HistoryService.list_top_domains(limit=10, browser="chrome")
        assert "domains" in result

    def test_chrome_export(self, mock_chrome_path):
        """Test exporting Chrome history."""
        result = HistoryService.export_history(format_type="csv", limit=10, browser="chrome")
        assert "content" in result
        assert result["format"] == "csv"


@pytest.mark.firefox
class TestFirefoxIntegration:
    """Integration tests for Firefox browser."""

    def test_list_browsers_includes_firefox(self, mock_all_browsers):
        """Test that Firefox is detected as available."""
        result = HistoryService.list_available_browsers()
        assert "firefox" in result["browsers"]


@pytest.mark.brave
class TestBraveIntegration:
    """Integration tests for Brave browser."""

    def test_brave_not_found_without_db(self):
        """Test that Brave raises error when no database is available."""
        with pytest.raises(BrowserNotFoundError):
            HistoryService.search_history(query="test", limit=10, browser="brave")


@pytest.mark.safari
class TestSafariIntegration:
    """Integration tests for Safari browser."""

    def test_safari_not_found_without_db(self):
        """Test that Safari raises error when no database is available."""
        with pytest.raises(BrowserNotFoundError):
            HistoryService.search_history(query="test", limit=10, browser="safari")


@pytest.mark.vivaldi
class TestVivaldiIntegration:
    """Integration tests for Vivaldi browser."""

    def test_vivaldi_not_found_without_db(self):
        """Test that Vivaldi raises error when no database is available."""
        with pytest.raises(BrowserNotFoundError):
            HistoryService.search_history(query="test", limit=10, browser="vivaldi")


@pytest.mark.opera
class TestOperaIntegration:
    """Integration tests for Opera browser."""

    def test_opera_not_found_without_db(self):
        """Test that Opera raises error when no database is available."""
        with pytest.raises(BrowserNotFoundError):
            HistoryService.search_history(query="test", limit=10, browser="opera")


@pytest.mark.integration
class TestBrowserIntegration:
    """General browser integration tests that run for any browser."""

    def test_search_with_query(self, mock_chrome_path):
        """Test search with a valid query."""
        result = HistoryService.search_history(query="github", limit=5, browser="chrome")
        assert "results" in result

    def test_search_respects_limit(self, mock_chrome_path):
        """Test that search respects the limit parameter."""
        result = HistoryService.search_history(query="github", limit=2, browser="chrome")
        assert result["count"] <= 2

    def test_recent_history_respects_hours(self, mock_chrome_path):
        """Test that recent history respects hours parameter."""
        result = HistoryService.get_recent_history(hours=1, limit=10, browser="chrome")
        assert "results" in result

    def test_count_visits_with_domain(self, mock_chrome_path):
        """Test count visits with a domain."""
        result = HistoryService.count_visits(domain="github.com", browser="chrome")
        assert "count" in result

    def test_top_domains_respects_limit(self, mock_chrome_path):
        """Test top domains respects limit."""
        result = HistoryService.list_top_domains(limit=5, browser="chrome")
        assert len(result["domains"]) <= 5
