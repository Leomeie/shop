import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from apps.products.models import Category, Product


User = get_user_model()


@pytest.fixture
def category(db):
    return Category.objects.create(name="测试分类", level=1, is_active=True)


@pytest.fixture
def product(category, db):
    return Product.objects.create(
        name="测试商品",
        description="测试描述",
        category=category,
        status="active",
        main_image="test.jpg",
        file="test.zip",
        view_count=0,
    )


@pytest.fixture
def vc_admin_user(db):
    return User.objects.create_superuser(
        username="vc_admin",
        email="vc_admin@example.com",
        password="adminpass123",
        phone="13700000001",
    )


@pytest.fixture
def vc_admin_client(api_client, vc_admin_user):
    api_client.force_authenticate(user=vc_admin_user)
    return api_client


@pytest.fixture
def vc_test_user(db):
    return User.objects.create_user(
        username="vc_test",
        email="vc_test@example.com",
        password="testpass123",
        phone="13700000002",
    )


@pytest.mark.django_db
class TestViewCountDetail:
    def test_detail_returns_view_count(self, api_client, product):
        resp = api_client.get(f"/api/v1/products/{product.pk}/")
        assert resp.status_code == status.HTTP_200_OK
        assert "view_count" in resp.data

    def test_view_count_increments(self, api_client, product):
        api_client.get(f"/api/v1/products/{product.pk}/")
        product.refresh_from_db()
        assert product.view_count == 1

    def test_same_ip_no_double_count(self, api_client, product):
        api_client.get(f"/api/v1/products/{product.pk}/")
        api_client.get(f"/api/v1/products/{product.pk}/")
        product.refresh_from_db()
        assert product.view_count == 1

    def test_different_ips_increment(self, api_client, product):
        # First visit from IP1
        api_client.get(f"/api/v1/products/{product.pk}/", HTTP_X_FORWARDED_FOR="1.1.1.1")
        # Second visit from IP2
        api_client.get(f"/api/v1/products/{product.pk}/", HTTP_X_FORWARDED_FOR="2.2.2.2")
        product.refresh_from_db()
        assert product.view_count == 2

    def test_cache_key_format(self, api_client, product):
        api_client.get(f"/api/v1/products/{product.pk}/", HTTP_X_FORWARDED_FOR="10.0.0.1")
        cache_key = f"product_view:{product.pk}:10.0.0.1"
        assert cache.get(cache_key) is True


@pytest.mark.django_db
class TestAdminViewCountRanking:
    def test_admin_can_access(self, vc_admin_client, product):
        resp = vc_admin_client.get("/api/v1/admin/products/views/")
        assert resp.status_code == status.HTTP_200_OK

    def test_non_admin_denied(self, api_client, vc_test_user, product):
        api_client.force_authenticate(user=vc_test_user)
        resp = api_client.get("/api/v1/admin/products/views/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_denied(self, api_client, product):
        resp = api_client.get("/api/v1/admin/products/views/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_ranking_order(self, vc_admin_client, category, db):
        Product.objects.create(
            name="高浏览", category=category, status="active",
            main_image="a.jpg", file="a.zip", view_count=100,
        )
        Product.objects.create(
            name="低浏览", category=category, status="active",
            main_image="b.jpg", file="b.zip", view_count=10,
        )
        resp = vc_admin_client.get("/api/v1/admin/products/views/")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert data[0]["name"] == "高浏览"
        assert data[1]["name"] == "低浏览"

    def test_excludes_deleted_products(self, vc_admin_client, product, db):
        product.is_deleted = True
        product.save(update_fields=["is_deleted"])
        resp = vc_admin_client.get("/api/v1/admin/products/views/")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["data"]) == 0
