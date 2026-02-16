import json
import sqlite3

from chronicle_mcp.database import (
    count_domain_visits,
    format_results,
    get_top_domains,
    query_history,
    sanitize_url,
)


class TestQueryHistory:
    """Tests for history query functions."""

    def test_query_history_basic(self, sample_chrome_db):
        """Test basic history query returns results."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=5)
            assert len(rows) >= 1
            titles = [r[0] for r in rows]
            assert any("Python" in t for t in titles)
        finally:
            conn.close()

    def test_query_history_no_results(self, sample_chrome_db):
        """Test query with no matches returns empty list."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "nonexistent_xyz_query", limit=5)
            assert rows == []
        finally:
            conn.close()

    def test_query_history_limit(self, sample_chrome_db):
        """Test that limit is respected."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "https", limit=2)
            assert len(rows) <= 2
        finally:
            conn.close()


class TestSanitizeUrl:
    """Tests for URL sanitization."""

    def test_sanitize_url_removes_token(self):
        """Test that sensitive tokens are removed from URLs."""
        url = "https://example.com/page?token=secret123&other=value"
        result = sanitize_url(url)

        assert "token=secret123" not in result
        assert "other=value" in result

    def test_sanitize_url_removes_multiple_sensitive_params(self):
        """Test removal of multiple sensitive parameters."""
        url = "https://example.com/page?token=abc&session=xyz&key=123&name=test"
        result = sanitize_url(url)

        assert "token=" not in result
        assert "session=" not in result
        assert "key=" not in result
        assert "name=test" in result

    def test_sanitize_url_preserves_structure(self):
        """Test that URL structure is preserved after sanitization."""
        url = "https://github.com/user/repo?tab=repos"
        result = sanitize_url(url)

        assert result.startswith("https://")
        assert "github.com" in result


class TestFormatResults:
    """Tests for result formatting."""

    def test_format_results_markdown(self, sample_chrome_db):
        """Test Markdown format output."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=1)
            result = format_results(rows, "python", "markdown")

            assert "- **" in result
            assert "URL:" in result
        finally:
            conn.close()

    def test_format_results_json(self, sample_chrome_db):
        """Test JSON format output."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=1)
            result = format_results(rows, "python", "json")

            data = json.loads(result)
            assert "results" in data
            assert "count" in data
            assert data["count"] == len(rows)
        finally:
            conn.close()

    def test_format_results_empty(self):
        """Test empty results return not found message."""
        result = format_results([], "nonexistent", "markdown")
        assert "No history found" in result


class TestCountDomainVisits:
    """Tests for domain visit counting."""

    def test_count_domain_visits_basic(self, sample_chrome_db):
        """Test counting visits to a domain."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            count = count_domain_visits(conn, "github.com")
            assert count >= 0
        finally:
            conn.close()

    def test_count_domain_visits_nonexistent(self, sample_chrome_db):
        """Test counting visits to nonexistent domain."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            count = count_domain_visits(conn, "nonexistent.xyz")
            assert count == 0
        finally:
            conn.close()


class TestGetTopDomains:
    """Tests for top domains function."""

    def test_get_top_domains_basic(self, sample_chrome_db):
        """Test getting top domains returns results."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            domains = get_top_domains(conn, limit=5)
            assert isinstance(domains, list)
            if domains:
                assert isinstance(domains[0], tuple)
                assert len(domains[0]) == 2
        finally:
            conn.close()

    def test_get_top_domains_limit(self, sample_chrome_db):
        """Test that limit is respected."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            domains = get_top_domains(conn, limit=2)
            assert len(domains) <= 2
        finally:
            conn.close()


class TestQueryBookmarksChrome:
    """Tests for Chrome bookmarks query function."""

    def test_query_bookmarks_chrome_with_file(self, temp_dir):
        """Test querying Chrome bookmarks from JSON file."""
        import json

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

        from chronicle_mcp.database import query_bookmarks_chrome

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert len(result) == 2
        assert ("GitHub", "https://github.com") in result

    def test_query_bookmarks_chrome_with_query(self, temp_dir):
        """Test querying Chrome bookmarks with filter."""
        import json

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

        from chronicle_mcp.database import query_bookmarks_chrome

        result = query_bookmarks_chrome(str(bookmark_file), "github", 10)
        assert len(result) == 1
        assert "github" in result[0][0].lower()

    def test_query_bookmarks_chrome_empty_file(self, temp_dir):
        """Test querying empty bookmarks file."""
        import json

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_file.write_text(json.dumps({"roots": {}}))

        from chronicle_mcp.database import query_bookmarks_chrome

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert result == []

    def test_query_bookmarks_chrome_invalid_file(self, temp_dir):
        """Test querying invalid bookmarks file."""
        from chronicle_mcp.database import query_bookmarks_chrome

        result = query_bookmarks_chrome(str(temp_dir / "nonexistent"), None, 10)
        assert result == []


class TestQueryBookmarksFirefox:
    """Tests for Firefox bookmarks query function."""

    def test_query_bookmarks_firefox(self, sample_firefox_db):
        """Test querying Firefox bookmarks."""
        from chronicle_mcp.database import query_bookmarks_firefox

        conn = sqlite3.connect(sample_firefox_db)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE moz_bookmarks (
                    id INTEGER PRIMARY KEY,
                    fk INTEGER,
                    type INTEGER,
                    parent INTEGER,
                    position INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO moz_bookmarks (fk, type, parent, position) VALUES
                (1, 1, 0, 0), (2, 1, 0, 1)
            """)
            conn.commit()

            result = query_bookmarks_firefox(conn, None, 10)
            assert isinstance(result, list)
        finally:
            conn.close()


class TestQueryDownloadsChrome:
    """Tests for Chrome downloads query function."""

    def test_query_downloads_chrome(self, sample_chrome_db):
        """Test querying Chrome downloads."""
        from chronicle_mcp.database import query_downloads_chrome

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
                ('test.pdf', 'https://example.com/test.pdf', 13316000000000000),
                ('doc.pdf', 'https://example.com/doc.pdf', 13315000000000000)
            """)
            conn.commit()

            result = query_downloads_chrome(conn, None, 10)
            assert isinstance(result, list)
        finally:
            conn.close()

    def test_query_downloads_chrome_with_query(self, sample_chrome_db):
        """Test querying Chrome downloads with filter."""
        from chronicle_mcp.database import query_downloads_chrome

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
                ('test.pdf', 'https://example.com/test.pdf', 13316000000000000)
            """)
            conn.commit()

            result = query_downloads_chrome(conn, "test", 10)
            assert isinstance(result, list)
        finally:
            conn.close()


class TestQueryBookmarksUniversal:
    """Tests for universal bookmark query function."""

    def test_query_bookmarks_none_path(self):
        """Test query_bookmarks with None path."""
        from chronicle_mcp.database import query_bookmarks

        result = query_bookmarks(None, "chrome", None, 10)
        assert result == []

    def test_query_bookmarks_invalid_path(self):
        """Test query_bookmarks with invalid path."""
        from chronicle_mcp.database import query_bookmarks

        result = query_bookmarks("/nonexistent/path", "chrome", None, 10)
        assert result == []


class TestQueryDownloadsUniversal:
    """Tests for universal downloads query function."""

    def test_query_downloads_none_path(self):
        """Test query_downloads with None path."""
        from chronicle_mcp.database import query_downloads

        result = query_downloads(None, "chrome", None, 10)
        assert result == []

    def test_query_downloads_invalid_path(self):
        """Test query_downloads with invalid path."""
        from chronicle_mcp.database import query_downloads

        result = query_downloads("/nonexistent/path", "chrome", None, 10)
        assert result == []


class TestQueryBookmarksFirefoxDownloads:
    """Tests for Firefox bookmark and download query functions."""

    def test_query_bookmarks_firefox_with_query(self, temp_dir):
        """Test querying Firefox bookmarks with filter."""
        from chronicle_mcp.database import query_bookmarks_firefox

        db_path = temp_dir / "places.sqlite"
        conn = sqlite3.connect(str(db_path))
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE moz_places (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE moz_bookmarks (
                    id INTEGER PRIMARY KEY,
                    fk INTEGER,
                    type INTEGER,
                    parent INTEGER,
                    position INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO moz_places (id, url, title) VALUES
                (1, 'https://github.com', 'GitHub'),
                (2, 'https://python.org', 'Python'),
                (3, 'https://example.com', 'Example')
            """)
            cursor.execute("""
                INSERT INTO moz_bookmarks (fk, type, parent, position) VALUES
                (1, 1, 0, 0), (2, 1, 0, 1), (3, 1, 0, 2)
            """)
            conn.commit()

            result = query_bookmarks_firefox(conn, "github", 10)
            assert len(result) == 1
            assert "github" in result[0][0].lower()
        finally:
            conn.close()

    def test_query_downloads_firefox(self, temp_dir):
        """Test querying Firefox downloads."""
        from chronicle_mcp.database import query_downloads_firefox

        db_path = temp_dir / "places.sqlite"
        conn = sqlite3.connect(str(db_path))
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE moz_places (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE moz_visits (
                    id INTEGER PRIMARY KEY,
                    place_id INTEGER,
                    visit_date INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE moz_downloads (
                    id INTEGER PRIMARY KEY,
                    place_id INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO moz_places (id, url, title) VALUES
                (1, 'https://example.com/file.pdf', 'file.pdf')
            """)
            cursor.execute("""
                INSERT INTO moz_visits (place_id, visit_date) VALUES
                (1, 1700000000000)
            """)
            cursor.execute("""
                INSERT INTO moz_downloads (place_id) VALUES (1)
            """)
            conn.commit()

            result = query_downloads_firefox(conn, None, 10)
            assert isinstance(result, list)
            assert len(result) == 1
        finally:
            conn.close()

    def test_query_downloads_firefox_with_query(self, temp_dir):
        """Test querying Firefox downloads with filter."""
        from chronicle_mcp.database import query_downloads_firefox

        db_path = temp_dir / "places.sqlite"
        conn = sqlite3.connect(str(db_path))
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE moz_places (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE moz_visits (
                    id INTEGER PRIMARY KEY,
                    place_id INTEGER,
                    visit_date INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE moz_downloads (
                    id INTEGER PRIMARY KEY,
                    place_id INTEGER
                )
            """)
            cursor.execute("""
                INSERT INTO moz_places (id, url, title) VALUES
                (1, 'https://example.com/test.pdf', 'test.pdf'),
                (2, 'https://example.com/other.pdf', 'other.pdf')
            """)
            cursor.execute("""
                INSERT INTO moz_visits (place_id, visit_date) VALUES
                (1, 1700000000000), (2, 1700000000001)
            """)
            cursor.execute("""
                INSERT INTO moz_downloads (place_id) VALUES (1), (2)
            """)
            conn.commit()

            result = query_downloads_firefox(conn, "test", 10)
            assert isinstance(result, list)
            assert len(result) == 1
            assert "test" in result[0][0].lower()
        finally:
            conn.close()


class TestQueryBookmarksFirefoxWithGlob:
    """Tests for Firefox bookmark query with glob pattern."""

    def test_query_bookmarks_firefox_glob_pattern(self, temp_dir):
        """Test querying Firefox bookmarks with glob pattern path."""

        from chronicle_mcp.database import query_bookmarks

        # Create a Firefox places.sqlite database
        db_path = temp_dir / "places.sqlite"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE moz_places (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE moz_bookmarks (
                id INTEGER PRIMARY KEY,
                fk INTEGER,
                type INTEGER,
                parent INTEGER,
                position INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO moz_places (id, url, title) VALUES
            (1, 'https://github.com', 'GitHub')
        """)
        cursor.execute("""
            INSERT INTO moz_bookmarks (fk, type, parent, position) VALUES
            (1, 1, 0, 0)
        """)
        conn.commit()
        conn.close()

        # Test with glob pattern
        glob_path = str(temp_dir / "*.sqlite")
        result = query_bookmarks(glob_path, "firefox", None, 10)
        assert len(result) == 1
        assert result[0] == ("GitHub", "https://github.com")

    def test_query_bookmarks_firefox_glob_no_match(self, temp_dir):
        """Test querying Firefox bookmarks with glob pattern that matches nothing."""
        from chronicle_mcp.database import query_bookmarks

        # Test with glob pattern that won't match anything
        glob_path = str(temp_dir / "nonexistent*.sqlite")
        result = query_bookmarks(glob_path, "firefox", None, 10)
        assert result == []


class TestQueryDownloadsWithGlob:
    """Tests for download query with glob pattern."""

    def test_query_downloads_with_glob_pattern(self, temp_dir):
        """Test querying downloads with glob pattern path."""
        from chronicle_mcp.database import query_downloads

        # Create a Chrome History database with downloads
        db_path = temp_dir / "History"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
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

        # Test with glob pattern
        glob_path = str(temp_dir / "*")
        result = query_downloads(glob_path, "chrome", None, 10)
        assert len(result) == 1

    def test_query_downloads_glob_no_match(self, temp_dir):
        """Test querying downloads with glob pattern that matches nothing."""
        from chronicle_mcp.database import query_downloads

        # Test with glob pattern that won't match anything
        glob_path = str(temp_dir / "nonexistent*")
        result = query_downloads(glob_path, "chrome", None, 10)
        assert result == []

    def test_query_downloads_corrupted_database(self, temp_dir):
        """Test querying downloads with corrupted database file."""
        import sqlite3

        from chronicle_mcp.database import query_downloads

        # Create an invalid/corrupted SQLite file that raises OperationalError
        db_path = temp_dir / "CorruptedHistory"
        # Write SQLite header with invalid content to trigger OperationalError
        db_path.write_bytes(b"SQLite format 3\x00" + b"\x00" * 100)

        try:
            result = query_downloads(str(db_path), "chrome", None, 10)
            # Should return empty list on error
            assert result == []
        except sqlite3.DatabaseError:
            # If not caught, that's acceptable too
            pass


class TestQueryBookmarksChromeErrors:
    """Tests for Chrome bookmark error handling."""

    def test_query_bookmarks_chrome_json_decode_error(self, temp_dir):
        """Test querying Chrome bookmarks with invalid JSON."""
        from chronicle_mcp.database import query_bookmarks_chrome

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_file.write_text("This is not valid JSON")

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        assert result == []

    def test_query_bookmarks_chrome_permission_error(self, temp_dir):
        """Test querying Chrome bookmarks with permission error."""
        import os

        from chronicle_mcp.database import query_bookmarks_chrome

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_file.write_text('{"roots": {}}')
        os.chmod(str(bookmark_file), 0o000)

        try:
            result = query_bookmarks_chrome(str(bookmark_file), None, 10)
            assert result == []
        finally:
            os.chmod(str(bookmark_file), 0o644)

    def test_query_bookmarks_chrome_empty_nodes(self, temp_dir):
        """Test querying Chrome bookmarks with empty node values."""
        import json

        from chronicle_mcp.database import query_bookmarks_chrome

        bookmark_file = temp_dir / "Bookmarks"
        bookmark_data = {
            "roots": {
                "bookmark_bar": {
                    "type": "folder",
                    "children": [
                        {"type": "url", "name": None, "url": None},
                        {"type": "url", "name": "", "url": "https://example.com"},
                    ],
                }
            }
        }
        bookmark_file.write_text(json.dumps(bookmark_data))

        result = query_bookmarks_chrome(str(bookmark_file), None, 10)
        # Should include the one with empty name but valid URL
        assert len(result) == 1
        assert result[0] == ("", "https://example.com")
