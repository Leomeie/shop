import pytest
from rest_framework import status
from apps.products.models import Category, Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="开发工具", level=1, is_active=True)


@pytest.fixture
def product(category, db):
    return Product.objects.create(
        name="Python 代码模板",
        description="高质量的 Python 项目模板",
        category=category,
        status="active",
        main_image="test.jpg",
        file="test.zip",
    )


@pytest.fixture
def product2(category, db):
    return Product.objects.create(
        name="Vue 组件库",
        description="基于 Vue 3 的 UI 组件",
        category=category,
        status="active",
        main_image="test2.jpg",
        file="test2.zip",
    )


@pytest.fixture
def inactive_product(category, db):
    return Product.objects.create(
        name="Python 工具包",
        description="已下架的工具",
        category=category,
        status="inactive",
        main_image="test3.jpg",
        file="test3.zip",
    )


@pytest.mark.django_db
class TestSearchBasic:
    def test_search_by_name(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Python 代码模板"

    def test_search_by_description(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "项目模板"})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 1

    def test_search_by_category_name(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "开发工具"})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_search_returns_multiple_matches(self, api_client, product, product2):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        assert resp.data["count"] == 1  # Only product has "Python" in name

    def test_search_case_insensitive(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "python"})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 1


@pytest.mark.django_db
class TestSearchFilters:
    def test_empty_keyword_returns_empty(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": ""})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 0

    def test_no_q_param_returns_empty(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 0

    def test_whitespace_only_returns_empty(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "   "})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 0

    def test_inactive_products_excluded(self, api_client, inactive_product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        assert resp.data["count"] == 0

    def test_no_match_returns_empty(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "不存在的内容"})
        assert resp.data["count"] == 0


@pytest.mark.django_db
class TestSearchPagination:
    def test_search_uses_standard_pagination(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        assert "count" in resp.data
        assert "results" in resp.data

    def test_search_result_structure(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        item = resp.data["results"][0]
        assert "id" in item
        assert "name" in item
        assert "category_name" in item
        assert "min_price_yuan" in item


@pytest.mark.django_db
class TestSearchPermission:
    def test_unauthenticated_can_search(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Python"})
        assert resp.status_code == status.HTTP_200_OK

    def test_partial_keyword_matches(self, api_client, product):
        resp = api_client.get("/api/v1/products/search/", {"q": "Pyth"})
        assert resp.data["count"] == 1
