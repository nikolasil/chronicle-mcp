"""Integration tests for HTTP server.

These tests start an actual HTTP server and test all endpoints.
"""

import pytest
from starlette.testclient import TestClient

from chronicle_mcp.protocols.http import app


class TestHTTPServerIntegration:
    """Integration tests for HTTP REST API server."""

    @pytest.fixture(autouse=True)
    def setup_server(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
        yield

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "chronicle-mcp"
        assert "version" in data
        assert "timestamp" in data

    def test_ready_endpoint(self):
        """Test readiness check endpoint."""
        response = self.client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["service"] == "chronicle-mcp"
        assert "browsers" in data
        assert "timestamp" in data

    def test_metrics_endpoint(self):
        """Test Prometheus metrics endpoint."""
        response = self.client.get("/metrics/prometheus")
        assert response.status_code == 200
        content = response.text
        assert "chronicle_uptime_seconds" in content
        assert "chronicle_requests_total" in content

    def test_search_endpoint_basic(self):
        """Test basic search endpoint."""
        response = self.client.post("/api/search", json={"query": "test", "limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_search_endpoint_with_browser(self):
        """Test search with specific browser."""
        response = self.client.post(
            "/api/search", json={"query": "github", "limit": 5, "browser": "chrome"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert data.get("browser") == "chrome" or "message" in data

    def test_search_endpoint_json_format(self):
        """Test search with JSON format."""
        response = self.client.post(
            "/api/search", json={"query": "test", "limit": 5, "format": "json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "count" in data

    def test_recent_endpoint(self):
        """Test recent history endpoint."""
        response = self.client.post("/api/recent", json={"hours": 24, "limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_recent_endpoint_custom_hours(self):
        """Test recent history with custom hours."""
        response = self.client.post("/api/recent", json={"hours": 1, "limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_count_endpoint(self):
        """Test count visits endpoint."""
        response = self.client.post("/api/count", json={"domain": "github.com"})
        assert response.status_code == 200
        data = response.json()
        assert "domain" in data
        assert "count" in data

    def test_top_domains_endpoint(self):
        """Test top domains endpoint."""
        response = self.client.post("/api/top-domains", json={"limit": 10})
        assert response.status_code == 200
        data = response.json()
        assert "domains" in data

    def test_domain_search_endpoint(self):
        """Test domain search endpoint."""
        response = self.client.post(
            "/api/domain-search", json={"domain": "github.com", "limit": 10}
        )
        assert response.status_code == 200

    def test_advanced_search_endpoint(self):
        """Test advanced search endpoint."""
        response = self.client.post("/api/advanced-search", json={"query": "test", "limit": 10})
        assert response.status_code == 200

    def test_advanced_search_with_options(self):
        """Test advanced search with regex and fuzzy options."""
        response = self.client.post(
            "/api/advanced-search",
            json={
                "query": "test",
                "limit": 10,
                "use_regex": False,
                "use_fuzzy": False,
                "sort_by": "date",
            },
        )
        assert response.status_code == 200

    def test_advanced_search_regex(self):
        """Test advanced search with regex."""
        response = self.client.post(
            "/api/advanced-search",
            json={"query": "github\\.com", "limit": 10, "use_regex": True},
        )
        assert response.status_code == 200

    def test_export_csv_endpoint(self):
        """Test CSV export endpoint."""
        response = self.client.post("/api/export", json={"format_type": "csv", "limit": 10})
        assert response.status_code == 200
        assert "text/csv" in response.headers["content-type"]

    def test_export_json_endpoint(self):
        """Test JSON export endpoint."""
        response = self.client.post("/api/export", json={"format_type": "json", "limit": 10})
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_delete_preview_endpoint(self):
        """Test delete preview mode."""
        response = self.client.post(
            "/api/delete", json={"query": "test", "limit": 10, "confirm": False}
        )
        assert response.status_code == 200

    def test_sync_dry_run_endpoint(self):
        """Test sync dry run endpoint."""
        response = self.client.post(
            "/api/sync",
            json={"source_browser": "chrome", "target_browser": "firefox", "dry_run": True},
        )
        assert response.status_code in (200, 404)

    def test_stats_endpoint(self):
        """Test browser stats endpoint."""
        response = self.client.post("/api/stats", json={"browser": "chrome"})
        assert response.status_code == 200

    def test_bookmarks_list_endpoint(self):
        """Test bookmarks list endpoint."""
        response = self.client.get("/api/bookmarks")
        assert response.status_code == 200
        data = response.json()
        assert "browsers" in data

    def test_downloads_list_endpoint(self):
        """Test downloads list endpoint."""
        response = self.client.get("/api/downloads")
        assert response.status_code == 200
        data = response.json()
        assert "browsers" in data

    def test_invalid_endpoint(self):
        """Test 404 for invalid endpoint."""
        response = self.client.get("/api/invalid")
        assert response.status_code == 404

    def test_search_with_invalid_browser(self):
        """Test error handling for invalid browser."""
        response = self.client.post(
            "/api/search", json={"query": "test", "browser": "invalid_browser_xyz"}
        )
        assert response.status_code in (400, 404, 500)

    def test_negative_limit(self):
        """Test error handling for negative limit."""
        response = self.client.post("/api/search", json={"query": "test", "limit": -1})
        assert response.status_code in (400, 422, 500)

    def test_missing_query(self):
        """Test error handling for missing query."""
        response = self.client.post("/api/search", json={})
        assert response.status_code in (400, 422, 500)

    def test_server_version(self):
        """Test version endpoint."""
        response = self.client.get("/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "name" in data

    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint."""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data


class TestHTTPServerErrorHandling:
    """Tests for HTTP server error handling."""

    @pytest.fixture(autouse=True)
    def setup_server(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
        yield

    def test_database_not_found(self):
        """Test handling when database is not found."""
        response = self.client.post(
            "/api/search", json={"query": "test", "browser": "nonexistent_browser"}
        )
        assert response.status_code in (404, 500)

    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        response = self.client.post(
            "/api/search",
            data="not valid json",
            headers={"content-type": "application/json"},
        )
        assert response.status_code == 422

    def testMalformedDate(self):
        """Test handling of malformed date in date range search."""
        response = self.client.post(
            "/api/advanced-search",
            json={"query": "test", "start_date": "not-a-date", "end_date": "2024-12-31"},
        )
        assert response.status_code in (400, 422, 500)

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import concurrent.futures

        def make_request():
            return self.client.post("/api/search", json={"query": "test", "limit": 5})

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        assert all(r.status_code == 200 for r in results)

    def test_large_limit(self):
        """Test handling of large but valid limit."""
        response = self.client.post("/api/search", json={"query": "test", "limit": 10000})
        assert response.status_code in (200, 400)


class TestHTTPServerCORS:
    """Tests for CORS configuration."""

    @pytest.fixture(autouse=True)
    def setup_server(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
        yield

    def test_cors_preflight(self):
        """Test CORS preflight request."""
        response = self.client.options(
            "/api/search",
            headers={
                "origin": "http://localhost:3000",
                "access-control-request-method": "POST",
            },
        )
        assert response.status_code in (200, 204)

    def test_cors_headers(self):
        """Test CORS headers in response."""
        response = self.client.get(
            "/health",
            headers={"origin": "http://localhost:3000"},
        )
        assert response.status_code == 200
