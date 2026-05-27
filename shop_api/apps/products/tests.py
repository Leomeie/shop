import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from .models import Category, Product, SKU, ProductImage

BASE = "/api/v1/products/"


# ── Fixtures (unique usernames to avoid migration conflict with 0003_create_superuser) ──

@pytest.fixture
def product_admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="prod_admin",
        email="prod_admin@example.com",
        password="adminpass123",
        phone="13800000010",
    )


@pytest.fixture
def product_admin_client(api_client, product_admin_user):
    api_client.force_authenticate(user=product_admin_user)
    return api_client


@pytest.fixture
def product_normal_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="prod_normal",
        email="prod_normal@example.com",
        password="userpass123",
        phone="13800000011",
    )


@pytest.fixture
def product_normal_client(api_client, product_normal_user):
    api_client.force_authenticate(user=product_normal_user)
    return api_client


# ── Helpers ──

def _img(name="test.jpg"):
    from io import BytesIO
    try:
        from PIL import Image
        buf = BytesIO()
        Image.new("RGB", (1, 1), "red").save(buf, format="JPEG")
        buf.seek(0)
        return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")
    except ImportError:
        return SimpleUploadedFile(name, b"\xff\xd8\xff" + b"\x00" * 100, content_type="image/jpeg")


def _file(name="test.zip"):
    return SimpleUploadedFile(name, b"PK" + b"\x00" * 100, content_type="application/zip")


def _create_category(name="Test Cat", parent=None, level=1, is_active=True):
    return Category.objects.create(name=name, parent=parent, level=level, is_active=is_active)


def _create_product(name="Test Product", category=None, status="active", **kwargs):
    product = Product.objects.create(
        name=name,
        category=category,
        main_image=_img(),
        file=_file(),
        status=status,
        **kwargs,
    )
    return product


def _create_sku(product, name="Basic", price=1000, original_price=2000, is_active=True):
    return SKU.objects.create(product=product, name=name, price=price, original_price=original_price, is_active=is_active)


# ── Public: Product List ──

@pytest.mark.django_db
class TestProductList:
    def test_empty_list(self, api_client):
        resp = api_client.get(BASE)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["results"] == []

    def test_returns_active_products_only(self, api_client):
        cat = _create_category()
        _create_product("Active", category=cat, status="active")
        _create_product("Draft", category=cat, status="draft")
        _create_product("Inactive", category=cat, status="inactive")
        resp = api_client.get(BASE)
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Active"

    def test_excludes_deleted_products(self, api_client):
        p = _create_product()
        p.is_deleted = True
        p.save(update_fields=["is_deleted"])
        resp = api_client.get(BASE)
        assert resp.data["count"] == 0

    def test_pagination(self, api_client):
        for i in range(25):
            _create_product(name=f"Product {i}")
        resp = api_client.get(BASE)
        assert resp.data["count"] == 25
        assert len(resp.data["results"]) == 20
        resp2 = api_client.get(BASE, {"page": 2})
        assert len(resp2.data["results"]) == 5

    def test_filter_by_category(self, api_client):
        cat1 = _create_category("Cat A")
        cat2 = _create_category("Cat B")
        _create_product("P1", category=cat1)
        _create_product("P2", category=cat2)
        resp = api_client.get(BASE, {"category": cat1.id})
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "P1"

    def test_filter_by_is_featured(self, api_client):
        _create_product("Featured", is_featured=True)
        _create_product("Normal", is_featured=False)
        resp = api_client.get(BASE, {"is_featured": "true"})
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Featured"

    def test_search_by_name(self, api_client):
        _create_product("Keyboard Pro")
        _create_product("Mouse Basic")
        resp = api_client.get(BASE, {"search": "Keyboard"})
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Keyboard Pro"

    def test_search_by_description(self, api_client):
        _create_product("Item A", description="mechanical switches")
        _create_product("Item B")
        resp = api_client.get(BASE, {"search": "mechanical"})
        assert resp.data["count"] == 1

    def test_ordering(self, api_client):
        p1 = _create_product("Old")
        p2 = _create_product("New")
        resp = api_client.get(BASE, {"ordering": "created_at"})
        names = [r["name"] for r in resp.data["results"]]
        assert "Old" in names and "New" in names

    def test_response_structure(self, api_client):
        cat = _create_category("Shoes")
        _create_product("Sneaker", category=cat)
        resp = api_client.get(BASE)
        item = resp.data["results"][0]
        assert "id" in item
        assert "name" in item
        assert "category" in item
        assert "category_name" in item
        assert item["category_name"] == "Shoes"
        assert "main_image" in item
        assert "min_price_yuan" in item
        assert "download_count" in item
        assert "view_count" in item
        assert "is_featured" in item
        assert "status" in item
        assert "created_at" in item


# ── Public: Product Detail ──

@pytest.mark.django_db
class TestProductDetail:
    def test_returns_200(self, api_client):
        p = _create_product()
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_returns_404_for_deleted(self, api_client):
        p = _create_product()
        p.is_deleted = True
        p.save(update_fields=["is_deleted"])
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_for_draft(self, api_client):
        p = _create_product(status="draft")
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_detail_structure(self, api_client):
        cat = _create_category("Software")
        p = _create_product("App v2", category=cat, description="A great app", version="2.0.0")
        s1 = _create_sku(p, name="Standard", price=9900, original_price=12900)
        s2 = _create_sku(p, name="Pro", price=19900, original_price=24900)
        resp = api_client.get(f"{BASE}{p.id}/")
        data = resp.data
        assert data["name"] == "App v2"
        assert data["category_name"] == "Software"
        assert data["description"] == "A great app"
        assert data["version"] == "2.0.0"
        assert len(data["skus"]) == 2
        sku_prices = {s["name"]: s["price"] for s in data["skus"]}
        assert sku_prices["Standard"] == 9900
        assert sku_prices["Pro"] == 19900

    def test_sku_yuan_conversion(self, api_client):
        p = _create_product()
        _create_sku(p, price=19900, original_price=24900)
        resp = api_client.get(f"{BASE}{p.id}/")
        sku = resp.data["skus"][0]
        assert sku["price_yuan"] == 199.0
        assert sku["original_price_yuan"] == 249.0

    def test_min_price_yuan(self, api_client):
        p = _create_product()
        _create_sku(p, name="Cheap", price=5000)
        _create_sku(p, name="Expensive", price=15000)
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.data["min_price_yuan"] == 50.0

    def test_increments_view_count(self, api_client):
        p = _create_product(view_count=0)
        api_client.get(f"{BASE}{p.id}/")
        p.refresh_from_db()
        assert p.view_count == 1
        api_client.get(f"{BASE}{p.id}/")
        p.refresh_from_db()
        assert p.view_count == 2

    def test_images_in_response(self, api_client):
        p = _create_product()
        ProductImage.objects.create(product=p, image=_img("a.jpg"), sort_order=0)
        ProductImage.objects.create(product=p, image=_img("b.jpg"), sort_order=1)
        resp = api_client.get(f"{BASE}{p.id}/")
        assert len(resp.data["images"]) == 2


# ── Admin: Product CRUD ──

@pytest.mark.django_db
class TestAdminProductCRUD:
    def test_admin_list(self, product_admin_client):
        _create_product("P1")
        _create_product("P2")
        resp = product_admin_client.get(f"{BASE}admin/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 2

    def test_admin_list_excludes_deleted(self, product_admin_client):
        p = _create_product()
        p.is_deleted = True
        p.save(update_fields=["is_deleted"])
        resp = product_admin_client.get(f"{BASE}admin/")
        assert resp.data["count"] == 0

    def test_admin_create_product(self, product_admin_client):
        cat = _create_category()
        resp = product_admin_client.post(f"{BASE}admin/", {
            "name": "New Product",
            "category": cat.id,
            "description": "Desc",
            "version": "1.0.0",
            "status": "draft",
            "main_image": _img(),
            "file": _file(),
        }, format="multipart")
        assert resp.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name="New Product").exists()

    def test_admin_update_product(self, product_admin_client):
        p = _create_product("Old Name")
        resp = product_admin_client.patch(f"{BASE}admin/{p.id}/", {
            "name": "New Name",
        }, format="multipart")
        assert resp.status_code == status.HTTP_200_OK
        p.refresh_from_db()
        assert p.name == "New Name"

    def test_admin_change_status_active_to_inactive(self, product_admin_client):
        p = _create_product(status="active")
        resp = product_admin_client.patch(f"{BASE}admin/{p.id}/", {
            "status": "inactive",
        }, format="multipart")
        assert resp.status_code == status.HTTP_200_OK
        p.refresh_from_db()
        assert p.status == "inactive"

    def test_admin_soft_delete(self, product_admin_client):
        p = _create_product()
        resp = product_admin_client.delete(f"{BASE}admin/{p.id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        p.refresh_from_db()
        assert p.is_deleted is True
        assert Product.objects.filter(pk=p.id).exists()

    def test_admin_batch_activate(self, product_admin_client):
        p1 = _create_product("P1", status="draft")
        p2 = _create_product("P2", status="draft")
        resp = product_admin_client.post(f"{BASE}admin/batch/", {
            "action": "activate",
            "ids": [p1.id, p2.id],
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        p1.refresh_from_db()
        p2.refresh_from_db()
        assert p1.status == "active"
        assert p2.status == "active"

    def test_admin_batch_deactivate(self, product_admin_client):
        p = _create_product(status="active")
        resp = product_admin_client.post(f"{BASE}admin/batch/", {
            "action": "deactivate",
            "ids": [p.id],
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        p.refresh_from_db()
        assert p.status == "inactive"

    def test_admin_batch_delete(self, product_admin_client):
        p = _create_product()
        resp = product_admin_client.post(f"{BASE}admin/batch/", {
            "action": "delete",
            "ids": [p.id],
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        p.refresh_from_db()
        assert p.is_deleted is True

    def test_admin_batch_invalid_action(self, product_admin_client):
        p = _create_product()
        resp = product_admin_client.post(f"{BASE}admin/batch/", {
            "action": "invalid",
            "ids": [p.id],
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        p.refresh_from_db()
        assert p.status == "active"


# ── Non-Admin: Permission Denial ──

@pytest.mark.django_db
class TestNonAdminPermission:
    def test_cannot_list_admin_products(self, product_normal_client):
        resp = product_normal_client.get(f"{BASE}admin/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_create_product(self, product_normal_client):
        resp = product_normal_client.post(f"{BASE}admin/", {
            "name": "Hacked",
        }, format="multipart")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_update_product(self, product_normal_client):
        p = _create_product()
        resp = product_normal_client.patch(f"{BASE}admin/{p.id}/", {
            "name": "Hacked",
        }, format="multipart")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_delete_product(self, product_normal_client):
        p = _create_product()
        resp = product_normal_client.delete(f"{BASE}admin/{p.id}/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_batch_operate(self, product_normal_client):
        resp = product_normal_client.post(f"{BASE}admin/batch/", {
            "action": "activate",
            "ids": [1],
        }, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_admin(self, api_client):
        resp = api_client.get(f"{BASE}admin/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ── Admin: SKU Management ──

@pytest.mark.django_db
class TestAdminSKU:
    def test_list_skus(self, product_admin_client):
        p = _create_product()
        _create_sku(p, "Basic", 1000)
        _create_sku(p, "Pro", 2000)
        resp = product_admin_client.get(f"{BASE}admin/{p.id}/skus/")
        assert resp.status_code == status.HTTP_200_OK
        results = resp.data.get("results", resp.data)
        assert len(results) == 2

    def test_create_sku(self, product_admin_client):
        p = _create_product()
        resp = product_admin_client.post(f"{BASE}admin/{p.id}/skus/", {
            "name": "Enterprise",
            "price": 50000,
            "original_price": 60000,
            "license_description": "Team license",
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert SKU.objects.filter(product=p, name="Enterprise").exists()

    def test_update_sku(self, product_admin_client):
        p = _create_product()
        s = _create_sku(p, "Basic", 1000)
        resp = product_admin_client.patch(f"{BASE}admin/{p.id}/skus/{s.id}/", {
            "price": 1500,
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        s.refresh_from_db()
        assert s.price == 1500

    def test_delete_sku(self, product_admin_client):
        p = _create_product()
        s = _create_sku(p)
        resp = product_admin_client.delete(f"{BASE}admin/{p.id}/skus/{s.id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert not SKU.objects.filter(pk=s.id).exists()

    def test_sku_yuan_fields(self, product_admin_client):
        p = _create_product()
        _create_sku(p, "Basic", price=9900, original_price=12900)
        resp = product_admin_client.get(f"{BASE}admin/{p.id}/skus/")
        results = resp.data.get("results", resp.data)
        sku = results[0]
        assert sku["price_yuan"] == 99.0
        assert sku["original_price_yuan"] == 129.0

    def test_non_admin_cannot_manage_skus(self, product_normal_client):
        p = _create_product()
        resp = product_normal_client.get(f"{BASE}admin/{p.id}/skus/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN


# ── Admin: Category Management ──

@pytest.mark.django_db
class TestAdminCategory:
    def test_admin_list_categories(self, product_admin_client):
        _create_category("Cat A")
        _create_category("Cat B")
        resp = product_admin_client.get(f"{BASE}admin/categories/")
        assert resp.status_code == status.HTTP_200_OK
        names = [c["name"] for c in resp.data]
        assert "Cat A" in names
        assert "Cat B" in names

    def test_admin_create_category(self, product_admin_client):
        resp = product_admin_client.post(f"{BASE}admin/categories/", {
            "name": "New Cat",
            "level": 1,
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Cat").exists()

    def test_admin_update_category(self, product_admin_client):
        cat = _create_category("Old")
        resp = product_admin_client.patch(f"{BASE}admin/categories/{cat.id}/", {
            "name": "Updated",
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        cat.refresh_from_db()
        assert cat.name == "Updated"

    def test_admin_delete_category(self, product_admin_client):
        cat = _create_category()
        resp = product_admin_client.delete(f"{BASE}admin/categories/{cat.id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=cat.id).exists()

    def test_non_admin_cannot_manage_categories(self, product_normal_client):
        resp = product_normal_client.get(f"{BASE}admin/categories/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN


# ── Public: Category Endpoints ──

@pytest.mark.django_db
class TestCategoryEndpoints:
    def test_category_tree(self, api_client):
        parent = _create_category("ParentTree")
        _create_category("Child 1", parent=parent, level=2)
        _create_category("Child 2", parent=parent, level=2)
        resp = api_client.get(f"{BASE}categories/")
        assert resp.status_code == status.HTTP_200_OK
        tree = [c for c in resp.data if c["name"] == "ParentTree"]
        assert len(tree) == 1
        assert len(tree[0]["children"]) == 2

    def test_category_tree_excludes_inactive(self, api_client):
        parent = _create_category("InactiveTree")
        _create_category("Active Child", parent=parent, level=2, is_active=True)
        _create_category("Inactive Child", parent=parent, level=2, is_active=False)
        resp = api_client.get(f"{BASE}categories/")
        tree = [c for c in resp.data if c["name"] == "InactiveTree"]
        assert len(tree) == 1
        assert len(tree[0]["children"]) == 1

    def test_category_flat_list(self, api_client):
        cat_a = _create_category("FlatA")
        cat_b = _create_category("FlatB")
        resp = api_client.get(f"{BASE}categories/flat/")
        assert resp.status_code == status.HTTP_200_OK
        names = [c["name"] for c in resp.data]
        assert "FlatA" in names
        assert "FlatB" in names

    def test_category_flat_excludes_inactive(self, api_client):
        _create_category("FlatActive", is_active=True)
        _create_category("FlatInactive", is_active=False)
        resp = api_client.get(f"{BASE}categories/flat/")
        names = [c["name"] for c in resp.data]
        assert "FlatActive" in names
        assert "FlatInactive" not in names


# ── SKU Pricing Correctness ──

@pytest.mark.django_db
class TestSKUPricing:
    def test_min_price_with_active_skus(self, api_client):
        p = _create_product()
        _create_sku(p, "Basic", price=5000)
        _create_sku(p, "Pro", price=15000)
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.data["min_price_yuan"] == 50.0

    def test_min_price_ignores_inactive_skus(self, api_client):
        p = _create_product()
        _create_sku(p, "Cheap", price=1000, is_active=False)
        _create_sku(p, "Expensive", price=9900, is_active=True)
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.data["min_price_yuan"] == 99.0

    def test_min_price_zero_when_no_skus(self, api_client):
        p = _create_product()
        resp = api_client.get(f"{BASE}{p.id}/")
        assert resp.data["min_price_yuan"] == 0

    def test_price_filter_min(self, api_client):
        p1 = _create_product("Cheap")
        _create_sku(p1, price=5000)
        p2 = _create_product("Expensive")
        _create_sku(p2, price=15000)
        resp = api_client.get(BASE, {"min_price": 10000})
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Expensive"

    def test_price_filter_max(self, api_client):
        p1 = _create_product("Cheap")
        _create_sku(p1, price=5000)
        p2 = _create_product("Expensive")
        _create_sku(p2, price=15000)
        resp = api_client.get(BASE, {"max_price": 10000})
        assert resp.data["count"] == 1
        assert resp.data["results"][0]["name"] == "Cheap"
