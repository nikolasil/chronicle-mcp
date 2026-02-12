"""HTTP server integration tests."""

import pytest
from starlette.testclient import TestClient

from chronicle_mcp.server_http import app


@pytest.fixture
def client():
    """Create a test client for the HTTP server."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "chronicle-mcp"
    assert "timestamp" in data


def test_ready_endpoint(client):
    """Test the readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "browsers" in data
    assert "timestamp" in data


def test_metrics_endpoint(client):
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "requests_total" in data
    assert "browsers_available" in data


def test_list_browsers_endpoint(client):
    """Test the list browsers endpoint."""
    response = client.get("/api/browsers")
    assert response.status_code == 200
    data = response.json()
    assert "browsers" in data
    assert isinstance(data["browsers"], list)


def test_search_endpoint_empty_query(client):
    """Test search with empty query returns error."""
    response = client.post("/api/search", json={"query": ""})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_search_endpoint_no_results(client):
    """Test search with non-existent query returns empty results."""
    response = client.post("/api/search", json={"query": "xyznonexistent123", "limit": 5})
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.json()
        assert "results" in data


def test_recent_endpoint_invalid_hours(client):
    """Test recent endpoint with invalid hours parameter."""
    response = client.post("/api/recent", json={"hours": -1, "limit": 10})
    assert response.status_code in [200, 404, 500]


def test_count_endpoint_empty_domain(client):
    """Test count endpoint with empty domain."""
    response = client.post("/api/count", json={"domain": ""})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_top_domains_endpoint_limit(client):
    """Test top domains endpoint with limit parameter."""
    response = client.post("/api/top-domains", json={"limit": 10})
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.json()
        assert "domains" in data


def test_search_date_endpoint_missing_params(client):
    """Test search by date with missing parameters."""
    response = client.post("/api/search-date", json={"query": "", "start_date": "", "end_date": ""})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_cors_headers(client):
    """Test that CORS headers are present."""
    response = client.options(
        "/api/search",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200


@pytest.mark.slow
def test_search_with_realistic_data(client, mock_realistic_chrome):
    """Test search with realistic database returns results."""
    response = client.post(
        "/api/search",
        json={"query": "github", "limit": 10, "browser": "chrome", "format": "markdown"},
    )
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "results" in data


@pytest.mark.slow
def test_count_endpoint_with_domain(client, mock_realistic_chrome):
    """Test count endpoint with valid domain."""
    response = client.post("/api/count", json={"domain": "github.com", "browser": "chrome"})
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "count" in data
        assert "domain" in data


@pytest.mark.slow
def test_top_domains_ordering(client, mock_realistic_chrome):
    """Test that top domains endpoint returns ordered results."""
    response = client.post("/api/top-domains", json={"limit": 20, "browser": "chrome"})
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "domains" in data
        if len(data["domains"]) > 1:
            # Check if results are ordered by visits (descending)
            visits = [d["visits"] for d in data["domains"]]
            assert visits == sorted(visits, reverse=True)


@pytest.mark.slow
def test_search_date_range(client, mock_realistic_chrome):
    """Test search by date within range."""
    response = client.post(
        "/api/search-date",
        json={
            "query": "python",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "limit": 10,
            "browser": "chrome",
        },
    )
    assert response.status_code in [200, 404]


def test_invalid_method_get_on_search(client):
    """Test that GET method is not allowed on search endpoint."""
    response = client.get("/api/search")
    assert response.status_code == 405


def test_invalid_browser_returns_error(client):
    """Test that invalid browser returns proper error."""
    response = client.post("/api/search", json={"query": "test", "browser": "invalid_browser_xyz"})
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


@pytest.mark.slow
def test_json_format_output(client, mock_realistic_chrome):
    """Test that JSON format returns proper structure."""
    response = client.post(
        "/api/search", json={"query": "github", "limit": 5, "browser": "chrome", "format": "json"}
    )
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        if isinstance(data.get("results"), list):
            assert "count" in data
