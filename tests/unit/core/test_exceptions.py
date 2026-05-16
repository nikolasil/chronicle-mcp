"""Tests for core exception classes.

This module tests all service layer exceptions to ensure proper
initialization, attributes, and message formatting.
"""

import pytest

from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    BrowserPathNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    InvalidDateRangeError,
    PermissionDeniedError,
    ServiceError,
    UnsupportedFormatError,
    ValidationError,
)


class TestServiceError:
    """Tests for ServiceError base class."""

    def test_basic_initialization(self):
        """Test basic error initialization."""
        error = ServiceError("Something went wrong")
        assert error.message == "Something went wrong"
        assert error.code == "SERVICE_ERROR"
        assert str(error) == "Something went wrong"

    def test_initialization_with_custom_code(self):
        """Test error with custom code."""
        error = ServiceError("Custom error", code="CUSTOM_CODE")
        assert error.message == "Custom error"
        assert error.code == "CUSTOM_CODE"

    def test_error_is_exception(self):
        """Test ServiceError is an Exception."""
        error = ServiceError("test")
        assert isinstance(error, Exception)


class TestValidationError:
    """Tests for ValidationError."""

    def test_basic_initialization(self):
        """Test basic validation error."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"
        assert error.field is None

    def test_with_field(self):
        """Test validation error with field."""
        error = ValidationError("Invalid browser", field="browser")
        assert error.message == "Invalid browser"
        assert error.field == "browser"

    def test_with_different_fields(self):
        """Test various field values."""
        test_cases = [
            ("browser", "browser"),
            ("limit", "limit"),
            ("query", "query"),
            ("date_range", "date_range"),
        ]
        for field_name, expected in test_cases:
            error = ValidationError("Error", field=field_name)
            assert error.field == expected


class TestBrowserNotFoundError:
    """Tests for BrowserNotFoundError."""

    def test_basic_initialization(self):
        """Test browser not found error."""
        error = BrowserNotFoundError("chrome")
        assert error.browser == "chrome"
        assert "chrome" in error.message
        assert error.code == "BROWSER_NOT_FOUND"

    def test_different_browsers(self):
        """Test with different browser names."""
        browsers = ["chrome", "firefox", "edge", "safari", "brave"]
        for browser in browsers:
            error = BrowserNotFoundError(browser)
            assert error.browser == browser
            assert browser in error.message

    def test_error_message_format(self):
        """Test error message contains browser name."""
        error = BrowserNotFoundError("test_browser")
        assert error.message == "Could not find test_browser history"


class TestBrowserPathNotFoundError:
    """Tests for BrowserPathNotFoundError."""

    def test_basic_initialization(self):
        """Test path not found error."""
        error = BrowserPathNotFoundError("chrome", "/path/to/history")
        assert error.browser == "chrome"
        assert error.path == "/path/to/history"
        assert "chrome" in error.message
        assert "/path/to/history" in error.message
        assert error.code == "PATH_NOT_FOUND"

    def test_different_paths(self):
        """Test with different paths."""
        test_cases = [
            ("firefox", "~/.mozilla/firefox/places.sqlite"),
            ("chrome", "C:\\Users\\user\\AppData\\Local\\Google\\Chrome"),
            ("edge", "/home/user/.config/microsoft-edge"),
        ]
        for browser, path in test_cases:
            error = BrowserPathNotFoundError(browser, path)
            assert error.browser == browser
            assert error.path == path


class TestDatabaseLockedError:
    """Tests for DatabaseLockedError."""

    def test_basic_initialization(self):
        """Test database locked error."""
        error = DatabaseLockedError("chrome")
        assert error.browser == "chrome"
        assert "chrome" in error.message
        assert "locked" in error.message.lower()
        assert error.code == "DATABASE_LOCKED"

    def test_different_browsers(self):
        """Test with different browsers."""
        browsers = ["chrome", "firefox", "edge"]
        for browser in browsers:
            error = DatabaseLockedError(browser)
            assert error.browser == browser
            assert browser in error.message


class TestPermissionDeniedError:
    """Tests for PermissionDeniedError."""

    def test_basic_initialization(self):
        """Test permission denied error."""
        error = PermissionDeniedError("chrome", "/path/to/db")
        assert error.browser == "chrome"
        assert error.path == "/path/to/db"
        assert "chrome" in error.message
        assert "/path/to/db" in error.message
        assert "Permission denied" in error.message
        assert error.code == "PERMISSION_DENIED"

    def test_error_message_format(self):
        """Test error message format."""
        error = PermissionDeniedError("firefox", "/home/user/.mozilla/places.sqlite")
        expected = (
            "Permission denied accessing firefox history at /home/user/.mozilla/places.sqlite"
        )
        assert error.message == expected


class TestDatabaseError:
    """Tests for DatabaseError."""

    def test_basic_initialization(self):
        """Test database error."""
        error = DatabaseError("Query failed")
        assert error.message == "Query failed"
        assert error.code == "DATABASE_ERROR"

    def test_with_complex_message(self):
        """Test with complex error message."""
        msg = "SQLite error: no such table: urls"
        error = DatabaseError(msg)
        assert error.message == msg


class TestUnsupportedFormatError:
    """Tests for UnsupportedFormatError."""

    def test_basic_initialization(self):
        """Test unsupported format error."""
        error = UnsupportedFormatError("xml", ["json", "csv", "markdown"])
        assert error.format_type == "xml"
        assert error.supported == ["json", "csv", "markdown"]
        assert "xml" in error.message
        assert "json" in error.message
        assert "csv" in error.message
        assert "markdown" in error.message
        assert error.code == "UNSUPPORTED_FORMAT"

    def test_single_supported_format(self):
        """Test with single supported format."""
        error = UnsupportedFormatError("yaml", ["json"])
        assert error.format_type == "yaml"
        assert error.supported == ["json"]
        assert "yaml" in error.message
        assert "json" in error.message

    def test_empty_supported_list(self):
        """Test with empty supported formats list."""
        error = UnsupportedFormatError("xml", [])
        assert error.format_type == "xml"
        assert error.supported == []


class TestInvalidDateRangeError:
    """Tests for InvalidDateRangeError."""

    def test_basic_initialization(self):
        """Test invalid date range error."""
        error = InvalidDateRangeError(
            "2024-12-31", "2024-01-01", "Start date must be before end date"
        )
        assert error.start_date == "2024-12-31"
        assert error.end_date == "2024-01-01"
        # The message contains the reason, dates are stored in attributes
        assert "Invalid date range" in error.message
        assert "Start date must be before end date" in error.message
        assert error.code == "INVALID_DATE_RANGE"

    def test_different_reasons(self):
        """Test with different reasons."""
        reasons = [
            "Start date must be before end date",
            "Invalid date format",
            "Date out of range",
        ]
        for reason in reasons:
            error = InvalidDateRangeError("2024-01-01", "2024-01-02", reason)
            assert error.start_date == "2024-01-01"
            assert error.end_date == "2024-01-02"
            assert reason in error.message


class TestExceptionInheritance:
    """Tests for exception inheritance hierarchy."""

    def test_all_inherit_from_service_error(self):
        """Test all exceptions inherit from ServiceError."""
        exceptions = [
            ValidationError("test"),
            BrowserNotFoundError("chrome"),
            BrowserPathNotFoundError("chrome", "/path"),
            DatabaseLockedError("chrome"),
            PermissionDeniedError("chrome", "/path"),
            DatabaseError("test"),
            UnsupportedFormatError("xml", ["json"]),
            InvalidDateRangeError("2024-01-01", "2024-01-02", "test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, ServiceError)

    def test_all_inherit_from_exception(self):
        """Test all exceptions inherit from Exception."""
        exceptions = [
            ServiceError("test"),
            ValidationError("test"),
            BrowserNotFoundError("chrome"),
            BrowserPathNotFoundError("chrome", "/path"),
            DatabaseLockedError("chrome"),
            PermissionDeniedError("chrome", "/path"),
            DatabaseError("test"),
            UnsupportedFormatError("xml", ["json"]),
            InvalidDateRangeError("2024-01-01", "2024-01-02", "test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, Exception)


class TestExceptionCatching:
    """Tests for exception catching behavior."""

    def test_catch_service_error_catches_all(self):
        """Test catching ServiceError catches all subclasses."""
        exceptions_to_test = [
            ValidationError("test"),
            BrowserNotFoundError("chrome"),
            DatabaseLockedError("chrome"),
            DatabaseError("test"),
        ]

        for exc in exceptions_to_test:
            caught = False
            try:
                raise exc
            except ServiceError as e:
                caught = True
                assert e is exc
            assert caught, f"Failed to catch {type(exc).__name__}"

    def test_catch_specific_exception(self):
        """Test catching specific exceptions."""
        try:
            raise ValidationError("test", field="browser")
        except ValidationError as e:
            assert e.field == "browser"
        except Exception:
            pytest.fail("Should not catch with generic Exception")

    def test_validation_error_not_caught_by_browser_not_found(self):
        """Test ValidationError is not caught by BrowserNotFoundError."""
        caught_by_validation = False
        try:
            raise ValidationError("test")
        except BrowserNotFoundError:
            pytest.fail("Should not catch ValidationError as BrowserNotFoundError")
        except ValidationError:
            caught_by_validation = True
        assert caught_by_validation
