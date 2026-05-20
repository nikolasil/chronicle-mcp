"""Property-based tests for validation functions using Hypothesis."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

pytestmark = pytest.mark.ci_excluded

from chronicle_mcp.core.exceptions import InvalidDateRangeError, ValidationError
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_date_range,
    validate_domain,
    validate_exclude_domains,
    validate_format_type,
    validate_fuzzy_threshold,
    validate_hours,
    validate_limit,
    validate_query,
    validate_sort_by,
)


class TestValidateBrowserProperty:
    """Property-based tests for validate_browser."""

    @given(
        browser=st.sampled_from(
            ["chrome", "firefox", "edge", "brave", "safari", "vivaldi", "opera"]
        )
    )
    @settings(max_examples=100)
    def test_valid_browser_returns_lowercase(self, browser):
        """Valid browser names should be returned as lowercase."""
        result = validate_browser(browser)
        assert result == browser.lower()

    @given(browser=st.text(min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_invalid_browser_raises(self, browser):
        """Invalid browser names should raise ValidationError."""
        invalid_browsers = ["invalid", "unknown", "xyz", "browser123", "saf"]
        if browser.lower() not in invalid_browsers:
            pytest.skip("Browser might be valid")
        with pytest.raises(ValidationError):
            validate_browser(browser)


class TestValidateQueryProperty:
    """Property-based tests for validate_query."""

    @given(query=st.text(min_size=1, max_size=1000).filter(lambda x: x.strip()))
    @settings(max_examples=100)
    def test_valid_query_accepted(self, query):
        """Any non-empty query should be accepted after stripping."""
        result = validate_query(query)
        assert result == query.strip()

    @given(query=st.text())
    @settings(max_examples=100)
    def test_empty_or_whitespace_query_raises(self, query):
        """Empty or whitespace-only queries should raise ValidationError."""
        if not query or not query.strip():
            with pytest.raises(ValidationError):
                validate_query(query)


class TestValidateLimitProperty:
    """Property-based tests for validate_limit."""

    @given(value=st.integers(min_value=1, max_value=100))
    @settings(max_examples=100)
    def test_valid_limit_accepted(self, value):
        """Valid limits within range should be accepted."""
        result = validate_limit(value, 1, 100)
        assert result == value

    @given(value=st.integers())
    @settings(max_examples=100)
    def test_out_of_range_limit_raises(self, value):
        """Limits outside range should raise ValidationError."""
        if value < 1 or value > 100:
            with pytest.raises(ValidationError):
                validate_limit(value, 1, 100)

    @given(min_val=st.integers(min_value=0, max_value=99))
    @settings(max_examples=50)
    def test_custom_range_respected(self, min_val):
        """Custom min/max ranges should be respected."""
        max_val = min_val + 100
        valid_value = min_val + 1
        result = validate_limit(valid_value, min_val, max_val)
        assert result == valid_value


class TestValidateHoursProperty:
    """Property-based tests for validate_hours."""

    @given(hours=st.integers(min_value=1, max_value=8760))
    @settings(max_examples=100)
    def test_valid_hours_accepted(self, hours):
        """Positive integer hours should be accepted."""
        result = validate_hours(hours)
        assert result == hours

    @given(hours=st.integers(max_value=0))
    @settings(max_examples=100)
    def test_non_positive_hours_raises(self, hours):
        """Zero or negative hours should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_hours(hours)


class TestValidateFormatTypeProperty:
    """Property-based tests for validate_format_type."""

    @given(format_type=st.sampled_from(["markdown", "json", "JSON", "Markdown"]))
    @settings(max_examples=10)
    def test_valid_formats_accepted(self, format_type):
        """Valid format types should be accepted and normalized."""
        result = validate_format_type(format_type)
        assert result in ["markdown", "json"]

    @given(
        format_type=st.text(min_size=1, max_size=20).filter(
            lambda x: x.lower() not in ["markdown", "json"]
        )
    )
    @settings(max_examples=100)
    def test_invalid_format_raises(self, format_type):
        """Invalid format types should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_format_type(format_type)


class TestValidateDomainProperty:
    """Property-based tests for validate_domain."""

    @given(domain=st.text(min_size=1, max_size=500).filter(lambda x: x.strip()))
    @settings(max_examples=100)
    def test_valid_domain_normalized(self, domain):
        """Valid domains should be stripped of whitespace."""
        result = validate_domain(domain)
        assert result == domain.strip()


class TestValidateSortByProperty:
    """Property-based tests for validate_sort_by."""

    @given(sort_by=st.sampled_from(["date", "visit_count", "title"]))
    @settings(max_examples=10)
    def test_valid_sort_by_accepted(self, sort_by):
        """Valid sort_by values should be accepted."""
        result = validate_sort_by(sort_by)
        assert result == sort_by


class TestValidateFuzzyThresholdProperty:
    """Property-based tests for validate_fuzzy_threshold."""

    @given(threshold=st.floats(min_value=0.0, max_value=1.0, allow_nan=False))
    @settings(max_examples=100)
    def test_valid_threshold_accepted(self, threshold):
        """Valid thresholds between 0.0 and 1.0 should be accepted."""
        result = validate_fuzzy_threshold(threshold)
        assert result == threshold

    @given(threshold=st.floats().filter(lambda x: x < 0.0 or x > 1.0))
    @settings(max_examples=100)
    def test_out_of_range_threshold_raises(self, threshold):
        """Thresholds outside 0.0-1.0 range should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_fuzzy_threshold(threshold)


class TestValidateExcludeDomainsProperty:
    """Property-based tests for validate_exclude_domains."""

    @given(
        domains=st.lists(
            st.sampled_from(["example.com", "test.org", "domain.net", "site.io", "app.dev"]),
            min_size=1,
            max_size=20,
        )
    )
    @settings(max_examples=50)
    def test_valid_domain_list(self, domains):
        """Valid domain lists should be processed."""
        result = validate_exclude_domains(domains)
        assert isinstance(result, list)
        assert len(result) <= len(domains)

    @given(
        domains=st.lists(
            st.sampled_from(["example.com", "test.org", "", "domain.net", "  "]),
            min_size=1,
            max_size=20,
        )
    )
    @settings(max_examples=50)
    def test_empty_strings_filtered(self, domains):
        """Empty strings in domain lists should be filtered."""
        result = validate_exclude_domains(domains)
        assert "" not in result
        assert "  " not in result


class TestValidateDateRangeProperty:
    """Property-based tests for validate_date_range."""

    @given(year=st.integers(min_value=2000, max_value=2099))
    @settings(max_examples=50)
    def test_valid_date_format_accepted(self, year):
        """Valid ISO date formats should be accepted."""
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        start_result, end_result = validate_date_range(start, end)
        assert start_result == start
        assert end_result == end

    @given(
        year1=st.integers(min_value=2000, max_value=2099),
        year2=st.integers(min_value=2000, max_value=2099),
    )
    @settings(max_examples=100)
    def test_start_before_end_validation(self, year1, year2):
        """Start date must be before end date."""
        start_date = f"{year1}-06-15"
        end_date = f"{year2}-06-15"
        if year1 <= year2:
            start_result, end_result = validate_date_range(start_date, end_date)
            assert start_result == start_date
            assert end_result == end_date
        else:
            with pytest.raises(InvalidDateRangeError):
                validate_date_range(start_date, end_date)
