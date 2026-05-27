import pytest
from unittest.mock import patch
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_returns_200(self, api_client):
        resp = api_client.get("/api/health/")
        assert resp.status_code == status.HTTP_200_OK

    def test_health_returns_ok_status(self, api_client):
        resp = api_client.get("/api/health/")
        data = resp.json()
        assert data["status"] == "ok"
        assert data["db"] == "ok"
        assert data["cache"] == "ok"

    def test_health_no_auth_required(self, api_client):
        resp = api_client.get("/api/health/")
        assert resp.status_code == status.HTTP_200_OK

    def test_health_db_error_returns_503(self, api_client):
        with patch("config.views.connection") as mock_conn:
            mock_conn.ensure_connection.side_effect = Exception("db down")
            resp = api_client.get("/api/health/")
            assert resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            data = resp.json()
            assert data["status"] == "error"
            assert data["db"] == "error"

    def test_health_cache_error_returns_503(self, api_client):
        with patch("config.views.cache") as mock_cache:
            mock_cache.set.side_effect = Exception("cache down")
            resp = api_client.get("/api/health/")
            assert resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            data = resp.json()
            assert data["status"] == "error"
            assert data["cache"] == "error"
