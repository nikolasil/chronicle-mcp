"""Service layer exceptions for ChronicleMCP.

This module defines exceptions used by the core business logic layer.
These exceptions are caught by protocol adapters and converted to
protocol-specific error responses.
"""


class ServiceError(Exception):
    """Base exception for service layer errors."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or "SERVICE_ERROR"
        super().__init__(self.message)


class ValidationError(ServiceError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message, code="VALIDATION_ERROR")


class BrowserNotFoundError(ServiceError):
    """Raised when browser history is not found."""

    def __init__(self, browser: str):
        self.browser = browser
        super().__init__(message=f"Could not find {browser} history", code="BROWSER_NOT_FOUND")


class BrowserPathNotFoundError(ServiceError):
    """Raised when browser history path doesn't exist."""

    def __init__(self, browser: str, path: str):
        self.browser = browser
        self.path = path
        super().__init__(
            message=f"Could not find {browser} history at {path}", code="PATH_NOT_FOUND"
        )


class DatabaseLockedError(ServiceError):
    """Raised when database is locked (browser running)."""

    def __init__(self, browser: str):
        self.browser = browser
        super().__init__(
            message=f"Unable to access {browser} history database (locked)", code="DATABASE_LOCKED"
        )


class PermissionDeniedError(ServiceError):
    """Raised when permission is denied accessing history."""

    def __init__(self, browser: str, path: str):
        self.browser = browser
        self.path = path
        super().__init__(
            message=f"Permission denied accessing {browser} history at {path}",
            code="PERMISSION_DENIED",
        )


class DatabaseError(ServiceError):
    """Raised when database operation fails."""

    def __init__(self, message: str):
        super().__init__(message, code="DATABASE_ERROR")


class UnsupportedFormatError(ServiceError):
    """Raised when unsupported format is requested."""

    def __init__(self, format_type: str, supported: list[str]):
        self.format_type = format_type
        self.supported = supported
        super().__init__(
            message=f"Unsupported format '{format_type}'. Valid: {', '.join(supported)}",
            code="UNSUPPORTED_FORMAT",
        )


class InvalidDateRangeError(ServiceError):
    """Raised when date range is invalid."""

    def __init__(self, start_date: str, end_date: str, reason: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(message=f"Invalid date range: {reason}", code="INVALID_DATE_RANGE")
