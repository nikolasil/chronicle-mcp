"""Tests for core validation functions."""

import pytest

from chronicle_mcp.core.exceptions import (
    InvalidDateRangeError,
    ValidationError,
)
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_browsers_different,
    validate_date_range,
    validate_domain,
    validate_exclude_domains,
    validate_format_type,
    validate_fuzzy_threshold,
    validate_hours,
    validate_limit,
    validate_merge_strategy,
    validate_query,
    validate_search_options,
    validate_sort_by,
)


class TestValidateBrowser:
    """Tests for validate_browser function."""

    def test_valid_browser_lowercase(self):
        result = validate_browser("chrome")
        assert result == "chrome"

    def test_valid_browser_uppercase(self):
        result = validate_browser("CHROME")
        assert result == "chrome"

    def test_valid_browser_mixed_case(self):
        result = validate_browser("Chrome")
        assert result == "chrome"

    def test_all_valid_browsers(self):
        browsers = ["chrome", "edge", "firefox", "brave", "safari", "vivaldi", "opera"]
        for browser in browsers:
            result = validate_browser(browser)
            assert result == browser

    def test_invalid_browser(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_browser("invalid")
        assert "Invalid browser" in str(exc_info.value)
        assert exc_info.value.field == "browser"

    def test_empty_browser(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_browser("")
        assert "Browser cannot be empty" in str(exc_info.value)

    def test_none_browser(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_browser(None)  # type: ignore
        assert "Browser cannot be empty" in str(exc_info.value)


class TestValidateQuery:
    """Tests for validate_query function."""

    def test_valid_query(self):
        result = validate_query("test query")
        assert result == "test query"

    def test_query_with_whitespace(self):
        result = validate_query("  test query  ")
        assert result == "test query"

    def test_empty_query(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_query("")
        assert "Query cannot be empty" in str(exc_info.value)

    def test_whitespace_only_query(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_query("   ")
        assert "Query cannot be empty" in str(exc_info.value)

    def test_none_query(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_query(None)  # type: ignore
        assert "Query cannot be empty" in str(exc_info.value)


class TestValidateLimit:
    """Tests for validate_limit function."""

    def test_valid_limit(self):
        result = validate_limit(10, 1, 100)
        assert result == 10

    def test_limit_at_min(self):
        result = validate_limit(1, 1, 100)
        assert result == 1

    def test_limit_at_max(self):
        result = validate_limit(100, 1, 100)
        assert result == 100

    def test_limit_below_min(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_limit(0, 1, 100)
        assert "must be between 1 and 100" in str(exc_info.value)

    def test_limit_above_max(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_limit(101, 1, 100)
        assert "must be between 1 and 100" in str(exc_info.value)

    def test_non_integer_limit(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_limit("10", 1, 100)
        assert "must be an integer" in str(exc_info.value)

    def test_custom_range(self):
        result = validate_limit(5, 1, 50)
        assert result == 5


class TestValidateHours:
    """Tests for validate_hours function."""

    def test_valid_hours(self):
        result = validate_hours(24)
        assert result == 24

    def test_hours_one(self):
        result = validate_hours(1)
        assert result == 1

    def test_hours_zero(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_hours(0)
        assert "Hours must be a positive integer" in str(exc_info.value)

    def test_negative_hours(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_hours(-1)
        assert "Hours must be a positive integer" in str(exc_info.value)

    def test_non_integer_hours(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_hours(24.5)
        assert "Hours must be an integer" in str(exc_info.value)


class TestValidateFormatType:
    """Tests for validate_format_type function."""

    def test_valid_markdown(self):
        result = validate_format_type("markdown")
        assert result == "markdown"

    def test_valid_json(self):
        result = validate_format_type("json")
        assert result == "json"

    def test_case_insensitive(self):
        result = validate_format_type("JSON")
        assert result == "json"

    def test_invalid_format(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_format_type("xml")
        assert "Invalid format_type" in str(exc_info.value)

    def test_export_csv_format(self):
        result = validate_format_type("csv", export=True)
        assert result == "csv"

    def test_export_invalid_format(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_format_type("xml", export=True)
        assert "Invalid format_type" in str(exc_info.value)


class TestValidateDomain:
    """Tests for validate_domain function."""

    def test_valid_domain(self):
        result = validate_domain("github.com")
        assert result == "github.com"

    def test_domain_with_whitespace(self):
        result = validate_domain("  github.com  ")
        assert result == "github.com"

    def test_empty_domain(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_domain("")
        assert "Domain cannot be empty" in str(exc_info.value)


class TestValidateDateRange:
    """Tests for validate_date_range function."""

    def test_valid_date_range(self):
        start, end = validate_date_range("2024-01-01", "2024-12-31")
        assert start == "2024-01-01"
        assert end == "2024-12-31"

    def test_start_after_end(self):
        with pytest.raises(InvalidDateRangeError) as exc_info:
            validate_date_range("2024-12-31", "2024-01-01")
        assert "Start date must be before" in str(exc_info.value)

    def test_invalid_date_format(self):
        with pytest.raises(InvalidDateRangeError) as exc_info:
            validate_date_range("invalid", "2024-12-31")
        assert "Invalid date format" in str(exc_info.value)

    def test_empty_start_date(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_date_range("", "2024-12-31")
        assert "Start date cannot be empty" in str(exc_info.value)


class TestValidateSortBy:
    """Tests for validate_sort_by function."""

    def test_valid_date(self):
        result = validate_sort_by("date")
        assert result == "date"

    def test_valid_visit_count(self):
        result = validate_sort_by("visit_count")
        assert result == "visit_count"

    def test_valid_title(self):
        result = validate_sort_by("title")
        assert result == "title"

    def test_invalid_sort(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_sort_by("invalid")
        assert "Invalid sort_by" in str(exc_info.value)


class TestValidateFuzzyThreshold:
    """Tests for validate_fuzzy_threshold function."""

    def test_valid_threshold(self):
        result = validate_fuzzy_threshold(0.6)
        assert result == 0.6

    def test_threshold_zero(self):
        result = validate_fuzzy_threshold(0.0)
        assert result == 0.0

    def test_threshold_one(self):
        result = validate_fuzzy_threshold(1.0)
        assert result == 1.0

    def test_threshold_below_zero(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_fuzzy_threshold(-0.1)
        assert "must be between 0.0 and 1.0" in str(exc_info.value)

    def test_threshold_above_one(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_fuzzy_threshold(1.1)
        assert "must be between 0.0 and 1.0" in str(exc_info.value)


class TestValidateSearchOptions:
    """Tests for validate_search_options function."""

    def test_neither_enabled(self):
        validate_search_options(False, False)  # Should not raise

    def test_only_regex(self):
        validate_search_options(True, False)  # Should not raise

    def test_only_fuzzy(self):
        validate_search_options(False, True)  # Should not raise

    def test_both_enabled(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_search_options(True, True)
        assert "Cannot use both regex and fuzzy" in str(exc_info.value)


class TestValidateMergeStrategy:
    """Tests for validate_merge_strategy function."""

    def test_valid_latest(self):
        result = validate_merge_strategy("latest")
        assert result == "latest"

    def test_valid_combine(self):
        result = validate_merge_strategy("combine")
        assert result == "combine"

    def test_valid_dedupe(self):
        result = validate_merge_strategy("dedupe")
        assert result == "dedupe"

    def test_invalid_strategy(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_merge_strategy("invalid")
        assert "Invalid merge_strategy" in str(exc_info.value)


class TestValidateBrowsersDifferent:
    """Tests for validate_browsers_different function."""

    def test_different_browsers(self):
        validate_browsers_different("chrome", "firefox")  # Should not raise

    def test_same_browser(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_browsers_different("chrome", "chrome")
        assert "must be different" in str(exc_info.value)

    def test_same_browser_different_case(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_browsers_different("chrome", "CHROME")
        assert "must be different" in str(exc_info.value)


class TestValidateExcludeDomains:
    """Tests for validate_exclude_domains function."""

    def test_valid_list(self):
        result = validate_exclude_domains(["example.com", "test.com"])
        assert result == ["example.com", "test.com"]

    def test_empty_list(self):
        result = validate_exclude_domains([])
        assert result == []

    def test_none(self):
        result = validate_exclude_domains(None)
        assert result == []

    def test_with_whitespace(self):
        result = validate_exclude_domains(["  example.com  ", "test.com"])
        assert result == ["example.com", "test.com"]

    def test_filters_empty_strings(self):
        result = validate_exclude_domains(["example.com", "", "test.com"])
        assert result == ["example.com", "test.com"]


class TestValidateFormatTypeExport:
    """Tests for validate_format_type with export parameter."""

    def test_valid_csv_export(self):
        from chronicle_mcp.core.validation import validate_format_type

        result = validate_format_type("csv", export=True)
        assert result == "csv"

    def test_valid_json_export(self):
        from chronicle_mcp.core.validation import validate_format_type

        result = validate_format_type("json", export=True)
        assert result == "json"

    def test_invalid_export_format(self):
        from chronicle_mcp.core.validation import ValidationError, validate_format_type

        with pytest.raises(ValidationError) as exc_info:
            validate_format_type("xml", export=True)
        assert "Invalid format_type" in str(exc_info.value)
