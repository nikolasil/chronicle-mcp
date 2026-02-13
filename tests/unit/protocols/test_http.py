"""Tests for HTTP protocol endpoints.

These tests verify the HTTP REST API endpoints.
"""

import pytest
from starlette.testclient import TestClient

from chronicle_mcp.protocols.http import app


@pytest.fixture
def http_client():
    """Provides a synchronous HTTP client for testing."""
    with TestClient(app=app) as client:
        yield client


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, http_client):
        """Test health check endpoint returns healthy status."""
        response = http_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "chronicle-mcp"
        assert "version" in data
        assert "timestamp" in data

    def test_ready_check(self, http_client):
        """Test readiness check endpoint."""
        response = http_client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["service"] == "chronicle-mcp"
        assert "browsers" in data
        assert "timestamp" in data


class TestMetricsEndpoints:
    """Tests for metrics endpoints."""

    def test_metrics_endpoint(self, http_client):
        """Test metrics endpoint returns statistics."""
        response = http_client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "requests_total" in data
        assert "requests_per_second" in data
        assert "average_latency_seconds" in data
        assert "browsers_available" in data

    def test_prometheus_metrics(self, http_client):
        """Test Prometheus metrics endpoint."""
        response = http_client.get("/metrics/prometheus")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        content = response.text
        assert "chronicle_uptime_seconds" in content
        assert "chronicle_requests_total" in content


class TestBrowserEndpoints:
    """Tests for browser API endpoints."""

    def test_list_browsers(self, http_client):
        """Test listing available browsers."""
        response = http_client.get("/api/browsers")
        assert response.status_code == 200
        data = response.json()
        assert "browsers" in data


class TestSearchEndpoints:
    """Tests for search API endpoints."""

    def test_search_endpoint(self, http_client):
        """Test search endpoint."""
        response = http_client.post("/api/search", json={"query": "test", "limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_search_with_format_json(self, http_client):
        """Test search with JSON format."""
        response = http_client.post(
            "/api/search", json={"query": "test", "limit": 5, "format": "json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "count" in data

    def test_recent_endpoint(self, http_client):
        """Test recent history endpoint."""
        response = http_client.post("/api/recent", json={"hours": 24, "limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_count_endpoint(self, http_client):
        """Test count visits endpoint."""
        response = http_client.post("/api/count", json={"domain": "github.com"})
        assert response.status_code == 200
        data = response.json()
        assert "domain" in data
        assert "browser" in data
        assert "count" in data

    def test_top_domains_endpoint(self, http_client):
        """Test top domains endpoint."""
        response = http_client.post("/api/top-domains", json={"limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "domains" in data


class TestAdvancedSearchEndpoints:
    """Tests for advanced search endpoints."""

    def test_domain_search(self, http_client):
        """Test domain search endpoint."""
        response = http_client.post(
            "/api/domain-search", json={"domain": "github.com", "limit": 10}
        )
        assert response.status_code == 200

    def test_advanced_search(self, http_client):
        """Test advanced search endpoint."""
        response = http_client.post("/api/advanced-search", json={"query": "test", "limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_advanced_search_with_options(self, http_client):
        """Test advanced search with regex and fuzzy options."""
        response = http_client.post(
            "/api/advanced-search",
            json={
                "query": "test",
                "limit": 10,
                "use_regex": True,
                "use_fuzzy": False,
                "sort_by": "date",
            },
        )
        assert response.status_code == 200


class TestExportEndpoints:
    """Tests for export endpoints."""

    def test_export_csv(self, http_client):
        """Test CSV export."""
        response = http_client.post("/api/export", json={"format_type": "csv", "limit": 10})
        assert response.status_code == 200
        assert "text/csv" in response.headers["content-type"]

    def test_export_json(self, http_client):
        """Test JSON export."""
        response = http_client.post("/api/export", json={"format_type": "json", "limit": 10})
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestDeleteEndpoints:
    """Tests for delete endpoints."""

    def test_delete_preview(self, http_client):
        """Test delete preview mode."""
        response = http_client.post(
            "/api/delete", json={"query": "test", "limit": 10, "confirm": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "preview" in data or "message" in data


class TestSyncEndpoints:
    """Tests for sync endpoints."""

    def test_sync_dry_run(self, http_client):
        """Test sync in dry-run mode."""
        response = http_client.post(
            "/api/sync",
            json={"source_browser": "chrome", "target_browser": "firefox", "dry_run": True},
        )
        assert response.status_code in (200, 404)
        data = response.json()
        if response.status_code == 200:
            assert "dry_run" in data
            assert data["dry_run"] is True


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_endpoint(self, http_client):
        """Test 404 for invalid endpoint."""
        response = http_client.get("/api/invalid")
        assert response.status_code == 404

    def test_search_invalid_browser(self, http_client):
        """Test error handling for invalid browser."""
        response = http_client.post(
            "/api/search", json={"query": "test", "browser": "invalid_browser_xyz"}
        )
        assert response.status_code in (200, 400, 404)
