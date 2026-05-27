import pytest

try:
    import drf_spectacular  # noqa: F401
    HAS_SPECTACULAR = True
except ImportError:
    HAS_SPECTACULAR = False

pytestmark = pytest.mark.skipif(
    not HAS_SPECTACULAR,
    reason="drf-spectacular not installed",
)


@pytest.mark.django_db
class TestSchemaEndpoint:
    def test_schema_json_accessible(self, api_client):
        resp = api_client.get("/api/schema/")
        assert resp.status_code == 200
        assert resp["Content-Type"].startswith("application/")

    def test_schema_contains_openapi_version(self, api_client):
        resp = api_client.get("/api/schema/")
        assert resp.status_code == 200
        data = resp.json()
        assert "openapi" in data
        assert data["openapi"].startswith("3.")

    def test_schema_contains_info(self, api_client):
        resp = api_client.get("/api/schema/")
        data = resp.json()
        assert "info" in data
        assert data["info"]["title"] == "ShopEase API"

    def test_schema_contains_paths(self, api_client):
        resp = api_client.get("/api/schema/")
        data = resp.json()
        assert "paths" in data
        assert len(data["paths"]) > 0


@pytest.mark.django_db
class TestSwaggerUI:
    def test_swagger_ui_accessible(self, api_client):
        resp = api_client.get("/api/docs/")
        assert resp.status_code == 200

    def test_swagger_ui_contains_html(self, api_client):
        resp = api_client.get("/api/docs/")
        assert b"swagger" in resp.content.lower()
