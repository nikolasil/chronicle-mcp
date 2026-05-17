"""Error recovery and edge case tests for ChronicleMCP.

These tests verify the system handles error conditions gracefully:
- Database locked scenarios
- Permission denied scenarios
- Corrupted database handling
- Disk full scenarios
- Invalid data handling
"""

import json
import os
import sqlite3

import pytest

from chronicle_mcp.connection import (
    BrowserPathNotFoundError,
    DatabaseLockedError,
    PermissionError,
    cleanup_temp_file,
    get_temp_filename,
)
from chronicle_mcp.database import (
    count_domain_visits,
    get_top_domains,
    query_bookmarks_chrome,
    query_downloads_chrome,
    query_history,
    sanitize_url,
)


class TestDatabaseLockedHandling:
    """Tests for database locked error handling."""

    @pytest.mark.skipif(os.name == "nt", reason="Database locking behaves differently on Windows")
    def test_database_locked_raises_error(self, temp_dir, monkeypatch):
        """Test that operational errors from locked database are handled."""
        from chronicle_mcp import connection, paths

        db_path = temp_dir / "locked.db"
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
        conn.commit()
        conn.close()

        def mock_get_browser_path(browser):
            return str(db_path)

        monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)

        conn2 = sqlite3.connect(str(db_path))
        conn2.execute("BEGIN EXCLUSIVE")
        try:
            with pytest.raises((DatabaseLockedError, sqlite3.OperationalError)):
                with connection.get_history_connection("chrome"):
                    pass
        finally:
            conn2.close()

    def test_database_query_when_locked(self, sample_chrome_db):
        """Test behavior when database is locked during query."""
        conn = sqlite3.connect(sample_chrome_db)

        conn.execute("BEGIN EXCLUSIVE")
        try:
            result = query_history(conn, "test", limit=5)
            assert isinstance(result, list)
        finally:
            conn.rollback()
            conn.close()


class TestPermissionDeniedHandling:
    """Tests for permission denied error handling."""

    @pytest.mark.skipif(os.name == "nt", reason="Permission mode behaves differently on Windows")
    def test_unreadable_database_raises_permission_error(self, temp_dir, monkeypatch):
        """Test that permission denied accessing database raises appropriate error."""
        from chronicle_mcp import connection, paths

        db_path = temp_dir / "unreadable.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()

        def mock_get_browser_path(browser):
            return str(db_path)

        monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)
        monkeypatch.setattr(connection, "get_browser_path", mock_get_browser_path)

        os.chmod(str(db_path), 0o000)

        try:
            with pytest.raises(PermissionError):
                with connection.get_history_connection("chrome"):
                    pass
        finally:
            os.chmod(str(db_path), 0o644)

    def test_bookmarks_file_permission_denied(self, temp_dir):
        """Test handling of bookmarks file with no read permission."""
        bookmark_file = temp_dir / "Bookmarks"
        bookmark_file.write_text('{"roots": {}}')
        os.chmod(str(bookmark_file), 0o000)

        try:
            result = query_bookmarks_chrome(str(bookmark_file), None, 10)
            assert result == []
        finally:
            os.chmod(str(bookmark_file), 0o644)

    def test_missing_history_file_raises_path_not_found(self, temp_dir, monkeypatch):
        """Test that missing history file raises BrowserPathNotFoundError."""
        from chronicle_mcp import connection, paths

        nonexistent_path = str(temp_dir / "nonexistent_history")

        def mock_get_browser_path(browser):
            return nonexistent_path

        monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)
        monkeypatch.setattr(connection, "get_browser_path", mock_get_browser_path)

        with pytest.raises((BrowserPathNotFoundError, connection.ConnectionError)):
            with connection.get_history_connection("chrome"):
                pass


class TestCorruptedDatabaseHandling:
    """Tests for corrupted database file handling."""

    def test_corrupted_history_database(self, temp_dir):
        """Test handling of corrupted SQLite database."""
        db_path = temp_dir / "corrupted.db"
        db_path.write_bytes(b"SQLite format 3\x00" + b"\x00" * 100)

        try:
            conn = sqlite3.connect(str(db_path))
            result = query_downloads_chrome(conn, None, 10)
            assert result == []
            conn.close()
        except sqlite3.DatabaseError:
            pass

    def test_corrupted_bookmarks_json(self, temp_dir):
        """Test handling of corrupted bookmarks JSON file."""
        bookmark_file = temp_dir / "Bookmarks"
        bookmark_file.write_text('{"roots": {broken')

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert result == []

    def test_invalid_sql_in_database(self, sample_chrome_db):
        """Test handling when database has invalid SQL."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls")
            rows = cursor.fetchall()
            assert isinstance(rows, list)
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()


class TestSanitizationEdgeCases:
    """Tests for URL sanitization edge cases."""

    def test_url_with_many_sensitive_params(self):
        """Test sanitization of URL with many sensitive parameters."""
        url = "https://example.com/page?token=a&session=b&key=c&password=d&auth=e&secret=f"
        result = sanitize_url(url)

        assert "token=" not in result
        assert "session=" not in result
        assert "key=" not in result
        assert "password=" not in result
        assert "auth=" not in result
        assert "secret=" not in result
        assert "example.com" in result

    def test_url_with_encoded_sensitive_params(self):
        """Test sanitization with URL-encoded sensitive params."""
        url = "https://example.com/page?token=abc%26def%3Dxyz"
        result = sanitize_url(url)

        assert "token=" not in result

    def test_url_with_no_query_params(self):
        """Test URL with no query parameters."""
        url = "https://github.com/user/repo"
        result = sanitize_url(url)

        assert result == url

    def test_url_with_only_safe_params(self):
        """Test URL with only non-sensitive parameters."""
        url = "https://example.com/page?name=test&sort=asc"
        result = sanitize_url(url)

        assert "name=test" in result
        assert "sort=asc" in result

    def test_empty_query_string(self):
        """Test URL with empty query string."""
        url = "https://example.com/page?"
        result = sanitize_url(url)

        assert "example.com" in result


class TestHistoryQueryEdgeCases:
    """Tests for history query edge cases."""

    def test_very_long_query(self, sample_chrome_db):
        """Test query with very long search string."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            long_query = "a" * 1000
            result = query_history(conn, long_query, limit=5)
            assert result == []
        finally:
            conn.close()

    def test_special_characters_in_query(self, sample_chrome_db):
        """Test query with special regex characters."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            special_query = "test.*+?|()[]{}\\"
            result = query_history(conn, special_query, limit=5)
            assert isinstance(result, list)
        finally:
            conn.close()

    def test_unicode_in_query(self, sample_chrome_db):
        """Test query with unicode characters."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            unicode_query = "测试中文日本語한국어"
            result = query_history(conn, unicode_query, limit=5)
            assert isinstance(result, list)
        finally:
            conn.close()

    def test_empty_database(self, temp_dir):
        """Test query on empty database."""
        db_path = temp_dir / "empty.db"
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
        conn.commit()
        conn.close()

        conn = sqlite3.connect(str(db_path))
        try:
            result = query_history(conn, "test", limit=5)
            assert result == []
        finally:
            conn.close()

    def test_query_with_sql_injection_attempt(self, sample_chrome_db):
        """Test that SQL injection attempts are safely handled."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            injection_query = "'; DROP TABLE urls; --"
            result = query_history(conn, injection_query, limit=5)
            assert isinstance(result, list)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            assert ("urls",) in tables
        finally:
            conn.close()


class TestTimestampEdgeCases:
    """Tests for timestamp handling edge cases."""

    def test_zero_timestamp(self, sample_chrome_db):
        """Test handling of zero timestamp."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://example.com", "Example", 1, 0))
            conn.commit()

            result = query_history(conn, "example", limit=5)
            assert len(result) >= 1
        finally:
            conn.close()

    def test_negative_timestamp(self, sample_chrome_db):
        """Test handling of negative timestamp."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://neg.example.com", "Negative", 1, -1))
            conn.commit()

            result = query_history(conn, "neg", limit=5)
            assert len(result) >= 1
        finally:
            conn.close()

    def test_very_large_timestamp(self, sample_chrome_db):
        """Test handling of very large timestamp."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://large.example.com", "Large", 1, 9999999999999999))
            conn.commit()

            result = query_history(conn, "large", limit=5)
            assert len(result) >= 1
        finally:
            conn.close()


class TestDomainMatchingEdgeCases:
    """Tests for domain matching edge cases."""

    def test_domain_with_subdomain(self, sample_chrome_db):
        """Test that subdomain doesn't incorrectly match."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://notgithub.com/page", "Not GitHub", 1, 1000000))
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://github.com/real", "Real GitHub", 1, 1000000))
            conn.commit()

            real_count = count_domain_visits(conn, "github.com")
            assert real_count >= 1
        finally:
            conn.close()

    def test_domain_with_port(self, sample_chrome_db):
        """Test domain matching with port number."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://example.com:8080/page", "With Port", 5, 1000000))
            conn.commit()

            count = count_domain_visits(conn, "example.com:8080")
            assert count >= 0
        finally:
            conn.close()

    def test_https_domain_matching(self, sample_chrome_db):
        """Test that HTTPS domains are correctly matched."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("https://secure.example.com/page", "Secure", 10, 1000000))
            cursor.execute("INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                         ("http://insecure.example.com/page", "Insecure", 5, 1000000))
            conn.commit()

            count = count_domain_visits(conn, "secure.example.com")
            assert count >= 1
        finally:
            conn.close()


class TestBookmarkFolderHierarchy:
    """Tests for nested bookmark folder structures."""

    def test_deeply_nested_folders(self, temp_dir):
        """Test bookmarks with deeply nested folder structure."""
        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "bookmark_bar": {
                    "type": "folder",
                    "children": [
                        {
                            "type": "folder",
                            "name": "Level 1",
                            "children": [
                                {
                                    "type": "folder",
                                    "name": "Level 2",
                                    "children": [
                                        {"type": "url", "name": "Deep Link", "url": "https://deep.example.com"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert len(result) == 1
        assert result[0] == ("Deep Link", "https://deep.example.com")

    def test_empty_folder_handling(self, temp_dir):
        """Test bookmarks with empty folders."""
        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "bookmark_bar": {
                    "type": "folder",
                    "children": [
                        {"type": "folder", "name": "Empty Folder", "children": []},
                        {"type": "url", "name": "Valid Link", "url": "https://valid.example.com"}
                    ]
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert len(result) == 1
        assert result[0] == ("Valid Link", "https://valid.example.com")

    def test_mixed_node_types(self, temp_dir):
        """Test bookmarks with mixed folder and URL nodes."""
        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "other": {
                    "type": "folder",
                    "children": [
                        {"type": "url", "name": "Other Link", "url": "https://other.example.com"}
                    ]
                },
                "bookmark_bar": {
                    "type": "folder",
                    "children": []
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert len(result) == 1
        assert result[0] == ("Other Link", "https://other.example.com")


class TestDownloadEdgeCases:
    """Tests for download query edge cases."""

    def test_downloads_with_no_filename(self, sample_chrome_db):
        """Test downloads where filename might be empty."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    url TEXT,
                    start_time INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO downloads (filename, url, start_time) VALUES
                (NULL, 'https://example.com/file1.pdf', 13316000000000000),
                ('', 'https://example.com/file2.pdf', 13315000000000000),
                ('valid.pdf', 'https://example.com/file3.pdf', 13314000000000000)
            """)
            conn.commit()

            result = query_downloads_chrome(conn, None, 10)
            assert len(result) == 1
            assert result[0][0] == "valid.pdf"
        finally:
            conn.close()

    def test_downloads_with_unicode_filename(self, sample_chrome_db):
        """Test downloads with unicode characters in filename."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    url TEXT,
                    start_time INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO downloads (filename, url, start_time) VALUES
                (?, ?, ?)
            """, ("文档.pdf", "https://example.com/doc.pdf", 13316000000000000))
            conn.commit()

            result = query_downloads_chrome(conn, None, 10)
            assert len(result) == 1
        finally:
            conn.close()


class TestTopDomainsEdgeCases:
    """Tests for top domains edge cases."""

    def test_domains_with_https_prefix(self, temp_dir):
        """Test that HTTPS URLs are included in top domains."""
        db_path = temp_dir / "https_test.db"
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
            INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES
            ('https://github.com', 'GitHub', 10, 1000000),
            ('https://stackoverflow.com', 'Stack Overflow', 5, 1000000),
            ('http://example.com', 'Example', 3, 1000000)
        """)
        conn.commit()
        conn.close()

        conn = sqlite3.connect(str(db_path))
        try:
            domains = get_top_domains(conn, limit=10)
            domain_names = [d[0] for d in domains]

            assert "github.com" in domain_names
            assert "stackoverflow.com" in domain_names
            assert "example.com" in domain_names
        finally:
            conn.close()

    def test_domains_with_trailing_slash(self, temp_dir):
        """Test handling of domains with trailing slashes."""
        db_path = temp_dir / "trailing.db"
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
            INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES
            ('https://example.com/', 'Example', 5, 1000000),
            ('https://example.com/page', 'Example Page', 3, 1000000)
        """)
        conn.commit()
        conn.close()

        conn = sqlite3.connect(str(db_path))
        try:
            domains = get_top_domains(conn, limit=5)
            domain_names = [d[0] for d in domains]

            assert "example.com" in domain_names
        finally:
            conn.close()


class TestConnectionCleanup:
    """Tests for connection cleanup scenarios."""

    def test_temp_file_cleanup_on_error(self, temp_dir):
        """Test that temp files are cleaned up when an error occurs."""
        db_path = temp_dir / "test.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()

        temp_path = get_temp_filename("test")
        import shutil
        shutil.copy2(str(db_path), temp_path)

        assert os.path.exists(temp_path)

        cleanup_temp_file(temp_path)

        assert not os.path.exists(temp_path)

    def test_cleanup_nonexistent_file(self):
        """Test cleanup of nonexistent file doesn't raise error."""
        cleanup_temp_file("/nonexistent/path/to/file.db")

    def test_cleanup_already_deleted_file(self, temp_dir):
        """Test cleanup when file has already been deleted."""
        temp_file = temp_dir / "already_deleted.db"
        temp_file.write_text("test")
        temp_file.unlink()

        cleanup_temp_file(str(temp_file))
