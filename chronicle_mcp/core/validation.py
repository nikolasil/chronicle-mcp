"""Input validation functions for ChronicleMCP service layer.

This module provides validation functions for all service inputs.
Validation functions raise ValidationError on failure.
"""

from chronicle_mcp.core.exceptions import InvalidDateRangeError, ValidationError

VALID_BROWSERS = ["chrome", "edge", "firefox", "brave", "safari", "vivaldi", "opera"]

VALID_FORMATS = ["markdown", "json"]
VALID_EXPORT_FORMATS = ["csv", "json"]
VALID_SORT_ORDERS = ["date", "visit_count", "title"]
VALID_MERGE_STRATEGIES = ["latest", "combine", "dedupe"]


def validate_browser(browser: str) -> str:
    """Validate browser name and return lowercase version.

    Args:
        browser: Browser name to validate

    Returns:
        Lowercase browser name

    Raises:
        ValidationError: If browser is not supported
    """
    if not browser or not isinstance(browser, str):
        raise ValidationError("Browser cannot be empty", field="browser")

    browser_lower = browser.lower()
    if browser_lower not in VALID_BROWSERS:
        raise ValidationError(
            f"Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}",
            field="browser",
        )

    return browser_lower


def validate_query(query: str | None, field_name: str = "query") -> str:
    """Validate search query string.

    Args:
        query: Query string to validate
        field_name: Name of the field for error messages

    Returns:
        Stripped query string

    Raises:
        ValidationError: If query is empty or invalid
    """
    if not query or not isinstance(query, str) or not query.strip():
        raise ValidationError(f"{field_name.capitalize()} cannot be empty", field=field_name)

    return query.strip()


def validate_limit(
    limit: int, min_val: int = 1, max_val: int = 100, field_name: str = "limit"
) -> int:
    """Validate limit parameter.

    Args:
        limit: Limit value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field for error messages

    Returns:
        Validated limit value

    Raises:
        ValidationError: If limit is out of range
    """
    if not isinstance(limit, int):
        raise ValidationError(f"{field_name.capitalize()} must be an integer", field=field_name)

    if limit < min_val or limit > max_val:
        raise ValidationError(
            f"{field_name.capitalize()} must be between {min_val} and {max_val}", field=field_name
        )

    return limit


def validate_hours(hours: int) -> int:
    """Validate hours parameter for recent history.

    Args:
        hours: Number of hours to look back

    Returns:
        Validated hours value

    Raises:
        ValidationError: If hours is invalid
    """
    if not isinstance(hours, int):
        raise ValidationError("Hours must be an integer", field="hours")

    if hours < 1:
        raise ValidationError("Hours must be a positive integer", field="hours")

    return hours


def validate_format_type(format_type: str, export: bool = False) -> str:
    """Validate output format type.

    Args:
        format_type: Format type to validate
        export: Whether this is for export (allows csv)

    Returns:
        Lowercase format type

    Raises:
        ValidationError: If format is not supported
    """
    if not format_type or not isinstance(format_type, str):
        raise ValidationError("Format type cannot be empty", field="format_type")

    format_lower = format_type.lower()
    valid_formats = VALID_EXPORT_FORMATS if export else VALID_FORMATS

    if format_lower not in valid_formats:
        valid_list = ", ".join(valid_formats)
        raise ValidationError(
            f"Invalid format_type '{format_type}'. Valid options: {valid_list}", field="format_type"
        )

    return format_lower


def validate_domain(domain: str) -> str:
    """Validate domain string.

    Args:
        domain: Domain to validate

    Returns:
        Stripped domain string

    Raises:
        ValidationError: If domain is empty
    """
    if not domain or not isinstance(domain, str) or not domain.strip():
        raise ValidationError("Domain cannot be empty", field="domain")

    return domain.strip()


def validate_date_range(start_date: str, end_date: str) -> tuple[str, str]:
    """Validate date range strings.

    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)

    Returns:
        Tuple of (start_date, end_date)

    Raises:
        ValidationError: If dates are empty
        InvalidDateRangeError: If date range is invalid
    """
    if not start_date or not isinstance(start_date, str):
        raise ValidationError("Start date cannot be empty", field="start_date")

    if not end_date or not isinstance(end_date, str):
        raise ValidationError("End date cannot be empty", field="end_date")

    # Basic ISO format validation
    try:
        from datetime import datetime

        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

        if start_dt > end_dt:
            raise InvalidDateRangeError(
                start_date, end_date, "Start date must be before or equal to end date"
            )
    except ValueError as e:
        raise InvalidDateRangeError(start_date, end_date, f"Invalid date format: {e}")

    return start_date.strip(), end_date.strip()


def validate_sort_by(sort_by: str) -> str:
    """Validate sort order parameter.

    Args:
        sort_by: Sort order to validate

    Returns:
        Lowercase sort order

    Raises:
        ValidationError: If sort order is invalid
    """
    if not sort_by or not isinstance(sort_by, str):
        raise ValidationError("Sort order cannot be empty", field="sort_by")

    sort_lower = sort_by.lower()
    if sort_lower not in VALID_SORT_ORDERS:
        raise ValidationError(
            f"Invalid sort_by '{sort_by}'. Valid options: {', '.join(VALID_SORT_ORDERS)}",
            field="sort_by",
        )

    return sort_lower


def validate_fuzzy_threshold(threshold: float) -> float:
    """Validate fuzzy matching threshold.

    Args:
        threshold: Threshold value (0.0-1.0)

    Returns:
        Validated threshold value

    Raises:
        ValidationError: If threshold is out of range
    """
    if not isinstance(threshold, (int, float)):
        raise ValidationError("Fuzzy threshold must be a number", field="fuzzy_threshold")

    if not 0.0 <= threshold <= 1.0:
        raise ValidationError(
            "Fuzzy threshold must be between 0.0 and 1.0", field="fuzzy_threshold"
        )

    return float(threshold)


def validate_search_options(use_regex: bool, use_fuzzy: bool) -> None:
    """Validate that regex and fuzzy are not both enabled.

    Args:
        use_regex: Whether regex matching is enabled
        use_fuzzy: Whether fuzzy matching is enabled

    Raises:
        ValidationError: If both are enabled
    """
    if use_regex and use_fuzzy:
        raise ValidationError(
            "Cannot use both regex and fuzzy matching simultaneously", field="search_options"
        )


def validate_merge_strategy(strategy: str) -> str:
    """Validate merge strategy for sync operations.

    Args:
        strategy: Merge strategy to validate

    Returns:
        Lowercase strategy name

    Raises:
        ValidationError: If strategy is invalid
    """
    if not strategy or not isinstance(strategy, str):
        raise ValidationError("Merge strategy cannot be empty", field="merge_strategy")

    strategy_lower = strategy.lower()
    if strategy_lower not in VALID_MERGE_STRATEGIES:
        raise ValidationError(
            f"Invalid merge_strategy '{strategy}'. Valid options: {', '.join(VALID_MERGE_STRATEGIES)}",
            field="merge_strategy",
        )

    return strategy_lower


def validate_browsers_different(source: str, target: str) -> None:
    """Validate that source and target browsers are different.

    Args:
        source: Source browser name
        target: Target browser name

    Raises:
        ValidationError: If browsers are the same
    """
    if source.lower() == target.lower():
        raise ValidationError("Source and target browsers must be different", field="browsers")


def validate_exclude_domains(exclude_domains: list[str] | None) -> list[str]:
    """Validate and clean exclude domains list.

    Args:
        exclude_domains: List of domains to exclude

    Returns:
        Cleaned list of domains
    """
    if not exclude_domains:
        return []

    if not isinstance(exclude_domains, list):
        raise ValidationError("exclude_domains must be a list", field="exclude_domains")

    return [str(d).strip() for d in exclude_domains if d and str(d).strip()]
