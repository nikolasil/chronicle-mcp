import os
import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

CHROME_EPOCH_OFFSET = 11644473600000000


def generate_chrome_timestamp(days_ago: int = 0, hours_ago: int = 0) -> int:
    """Generate a Chrome-style timestamp (microseconds since 1601-01-01)."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_ago)
    chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    return int((cutoff - chrome_epoch).total_seconds() * 1_000_000)


@pytest.fixture
def temp_dir():
    """Provides a temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_chrome_db(temp_dir):
    """Creates a synthetic Chrome history database with 5 entries."""
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

    test_data = [
        (
            "https://github.com/anthropics/claude",
            "Claude - Anthropic",
            10,
            generate_chrome_timestamp(hours_ago=1),
        ),
        (
            "https://stackoverflow.com/questions/123",
            "Python SQLite Tutorial",
            5,
            generate_chrome_timestamp(hours_ago=2),
        ),
        (
            "https://docs.python.org/3/tutorial/",
            "Python Tutorial",
            3,
            generate_chrome_timestamp(hours_ago=3),
        ),
        (
            "https://github.com/microsoft/vscode",
            "VS Code - Microsoft",
            8,
            generate_chrome_timestamp(hours_ago=4),
        ),
        (
            "https://example.com/test?token=secret123",
            "Test Site with Token",
            2,
            generate_chrome_timestamp(hours_ago=5),
        ),
    ]

    cursor.executemany(
        "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)", test_data
    )

    conn.commit()
    conn.close()

    return db_path


@pytest.fixture(scope="session")
def session_temp_dir():
    """Session-scoped temporary directory for heavy fixtures."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(scope="session")
def realistic_chrome_db(session_temp_dir):
    """Creates a realistic Chrome history database with 50 entries (session-scoped).

    Data distribution:
    - GitHub: 10 entries
    - Stack Overflow: 8 entries
    - Documentation: 6 entries
    - News: 8 entries
    - Social: 6 entries
    - Other: 12 entries
    """
    db_path = os.path.join(session_temp_dir, "History_realistic")
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

    test_data = []

    github_entries = [
        ("https://github.com/anthropics/claude", "Claude - Anthropic", 10),
        ("https://github.com/anthropics/claude-code", "Claude Code", 8),
        ("https://github.com/microsoft/vscode", "VS Code - Microsoft", 12),
        ("https://github.com/microsoft/TypeScript", "TypeScript", 7),
        ("https://github.com/facebook/react", "React", 9),
        ("https://github.com/torvalds/linux", "Linux Kernel", 5),
        ("https://github.com/docker/docker-ce", "Docker", 6),
        ("https://github.com/kubernetes/kubernetes", "Kubernetes", 4),
        ("https://github.com/python/cpython", "CPython", 11),
        ("https://github.com/pallets/flask", "Flask", 3),
    ]

    stackoverflow_entries = [
        ("https://stackoverflow.com/questions/123", "Python SQLite Tutorial", 15),
        ("https://stackoverflow.com/questions/456", "JavaScript Closures", 8),
        ("https://stackoverflow.com/questions/789", "React Hooks Guide", 6),
        ("https://stackoverflow.com/questions/321", "TypeScript Generics", 5),
        ("https://stackoverflow.com/questions/654", "Dockerfile Best Practices", 4),
        ("https://stackoverflow.com/questions/987", "Git Merge vs Rebase", 7),
        ("https://stackoverflow.com/questions/234", "Python Async Await", 9),
        ("https://stackoverflow.com/questions/567", "CSS Grid Layout", 3),
    ]

    docs_entries = [
        ("https://docs.python.org/3/tutorial/", "Python Tutorial", 20),
        ("https://docs.python.org/3/library/sqlite3.html", "Python SQLite3", 8),
        ("https://developer.mozilla.org/en-US/docs/Web/JavaScript", "MDN JavaScript", 15),
        ("https://docs.docker.com/get-started/", "Docker Get Started", 5),
        ("https://docs.github.com/en", "GitHub Docs", 7),
        ("https://docs.fastapi.tiangolo.com/", "FastAPI Docs", 6),
    ]

    news_entries = [
        ("https://news.ycombinator.com/", "Hacker News", 25),
        ("https://reddit.com/r/programming", "Reddit Programming", 18),
        ("https://techcrunch.com/", "TechCrunch", 7),
        ("https://www.theverge.com/", "The Verge", 4),
        ("https://wired.com/", "Wired", 3),
        ("https://arstechnica.com/", "Ars Technica", 5),
        ("https://www.infoq.com/", "InfoQ", 4),
        ("https://dev.to/", "Dev.to", 12),
    ]

    social_entries = [
        ("https://twitter.com/", "Twitter / X", 30),
        ("https://linkedin.com/feed", "LinkedIn Feed", 12),
        ("https://discord.com/", "Discord", 15),
        ("https://slack.com/", "Slack", 8),
        ("https://youtube.com/", "YouTube", 20),
        ("https://twitch.tv/", "Twitch", 5),
    ]

    other_entries = [
        ("https://wikipedia.org/", "Wikipedia", 25),
        ("https://chatgpt.com/", "ChatGPT", 15),
        ("https://claude.ai/", "Claude", 10),
        ("https://stackoverflow.com/", "Stack Overflow", 30),
        ("https://github.com/", "GitHub", 40),
        ("https://gitlab.com/", "GitLab", 5),
        ("https://bitbucket.org/", "Bitbucket", 3),
        ("https://codepen.io/", "CodePen", 8),
        ("https://jsfiddle.net/", "JSFiddle", 4),
        ("https://replit.com/", "Replit", 6),
        ("https://codesandbox.io/", "CodeSandbox", 5),
        ("https://glitch.com/", "Glitch", 2),
    ]

    all_entries = (
        github_entries
        + stackoverflow_entries
        + docs_entries
        + news_entries
        + social_entries
        + other_entries
    )

    for i, (url, title, visit_count) in enumerate(all_entries):
        days_ago = (i % 30) + 1
        hours_ago = i % 24
        timestamp = generate_chrome_timestamp(days_ago=days_ago, hours_ago=hours_ago)
        test_data.append((url, title, visit_count, timestamp))

    cursor.executemany(
        "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)", test_data
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
        firefox_data,
    )

    conn.commit()
    conn.close()

    return db_path


def _make_mock_get_browser_path(sample_chrome_db, sample_firefox_db=None):
    """Factory for mock_get_browser_path functions."""

    def mock_get_browser_path(browser):
        browser_lower = browser.lower()
        if browser_lower == "chrome":
            return sample_chrome_db
        elif browser_lower == "firefox" and sample_firefox_db:
            return sample_firefox_db
        elif browser_lower == "edge":
            return None
        return None

    return mock_get_browser_path


@pytest.fixture
def mock_chrome_path(monkeypatch, sample_chrome_db):
    """Mocks get_browser_path to return our sample database."""
    from chronicle_mcp import paths, connection

    mock_fn = _make_mock_get_browser_path(sample_chrome_db)
    monkeypatch.setattr(paths, "get_browser_path", mock_fn)
    monkeypatch.setattr(connection, "get_browser_path", mock_fn)


@pytest.fixture
def mock_all_browsers(monkeypatch, sample_chrome_db, sample_firefox_db):
    """Mocks multiple browser paths."""
    from chronicle_mcp import paths, connection

    mock_fn = _make_mock_get_browser_path(sample_chrome_db, sample_firefox_db)
    monkeypatch.setattr(paths, "get_browser_path", mock_fn)
    monkeypatch.setattr(connection, "get_browser_path", mock_fn)


@pytest.fixture
def mock_realistic_chrome(monkeypatch, realistic_chrome_db):
    """Mocks get_browser_path with a realistic database."""
    from chronicle_mcp import paths, connection

    def mock_fn(browser):
        if browser.lower() == "chrome":
            return realistic_chrome_db
        return None

    monkeypatch.setattr(paths, "get_browser_path", mock_fn)
    monkeypatch.setattr(connection, "get_browser_path", mock_fn)
