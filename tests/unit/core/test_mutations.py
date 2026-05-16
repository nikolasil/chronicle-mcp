"""Mutation tests for services.py to verify code robustness."""

from unittest.mock import patch

from chronicle_mcp.core.events import EventType
from chronicle_mcp.core.realtime import get_subscription_manager


class TestDuplicateEntriesMutationSafety:
    """Tests to ensure duplicate detection logic survives code changes."""

    def test_find_duplicate_entries_threshold_exactly_0_9(self):
        """Threshold at exactly 0.9 should be accepted."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection', return_value=[]):
            result = HistoryService.find_duplicate_entries(
                "chrome",
                similarity_threshold=0.9,
                limit=10,
            )
        assert result["similarity_threshold"] == 0.9

    def test_find_duplicate_entries_threshold_boundary_values(self):
        """Test boundary threshold values 0.0 and 1.0."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection', return_value=[]):
            result = HistoryService.find_duplicate_entries(
                "chrome",
                similarity_threshold=0.0,
                limit=10,
            )
            assert result["similarity_threshold"] == 0.0

            result = HistoryService.find_duplicate_entries(
                "chrome",
                similarity_threshold=1.0,
                limit=10,
            )
            assert result["similarity_threshold"] == 1.0

    def test_find_duplicate_entries_empty_db_returns_empty(self):
        """Empty database should return empty results."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection', return_value=[]):
            result = HistoryService.find_duplicate_entries("chrome")
            assert result["total_entries_analyzed"] == 0
            assert result["duplicate_groups"] == []

    def test_delete_duplicates_all_strategies_accepted(self):
        """All keep_strategy values should be accepted."""
        from chronicle_mcp.core.services import HistoryService

        for strategy in ["most_visits", "most_recent", "first"]:
            with patch.object(HistoryService, 'find_duplicate_entries', return_value={
                "duplicate_groups": [],
            }):
                with patch.object(HistoryService, 'delete_history', return_value={"deleted": 0}):
                    result = HistoryService.delete_duplicates(
                        "chrome",
                        keep_strategy=strategy,
                        confirm=True,
                    )
                    assert result is not None


class TestSubscriptionMutationSafety:
    """Tests to ensure subscription logic survives code changes."""

    def test_subscribe_with_single_event_type(self):
        """Single event type subscription should work."""
        from chronicle_mcp.core.services import HistoryService

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        result = HistoryService.subscribe_history_changes(
            browser="chrome",
            event_types=["history_added"],
            callback=lambda e: None,
        )
        assert "subscription_id" in result
        assert result["browser"] == "chrome"

    def test_subscribe_with_multiple_event_types(self):
        """Multiple event types subscription should work."""
        from chronicle_mcp.core.services import HistoryService

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        result = HistoryService.subscribe_history_changes(
            browser="chrome",
            event_types=["history_added", "bookmark_added"],
            callback=lambda e: None,
        )
        assert "subscription_id" in result
        assert len(result["event_types"]) == 2

    def test_unsubscribe_returns_correct_structure(self):
        """Unsubscribe should return correct structure."""
        from chronicle_mcp.core.services import HistoryService

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        sub_result = HistoryService.subscribe_history_changes(
            browser="chrome",
            event_types=[EventType.HISTORY_ADDED],
            callback=lambda e: None,
        )
        sub_id = sub_result["subscription_id"]

        result = HistoryService.unsubscribe_history_changes(sub_id)
        assert "subscription_id" in result
        assert "success" in result
        assert result["success"] is True

    def test_get_subscription_status_global_returns_stats(self):
        """Get subscription status without ID returns global stats."""
        from chronicle_mcp.core.services import HistoryService

        manager = get_subscription_manager()
        manager.unsubscribe_all()

        result = HistoryService.get_subscription_status()
        assert "active_subscriptions" in result
        assert "total_events" in result


class TestAnalyticsMutationSafety:
    """Tests to ensure analytics calculations survive code changes."""

    def test_compare_time_periods_same_period_no_change(self):
        """Same start/end dates should show zero delta."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection') as mock_conn:
            mock_conn.return_value = {
                "total_visits": 100,
                "unique_urls": 50,
                "top_domains": [("example.com", 100)],
            }
            result = HistoryService.compare_time_periods(
                start_date1="2024-01-01",
                end_date1="2024-01-31",
                start_date2="2024-01-01",
                end_date2="2024-01-31",
                browser="chrome",
            )
            assert result["changes"]["total_visits_delta"] == 0

    def test_analyze_productivity_returns_score_and_grade(self):
        """Productivity analysis should return score and grade."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection') as mock_conn:
            mock_conn.return_value = {}
            result = HistoryService.analyze_productivity(browser="chrome")
            assert "productivity_score" in result
            assert "grade" in result
            assert isinstance(result["productivity_score"], (int, float))
            assert result["grade"] in ["A", "B+", "B", "C", "D", "F", "N/A"]


class TestExportVisualizationMutationSafety:
    """Tests to ensure visualization export survives code changes."""

    def test_export_visualization_chart_json_structure(self):
        """Chart JSON export should have correct structure."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection') as mock_conn:
            mock_conn.return_value = {}
            result = HistoryService.export_visualization(
                format_type="chart_json",
                period="month",
                browser="chrome",
            )
            assert "charts" in result
            assert "period" in result

    def test_export_visualization_csv_content(self):
        """CSV export should return string content."""
        from chronicle_mcp.core.services import HistoryService

        with patch.object(HistoryService, '_with_connection') as mock_conn:
            mock_conn.return_value = {}
            result = HistoryService.export_visualization(
                format_type="csv",
                period="week",
                browser="chrome",
            )
            assert "content" in result
            assert "format" in result
            assert result["format"] == "csv"


class TestInsightsReportMutationSafety:
    """Tests to ensure insights report survives code changes."""

    def test_insights_report_method_exists(self):
        """Verify generate_insights_report method exists and is callable."""
        from chronicle_mcp.core.services import HistoryService

        assert hasattr(HistoryService, 'generate_insights_report')
        assert callable(HistoryService.generate_insights_report)
