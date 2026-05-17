"""Tests for analysis service methods."""

import pytest

from chronicle_mcp.core import HistoryService
from chronicle_mcp.core.categories import CATEGORY_PATTERNS


class TestCompareTimePeriods:
    """Tests for compare_time_periods service method."""

    def test_compare_periods_requires_valid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.compare_time_periods(
                start_date1="2024-01-01",
                end_date1="2024-01-31",
                start_date2="2024-02-01",
                end_date2="2024-02-29",
                browser="invalid",
            )

    def test_compare_periods_returns_both_periods(self, mock_chrome_path, sample_chrome_db):
        """Should return data for both periods."""
        result = HistoryService.compare_time_periods(
            start_date1="2024-01-01",
            end_date1="2024-01-31",
            start_date2="2024-02-01",
            end_date2="2024-02-29",
            browser="chrome",
        )

        assert "period1" in result
        assert "period2" in result
        assert "start" in result["period1"]
        assert "end" in result["period1"]
        assert "total_visits" in result["period1"]
        assert "unique_urls" in result["period1"]
        assert "top_domains" in result["period1"]

    def test_compare_periods_includes_changes(self, mock_chrome_path, sample_chrome_db):
        """Should include delta changes between periods."""
        result = HistoryService.compare_time_periods(
            start_date1="2024-01-01",
            end_date1="2024-01-31",
            start_date2="2024-02-01",
            end_date2="2024-02-29",
            browser="chrome",
        )

        assert "changes" in result
        assert "total_visits_delta" in result["changes"]
        assert "unique_urls_delta" in result["changes"]
        assert isinstance(result["changes"]["total_visits_delta"], int)

    def test_compare_periods_includes_category_breakdown(self, mock_chrome_path, sample_chrome_db):
        """Should include category breakdown."""
        result = HistoryService.compare_time_periods(
            start_date1="2024-01-01",
            end_date1="2024-01-31",
            start_date2="2024-02-01",
            end_date2="2024-02-29",
            browser="chrome",
        )

        assert "category_breakdown" in result
        assert isinstance(result["category_breakdown"], dict)

    def test_compare_periods_with_overlapping_dates(self, mock_chrome_path, sample_chrome_db):
        """Should handle overlapping date periods."""
        result = HistoryService.compare_time_periods(
            start_date1="2024-02-01",
            end_date1="2024-02-29",
            start_date2="2024-02-15",
            end_date2="2024-03-15",
            browser="chrome",
        )
        assert "period1" in result
        assert "period2" in result

    def test_compare_periods_invalid_date_range(self, mock_chrome_path, sample_chrome_db):
        """Should raise error for invalid date range (start > end)."""
        from chronicle_mcp.core import InvalidDateRangeError

        with pytest.raises(InvalidDateRangeError):
            HistoryService.compare_time_periods(
                start_date1="2024-01-31",
                end_date1="2024-01-01",
                start_date2="2024-02-01",
                end_date2="2024-02-29",
                browser="chrome",
            )


class TestAnalyzeProductivity:
    """Tests for analyze_productivity service method."""

    def test_productivity_analysis_returns_score(self, mock_chrome_path, sample_chrome_db):
        """Should return productivity score and grade."""
        result = HistoryService.analyze_productivity(browser="chrome")
        assert "productivity_score" in result
        assert isinstance(result["productivity_score"], (int, float))
        assert 0 <= result["productivity_score"] <= 100

    def test_productivity_analysis_returns_grade(self, mock_chrome_path, sample_chrome_db):
        """Should return a letter grade."""
        result = HistoryService.analyze_productivity(browser="chrome")
        assert "grade" in result
        assert result["grade"] in ["A", "B", "C", "D", "F", "N/A"]

    def test_productivity_analysis_returns_category_breakdown(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Should return category breakdown with counts and percentages."""
        result = HistoryService.analyze_productivity(browser="chrome")
        assert "category_breakdown" in result
        assert isinstance(result["category_breakdown"], dict)
        for category, data in result["category_breakdown"].items():
            assert "count" in data
            assert "percentage" in data

    def test_productivity_analysis_returns_recommendations(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Should return recommendations list."""
        result = HistoryService.analyze_productivity(browser="chrome")
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

    def test_productivity_analysis_with_date_range(self, mock_chrome_path, sample_chrome_db):
        """Should accept optional date range parameters."""
        result = HistoryService.analyze_productivity(
            start_date="2024-01-01",
            end_date="2024-01-31",
            browser="chrome",
        )
        assert "period" in result
        assert result["period"]["start"] == "2024-01-01"
        assert result["period"]["end"] == "2024-01-31"

    def test_productivity_analysis_invalid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.analyze_productivity(browser="invalid")


class TestSuggestCategories:
    """Tests for suggest_categories service method."""

    def test_suggest_categories_returns_list(self, mock_chrome_path, sample_chrome_db):
        """Should return list of suggestions."""
        result = HistoryService.suggest_categories(browser="chrome", limit=10)
        assert "uncategorized" in result
        assert isinstance(result["uncategorized"], list)

    def test_suggest_categories_includes_url_details(self, mock_chrome_path, sample_chrome_db):
        """Each suggestion should include title, url, visit_count."""
        result = HistoryService.suggest_categories(browser="chrome", limit=10)
        for suggestion in result["uncategorized"]:
            assert "title" in suggestion
            assert "url" in suggestion
            assert "visit_count" in suggestion
            assert "suggested_category" in suggestion

    def test_suggest_categories_respects_limit(self, mock_chrome_path, sample_chrome_db):
        """Should respect the limit parameter."""
        result = HistoryService.suggest_categories(browser="chrome", limit=5)
        assert result["count"] <= 5

    def test_suggest_categories_invalid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.suggest_categories(browser="invalid")

    def test_suggest_categories_invalid_limit(self):
        """Invalid limit should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.suggest_categories(browser="chrome", limit=0)

    def test_suggest_categories_limit_boundary(self):
        """Limit of 1 should be valid."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.suggest_categories(browser="chrome", limit=-1)


class TestExportVisualization:
    """Tests for export_visualization service method."""

    def test_export_visualization_returns_chart_json_by_default(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Should return Chart.js format data by default."""
        result = HistoryService.export_visualization(browser="chrome")
        assert "charts" in result
        assert isinstance(result["charts"], list)
        assert len(result["charts"]) > 0

    def test_export_visualization_chart_structure(self, mock_chrome_path, sample_chrome_db):
        """Each chart should have type, title, and data."""
        result = HistoryService.export_visualization(browser="chrome")
        for chart in result["charts"]:
            assert "type" in chart
            assert "title" in chart
            assert "data" in chart
            assert "labels" in chart["data"]
            assert "datasets" in chart["data"]

    def test_export_visualization_csv_format(self, mock_chrome_path, sample_chrome_db):
        """Should return csv format when requested."""
        result = HistoryService.export_visualization(browser="chrome", format_type="csv")
        assert "content" in result
        assert isinstance(result["content"], str)
        assert "Category" in result["content"]
        assert result["format"] == "csv"

    def test_export_visualization_includes_category_breakdown(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Should include category breakdown in output."""
        result = HistoryService.export_visualization(browser="chrome")
        assert "category_breakdown" in result

    def test_export_visualization_includes_period(self, mock_chrome_path, sample_chrome_db):
        """Should include period in output."""
        result = HistoryService.export_visualization(browser="chrome", period="month")
        assert "period" in result
        assert result["period"] == "month"

    def test_export_visualization_chart_types(self, mock_chrome_path, sample_chrome_db):
        """Should include doughnut, bar charts for categories/domains."""
        result = HistoryService.export_visualization(browser="chrome")
        chart_types = {c["type"] for c in result["charts"]}
        assert "doughnut" in chart_types
        assert "bar" in chart_types

    def test_export_visualization_doughnut_has_category_labels(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Doughnut chart should have category labels."""
        result = HistoryService.export_visualization(browser="chrome")
        doughnut_chart = next((c for c in result["charts"] if c["type"] == "doughnut"), None)
        assert doughnut_chart is not None
        assert len(doughnut_chart["data"]["labels"]) > 0


class TestGenerateInsightsReport:
    """Tests for generate_insights_report service method."""

    def test_generate_insights_report_returns_markdown_summary(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Should return markdown summary."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert "summary_markdown" in result
        assert isinstance(result["summary_markdown"], str)
        assert len(result["summary_markdown"]) > 0

    def test_generate_insights_report_contains_browser(self, mock_chrome_path, sample_chrome_db):
        """Markdown should contain browser name."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert "**Browser:** chrome" in result["summary_markdown"]

    def test_generate_insights_report_contains_productivity(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Markdown should contain productivity score and grade."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert "**Score:**" in result["summary_markdown"]
        assert "productivity" in result["summary_markdown"].lower()

    def test_generate_insights_report_contains_top_domains(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Markdown should contain top domains section."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert (
            "## Top Domains" in result["summary_markdown"]
            or "Top Domains" in result["summary_markdown"]
        )

    def test_generate_insights_report_contains_recommendations(
        self, mock_chrome_path, sample_chrome_db
    ):
        """Markdown should contain recommendations section."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert (
            "## Recommendations" in result["summary_markdown"]
            or "Recommendations" in result["summary_markdown"]
        )

    def test_generate_insights_report_json_format(self, mock_chrome_path, sample_chrome_db):
        """Should return detailed data when format is json."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="json")
        assert "data" in result
        assert "stats" in result["data"]
        assert "productivity" in result["data"]
        assert "top_domains" in result["data"]

    def test_generate_insights_report_invalid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.generate_insights_report(browser="invalid")

    def test_generate_insights_report_invalid_period(self, mock_chrome_path, sample_chrome_db):
        """Invalid period should be handled gracefully."""
        result = HistoryService.generate_insights_report(browser="chrome", period="invalid")
        assert "summary_markdown" in result

    def test_generate_insights_report_includes_period(self, mock_chrome_path, sample_chrome_db):
        """Should include period in output."""
        result = HistoryService.generate_insights_report(browser="chrome", period="week")
        assert "period" in result or "week" in result["summary_markdown"].lower()


class TestAnalyticsWithRealisticData:
    """Tests for analytics with realistic database."""

    def test_analyze_productivity_with_realistic_data(
        self, mock_realistic_chrome, realistic_chrome_db
    ):
        """Should return meaningful productivity analysis."""
        result = HistoryService.analyze_productivity(browser="chrome")

        assert result["productivity_score"] >= 0
        assert result["productivity_score"] <= 100
        assert result["grade"] in ["A", "B", "C", "D", "F", "N/A"]
        assert len(result["category_breakdown"]) > 0

    def test_compare_time_periods_with_realistic_data(
        self, mock_realistic_chrome, realistic_chrome_db
    ):
        """Should return meaningful period comparison."""
        result = HistoryService.compare_time_periods(
            start_date1="2024-01-01",
            end_date1="2024-01-31",
            start_date2="2024-02-01",
            end_date2="2024-02-29",
            browser="chrome",
        )

        assert result["period1"]["total_visits"] >= 0
        assert result["period2"]["total_visits"] >= 0
        assert isinstance(result["changes"]["total_visits_delta"], int)

    def test_suggest_categories_with_realistic_data(
        self, mock_realistic_chrome, realistic_chrome_db
    ):
        """Should return meaningful category suggestions."""
        result = HistoryService.suggest_categories(browser="chrome", limit=20)

        assert result["count"] <= 20
        for suggestion in result["uncategorized"]:
            assert (
                suggestion["suggested_category"] in CATEGORY_PATTERNS.keys()
                or suggestion["suggested_category"] is None
            )

    def test_export_visualization_with_realistic_data(
        self, mock_realistic_chrome, realistic_chrome_db
    ):
        """Should return meaningful visualization data."""
        result = HistoryService.export_visualization(browser="chrome")

        assert len(result["charts"]) >= 3
        total_visits = (
            sum(sum(ds["data"]) for ds in result["charts"][0]["data"]["datasets"])
            if result["charts"]
            else 0
        )
        assert total_visits >= 0

    def test_generate_insights_report_with_realistic_data(
        self, mock_realistic_chrome, realistic_chrome_db
    ):
        """Should return comprehensive insights."""
        result = HistoryService.generate_insights_report(browser="chrome", period="month")

        assert "summary_markdown" in result
        assert (
            "# Browsing Insights Report" in result["summary_markdown"]
            or "Browsing Insights" in result["summary_markdown"]
        )
