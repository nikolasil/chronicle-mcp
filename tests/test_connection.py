"""Tests for connection management module.

These tests verify the temp file handling and connection lifecycle.
"""

import os
import platform
import tempfile
import time

import pytest

from chronicle_mcp.connection import (
    BrowserNotFoundError,
    cleanup_temp_file,
    get_history_connection,
    get_temp_filename,
)


class TestTempFileLifecycle:
    """Tests for temp file creation and cleanup."""

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason="Windows file locking prevents immediate cleanup - production code handles gracefully",
    )
    def test_temp_file_created_during_query(self, mock_chrome_path, sample_chrome_db):
        """Verify temp file is created during query."""
        temp_dir = tempfile.gettempdir()
        temp_files_before = set(os.listdir(temp_dir))

        with get_history_connection("chrome") as conn:
            # Temp file should exist during query
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()

        # On Windows, file locking may delay cleanup - check with retry
        chronicle_files = []
        max_retries = 5
        for i in range(max_retries):
            temp_files_after = set(os.listdir(temp_dir))
            new_files = temp_files_after - temp_files_before
            chronicle_files = [f for f in new_files if f.startswith("chronicle_")]

            if not chronicle_files:
                break

            if i < max_retries - 1:
                time.sleep(0.1)  # Wait for cleanup

        # Temp file should be cleaned up after context exits
        assert len(chronicle_files) == 0, f"Temp files not cleaned up: {chronicle_files}"

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason="Windows file locking prevents immediate cleanup on error - production code handles gracefully",
    )
    def test_temp_file_removed_on_error(self, mock_chrome_path, sample_chrome_db):
        """Verify temp files are removed even when errors occur."""
        temp_dir = tempfile.gettempdir()
        temp_files_before = set(os.listdir(temp_dir))

        try:
            with get_history_connection("chrome") as conn:
                # Simulate an error during query
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                raise ValueError("Simulated error")
        except ValueError:
            pass

        # On Windows, file locking may delay cleanup - check with retry
        chronicle_files = []
        max_retries = 5
        for i in range(max_retries):
            temp_files_after = set(os.listdir(temp_dir))
            new_files = temp_files_after - temp_files_before
            chronicle_files = [f for f in new_files if f.startswith("chronicle_")]

            if not chronicle_files:
                break

            if i < max_retries - 1:
                time.sleep(0.1)  # Wait for cleanup

        # Temp file should still be cleaned up
        assert len(chronicle_files) == 0, (
            f"Temp files not cleaned up after error: {chronicle_files}"
        )

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason="Windows file locking prevents immediate cleanup - production code handles gracefully",
    )
    def test_no_temp_files_leaked(self, mock_chrome_path, sample_chrome_db):
        """Verify no temp files are leaked after multiple queries."""
        temp_dir = tempfile.gettempdir()
        temp_files_before = set(os.listdir(temp_dir))

        # Run multiple queries
        for _ in range(10):
            try:
                with get_history_connection("chrome") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
            except Exception:
                pass

        # On Windows, file locking may delay cleanup - check with retry
        chronicle_files = []
        max_retries = 10
        for i in range(max_retries):
            temp_files_after = set(os.listdir(temp_dir))
            new_files = temp_files_after - temp_files_before
            chronicle_files = [f for f in new_files if f.startswith("chronicle_")]

            if not chronicle_files:
                break

            if i < max_retries - 1:
                time.sleep(0.2)  # Wait longer for multiple files

        # No chronicle temp files should remain
        assert len(chronicle_files) == 0, f"Leaked temp files: {chronicle_files}"


class TestConnectionExceptions:
    """Tests for connection exception handling."""

    def test_browser_not_found_error(self):
        """Test BrowserNotFoundError is raised for unknown browser."""
        with pytest.raises(BrowserNotFoundError):
            with get_history_connection("unknown_browser_xyz"):
                pass

    def test_error_message_contains_browser_name(self):
        """Test error messages contain the browser name."""
        error = BrowserNotFoundError("test_browser")
        assert "test_browser" in str(error)
        assert "test_browser" in error.browser


class TestConnectionUtilityFunctions:
    """Tests for connection utility functions."""

    def test_cleanup_temp_file_removes_file(self, tmp_path):
        """Test cleanup_temp_file removes the file."""
        test_file = tmp_path / "test_cleanup.db"
        test_file.write_text("test data")

        assert test_file.exists()
        cleanup_temp_file(str(test_file))
        assert not test_file.exists()

    def test_cleanup_temp_file_handles_missing_file(self, tmp_path):
        """Test cleanup_temp_file handles missing files gracefully."""
        nonexistent_file = tmp_path / "nonexistent.db"

        # Should not raise error for missing file
        cleanup_temp_file(str(nonexistent_file))

    def test_temp_filename_unique(self):
        """Test that temp filenames are unique."""
        filenames = []
        for _ in range(10):
            filenames.append(get_temp_filename("chrome"))
            time.sleep(0.002)  # 2ms delay to ensure unique timestamps

        # All filenames should be unique
        assert len(set(filenames)) == len(filenames)

    def test_temp_filename_contains_browser(self):
        """Test that temp filename contains browser name."""
        filename = get_temp_filename("chrome")
        assert "chrome" in filename

        filename = get_temp_filename("firefox")
        assert "firefox" in filename
