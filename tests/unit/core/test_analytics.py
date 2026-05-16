"""Tests for analysis service methods."""

import pytest

from chronicle_mcp.core import HistoryService


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


class TestAnalyzeProductivity:
    """Tests for analyze_productivity service method."""

    def test_productivity_analysis_returns_score(self, mock_chrome_path, sample_chrome_db):
        """Should return productivity score and grade."""
        result = HistoryService.analyze_productivity(browser="chrome")
        assert "productivity_score" in result
        assert "grade" in result
        assert "category_breakdown" in result

    def test_productivity_analysis_invalid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.analyze_productivity(browser="invalid")


class TestSuggestCategories:
    """Tests for suggest_categories service method."""

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


class TestExportVisualization:
    """Tests for export_visualization service method."""

    def test_export_visualization_returns_data(self, mock_chrome_path, sample_chrome_db):
        """Should return visualization data."""
        result = HistoryService.export_visualization(browser="chrome")
        assert "category_breakdown" in result
        assert "period" in result

    def test_export_visualization_csv_format(self, mock_chrome_path, sample_chrome_db):
        """Should return csv format when requested."""
        result = HistoryService.export_visualization(browser="chrome", format_type="csv")
        assert "content" in result
        assert result["format"] == "csv"


class TestGenerateInsightsReport:
    """Tests for generate_insights_report service method."""

    def test_generate_insights_report_invalid_browser(self):
        """Invalid browser should raise error."""
        from chronicle_mcp.core import ValidationError

        with pytest.raises(ValidationError):
            HistoryService.generate_insights_report(browser="invalid")

    def test_generate_insights_report_returns_markdown(self, mock_chrome_path, sample_chrome_db):
        """Should return markdown summary."""
        result = HistoryService.generate_insights_report(browser="chrome", format_type="markdown")
        assert "summary_markdown" in result
