import os
import sqlite3
import tempfile

import pytest


@pytest.fixture
def temp_dir():
    """Provides a temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_chrome_db(temp_dir):
    """Creates a synthetic Chrome history database."""
    db_path = os.path.join(temp_dir, "History")
    conn = sqlite3.connect(db_path)
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
        CREATE INDEX idx_url_search ON urls(title, url, last_visit_time)
    """)

    chrome_epoch_offset = 11644473600000000

    test_data = [
        ("https://github.com/anthropics/claude", "Claude - Anthropic", 10, chrome_epoch_offset + 1000000000),
        ("https://stackoverflow.com/questions/123", "Python SQLite Tutorial", 5, chrome_epoch_offset + 900000000),
        ("https://docs.python.org/3/tutorial/", "Python Tutorial", 3, chrome_epoch_offset + 800000000),
        ("https://github.com/microsoft/vscode", "VS Code - Microsoft", 8, chrome_epoch_offset + 700000000),
        ("https://example.com/test?token=secret123", "Test Site with Token", 2, chrome_epoch_offset + 600000000),
    ]

    cursor.executemany(
        "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
        test_data
    )

    conn.commit()
    conn.close()

    return db_path


@pytest.fixture
def sample_firefox_db(temp_dir):
    """Creates a synthetic Firefox places database."""
    db_path = os.path.join(temp_dir, "places.sqlite")
    conn = sqlite3.connect(db_path)
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

    firefox_data = [
        ("https://firefox.com/", "Firefox Browser", 15, 1700000000000),
        ("https://moz.org/", "Mozilla", 5, 1699900000000),
    ]

    cursor.executemany(
        "INSERT INTO moz_places (url, title, visit_count, last_visit_date) VALUES (?, ?, ?, ?)",
        firefox_data
    )

    conn.commit()
    conn.close()

    return db_path


@pytest.fixture
def mock_chrome_path(monkeypatch, sample_chrome_db):
    """Mocks get_browser_path to return our sample database."""
    from chronicle_mcp import paths

    def mock_get_browser_path(browser):
        if browser.lower() == "chrome":
            return sample_chrome_db
        return None

    monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)


@pytest.fixture
def mock_all_browsers(monkeypatch, sample_chrome_db, sample_firefox_db):
    """Mocks multiple browser paths."""
    from chronicle_mcp import paths

    def mock_get_browser_path(browser):
        browser_lower = browser.lower()
        if browser_lower == "chrome":
            return sample_chrome_db
        elif browser_lower == "firefox":
            return sample_firefox_db
        elif browser_lower == "edge":
            return None
        return None

    monkeypatch.setattr(paths, "get_browser_path", mock_get_browser_path)
