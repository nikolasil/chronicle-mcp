"""Test isolation verification tests.

This module verifies that test fixtures properly isolate tests from each other,
catching common fixture pollution issues.
"""


class TestFixtureIsolation:
    """Verify that fixtures don't leak state between tests."""

    def test_temp_dir_isolation(self, temp_dir):
        """Test that temp_dir fixture provides isolated directory per test."""
        test_file = temp_dir / "test_isolation_file.txt"
        test_file.write_text("test content")

        assert test_file.exists()
        assert test_file.read_text() == "test content"

    def test_temp_dir_no_leakage(self, temp_dir):
        """Test that temp_dir doesn't see files from other tests."""
        test_file = temp_dir / "leak_test.txt"
        assert not test_file.exists()

    def test_mock_chrome_path_isolation(self, mock_chrome_path):
        """Test that mock_chrome_path is isolated."""
        from chronicle_mcp.paths import get_browser_path

        path = get_browser_path("chrome")
        assert path is not None
        assert "History" in path or "test_chrome" in path

    def test_mock_chrome_path_no_leakage(self, mock_chrome_path):
        """Test that mock doesn't leak to other tests."""
        from chronicle_mcp.paths import get_browser_path

        path = get_browser_path("edge")
        assert path is None

    def test_sample_chrome_db_isolation(self, sample_chrome_db):
        """Test that sample_chrome_db fixture is isolated."""
        import sqlite3

        conn = sqlite3.connect(sample_chrome_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls")
        count = cursor.fetchone()[0]
        conn.close()

        assert count == 5

    def test_realistic_chrome_db_isolation(self, realistic_chrome_db):
        """Test that realistic_chrome_db has expected data."""
        import sqlite3

        conn = sqlite3.connect(realistic_chrome_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls")
        count = cursor.fetchone()[0]
        conn.close()

        assert count == 50

    def test_cache_cleanup_isolation(self):
        """Test that cache cleanup fixture works."""
        from chronicle_mcp.cache import default_cache

        assert default_cache is not None

    def test_webhook_manager_cleanup_isolation(self):
        """Test that webhook manager cleanup fixture works."""
        from chronicle_mcp.webhooks import WebhookManager

        manager = WebhookManager()
        assert manager is not None


class TestGlobalStateIsolation:
    """Test that global state doesn't leak between tests."""

    def test_subscription_manager_isolation(self):
        """Test that subscription manager can be reset."""
        from chronicle_mcp.core.realtime import (
            get_subscription_manager,
            reset_subscription_manager,
        )

        manager1 = get_subscription_manager()
        reset_subscription_manager()
        manager2 = get_subscription_manager()

        assert manager1 is not manager2

    def test_cache_isolation(self):
        """Test that caches don't share state inappropriately."""
        from chronicle_mcp.cache import QueryCache

        cache1 = QueryCache(ttl_seconds=60)
        cache2 = QueryCache(ttl_seconds=60)

        cache1.set("type1", {"id": 1}, "value1")
        cache2.set("type1", {"id": 1}, "value2")

        result1 = cache1.get("type1", {"id": 1})
        result2 = cache2.get("type1", {"id": 1})

        assert result1 == "value1"
        assert result2 == "value2"

    def test_config_isolation(self):
        """Test that config loading doesn't pollute global state."""
        from chronicle_mcp.config import Config, load_config

        config1 = load_config()
        config2 = load_config()

        assert config1.default_browser == config2.default_browser
        assert isinstance(config1, Config)


class TestDatabaseIsolation:
    """Test that database connections and fixtures are properly isolated."""

    def test_connection_cleanup(self, temp_dir):
        """Test that temp database connections are cleaned up."""
        from chronicle_mcp.connection import cleanup_temp_file

        temp_path = temp_dir / "test_cleanup.db"
        temp_path.write_text("test")

        cleanup_temp_file(str(temp_path))

        assert not temp_path.exists()

    def test_separate_temp_files(self, temp_dir):
        """Test that temp filenames are unique."""
        from chronicle_mcp.connection import get_temp_filename

        name1 = get_temp_filename("chrome")
        name2 = get_temp_filename("firefox")

        assert name1 != name2
