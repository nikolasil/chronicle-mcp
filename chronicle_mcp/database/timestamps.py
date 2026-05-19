"""Timestamp formatters for different browser databases."""

from datetime import datetime, timedelta, timezone

BROWSER_EPOCHS = {
    "chrome": datetime(1601, 1, 1, tzinfo=timezone.utc),
    "firefox": datetime(1970, 1, 1, tzinfo=timezone.utc),
    "safari": datetime(2001, 1, 1, tzinfo=timezone.utc),
}


def format_timestamp(value: int, browser: str, unit: str = "microseconds") -> str:
    """
    Generic timestamp formatter for browser history databases.

    Args:
        value: Timestamp value from the browser database
        browser: Browser type ('chrome', 'firefox', 'safari')
        unit: Time unit ('microseconds' or 'seconds')

    Returns:
        ISO 8601 formatted datetime string
    """
    epoch = BROWSER_EPOCHS.get(browser.lower())
    if not epoch:
        return f"value={value}"

    try:
        if unit == "seconds":
            delta = timedelta(seconds=value)
        else:
            delta = timedelta(microseconds=value)
        dt = epoch + delta
        return dt.isoformat()
    except Exception:
        return f"value={value}"


def format_chrome_timestamp(microseconds: int) -> str:
    """
    Converts Chrome's microseconds-since-1601-01-01 to ISO 8601 string.

    Args:
        microseconds: Chrome's last_visit_time value

    Returns:
        ISO 8601 formatted datetime string
    """
    return format_timestamp(microseconds, "chrome", "microseconds")


def format_firefox_timestamp(microseconds: int) -> str:
    """
    Converts Firefox's microseconds-since-1970-01-01 to ISO 8601 string.

    Args:
        microseconds: Firefox's visit_date value

    Returns:
        ISO 8601 formatted datetime string
    """
    return format_timestamp(microseconds, "firefox", "microseconds")


def format_safari_timestamp(seconds: int) -> str:
    """
    Converts Apple's CFAbsoluteTime (seconds since 2001-01-01) to ISO 8601 string.

    Args:
        seconds: Safari's timestamp value

    Returns:
        ISO 8601 formatted datetime string
    """
    return format_timestamp(seconds, "safari", "seconds")
