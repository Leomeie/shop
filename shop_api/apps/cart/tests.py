import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from apps.products.models import Category, Product, SKU
from .models import CartItem

BASE = "/api/v1/cart/"


# ── Fixtures ──

@pytest.fixture
def cart_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="cart_user",
        email="cart_user@example.com",
        password="userpass123",
        phone="13900000001",
    )


@pytest.fixture
def cart_client(cart_user):
    c = APIClient()
    c.force_authenticate(user=cart_user)
    return c


@pytest.fixture
def second_cart_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="second_cart_user",
        email="second_cart@example.com",
        password="userpass123",
        phone="13900000002",
    )


@pytest.fixture
def second_cart_client(second_cart_user):
    c = APIClient()
    c.force_authenticate(user=second_cart_user)
    return c


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


def _create_category(name="Test Cat"):
    return Category.objects.create(name=name)


def _create_product(name="Test Product", category=None, status="active"):
    return Product.objects.create(
        name=name,
        category=category,
        main_image=_img(),
        file=_file(),
        status=status,
    )


def _create_sku(product, name="Basic", price=1000, original_price=2000, is_active=True):
    return SKU.objects.create(
        product=product, name=name, price=price,
        original_price=original_price, is_active=is_active,
    )


# ── Auth: Unauthenticated Access ──

@pytest.mark.django_db
class TestCartAuth:
    def test_get_cart_requires_auth(self, api_client):
        resp = api_client.get(BASE)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_item_requires_auth(self, api_client):
        resp = api_client.post(BASE + "items/", {"sku_id": 1})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_item_requires_auth(self, api_client):
        resp = api_client.put(BASE + "items/1/", {"quantity": 2})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_item_requires_auth(self, api_client):
        resp = api_client.delete(BASE + "items/1/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_clear_cart_requires_auth(self, api_client):
        resp = api_client.delete(BASE)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_select_all_requires_auth(self, api_client):
        resp = api_client.post(BASE + "select-all/", {"selected": True})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_remove_selected_requires_auth(self, api_client):
        resp = api_client.post(BASE + "remove-selected/", {"sku_ids": [1]})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ── Add Items ──

@pytest.mark.django_db
class TestCartAdd:
    def test_add_single_item(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        resp = cart_client.post(BASE + "items/", {"sku_id": sku.id})
        assert resp.status_code == status.HTTP_200_OK
        assert "已加入购物车" in resp.data["message"]

    def test_add_item_increases_quantity(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 1
        assert resp.data["data"]["items"][0]["quantity"] == 2

    def test_add_item_with_quantity(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        resp = cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 3})
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["quantity"] == 3

    def test_add_accumulates_quantity(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 2})
        cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 3})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["quantity"] == 5

    def test_add_multiple_different_skus(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1", price=1000)
        sku2 = _create_sku(p, name="Sku2", price=2000)
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 2

    def test_add_inactive_sku_fails(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, is_active=False)
        resp = cart_client.post(BASE + "items/", {"sku_id": sku.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "商品不存在或已下架" in resp.data["message"]

    def test_add_nonexistent_sku_fails(self, cart_client):
        resp = cart_client.post(BASE + "items/", {"sku_id": 99999})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "商品不存在或已下架" in resp.data["message"]

    def test_add_missing_sku_id_fails(self, cart_client):
        resp = cart_client.post(BASE + "items/", {})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_quantity_zero_fails(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        resp = cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 0})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_quantity_exceeds_max_fails(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        resp = cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 100})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_item_selected_by_default(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["selected"] is True


# ── Get Cart ──

@pytest.mark.django_db
class TestCartGet:
    def test_empty_cart(self, cart_client):
        resp = cart_client.get(BASE)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert data["items"] == []
        assert data["total_yuan"] == 0
        assert data["selected_total_yuan"] == 0
        assert data["count"] == 0

    def test_cart_with_items(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=1500)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        data = resp.data["data"]
        assert data["count"] == 1
        item = data["items"][0]
        assert item["sku_id"] == sku.id
        assert item["product_name"] == p.name
        assert item["sku_name"] == "Basic"
        assert item["price"] == 1500
        assert item["price_yuan"] == 15.0
        assert item["quantity"] == 1
        assert item["subtotal_yuan"] == 15.0

    def test_cart_total_yuan(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1", price=1000)
        sku2 = _create_sku(p, name="Sku2", price=2000)
        cart_client.post(BASE + "items/", {"sku_id": sku1.id, "quantity": 2})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id, "quantity": 1})
        resp = cart_client.get(BASE)
        data = resp.data["data"]
        assert data["total_yuan"] == 40.0  # 2*10 + 1*20
        assert data["count"] == 2

    def test_cart_selected_total(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1", price=1000)
        sku2 = _create_sku(p, name="Sku2", price=2000)
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        # Deselect second item
        cart_client.put(BASE + f"items/{sku2.id}/", {"selected": False})
        resp = cart_client.get(BASE)
        data = resp.data["data"]
        assert data["total_yuan"] == 30.0   # 10 + 20
        assert data["selected_total_yuan"] == 10.0  # only sku1

    def test_cart_original_price(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=1000, original_price=2000)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["original_price_yuan"] == 20.0

    def test_cart_hides_inactive_skus(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        # Deactivate SKU
        sku.is_active = False
        sku.save(update_fields=["is_active"])
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 0
        assert resp.data["data"]["items"] == []

    def test_user_isolation(self, cart_client, second_cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        # Second user should have empty cart
        resp = second_cart_client.get(BASE)
        assert resp.data["data"]["count"] == 0

    def test_cart_response_structure(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert "sku_id" in item
        assert "product_id" in item
        assert "product_name" in item
        assert "sku_name" in item
        assert "price" in item
        assert "price_yuan" in item
        assert "original_price_yuan" in item
        assert "image" in item
        assert "quantity" in item
        assert "selected" in item
        assert "subtotal_yuan" in item


# ── Update Cart Item ──

@pytest.mark.django_db
class TestCartUpdate:
    def test_update_quantity(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 5})
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["quantity"] == 5

    def test_update_selected(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.put(BASE + f"items/{sku.id}/", {"selected": False})
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["selected"] is False

    def test_update_both_fields(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 3, "selected": False})
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["quantity"] == 3
        assert item["selected"] is False

    def test_update_nonexistent_item(self, cart_client):
        resp = cart_client.put(BASE + "items/99999/", {"quantity": 2})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "购物车中无此商品" in resp.data["message"]

    def test_update_quantity_zero_fails(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 0})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_quantity_exceeds_max_fails(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 100})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_subtotal_changes(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=1000)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 3})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["subtotal_yuan"] == 30.0


# ── Delete Cart Item ──

@pytest.mark.django_db
class TestCartDelete:
    def test_delete_single_item(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.delete(BASE + f"items/{sku.id}/")
        assert resp.status_code == status.HTTP_200_OK
        assert "已删除" in resp.data["message"]
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 0

    def test_delete_nonexistent_item_succeeds(self, cart_client):
        resp = cart_client.delete(BASE + "items/99999/")
        assert resp.status_code == status.HTTP_200_OK

    def test_delete_one_of_many(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1")
        sku2 = _create_sku(p, name="Sku2")
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        cart_client.delete(BASE + f"items/{sku1.id}/")
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 1
        assert resp.data["data"]["items"][0]["sku_id"] == sku2.id


# ── Clear Cart ──

@pytest.mark.django_db
class TestCartClear:
    def test_clear_cart(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1")
        sku2 = _create_sku(p, name="Sku2")
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        resp = cart_client.delete(BASE)
        assert resp.status_code == status.HTTP_200_OK
        assert "购物车已清空" in resp.data["message"]
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 0

    def test_clear_empty_cart(self, cart_client):
        resp = cart_client.delete(BASE)
        assert resp.status_code == status.HTTP_200_OK


# ── Select All ──

@pytest.mark.django_db
class TestCartSelectAll:
    def test_select_all(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1")
        sku2 = _create_sku(p, name="Sku2")
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        # Deselect all
        cart_client.post(BASE + "select-all/", {"selected": False})
        resp = cart_client.get(BASE)
        for item in resp.data["data"]["items"]:
            assert item["selected"] is False
        # Select all
        cart_client.post(BASE + "select-all/", {"selected": True})
        resp = cart_client.get(BASE)
        for item in resp.data["data"]["items"]:
            assert item["selected"] is True

    def test_select_all_default_true(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.post(BASE + "select-all/")
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        assert resp.data["data"]["items"][0]["selected"] is True

    def test_deselect_all_clears_selected_total(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=1000)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        cart_client.post(BASE + "select-all/", {"selected": False})
        resp = cart_client.get(BASE)
        assert resp.data["data"]["selected_total_yuan"] == 0


# ── Remove Selected ──

@pytest.mark.django_db
class TestCartRemoveSelected:
    def test_remove_selected(self, cart_client):
        p = _create_product()
        sku1 = _create_sku(p, name="Sku1")
        sku2 = _create_sku(p, name="Sku2")
        sku3 = _create_sku(p, name="Sku3")
        cart_client.post(BASE + "items/", {"sku_id": sku1.id})
        cart_client.post(BASE + "items/", {"sku_id": sku2.id})
        cart_client.post(BASE + "items/", {"sku_id": sku3.id})
        resp = cart_client.post(BASE + "remove-selected/", {"sku_ids": [sku1.id, sku3.id]})
        assert resp.status_code == status.HTTP_200_OK
        resp = cart_client.get(BASE)
        assert resp.data["data"]["count"] == 1
        assert resp.data["data"]["items"][0]["sku_id"] == sku2.id

    def test_remove_selected_empty_list_fails(self, cart_client):
        resp = cart_client.post(BASE + "remove-selected/", {"sku_ids": []})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_remove_nonexistent_ids_succeeds(self, cart_client):
        resp = cart_client.post(BASE + "remove-selected/", {"sku_ids": [99999]})
        assert resp.status_code == status.HTTP_200_OK

    def test_remove_missing_sku_ids_fails(self, cart_client):
        resp = cart_client.post(BASE + "remove-selected/", {})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── Edge Cases ──

@pytest.mark.django_db
class TestCartEdgeCases:
    def test_add_then_get_shows_yuan_conversion(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=9999, original_price=19999)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["price_yuan"] == 99.99
        assert item["original_price_yuan"] == 199.99
        assert item["subtotal_yuan"] == 99.99

    def test_cart_with_quantity_and_price_math(self, cart_client):
        p = _create_product()
        sku = _create_sku(p, price=333)
        cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 7})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["subtotal_yuan"] == 23.31  # 333 * 7 / 100

    def test_update_only_quantity_preserves_selected(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id})
        cart_client.put(BASE + f"items/{sku.id}/", {"selected": False})
        cart_client.put(BASE + f"items/{sku.id}/", {"quantity": 3})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["quantity"] == 3
        assert item["selected"] is False

    def test_update_only_selected_preserves_quantity(self, cart_client):
        p = _create_product()
        sku = _create_sku(p)
        cart_client.post(BASE + "items/", {"sku_id": sku.id, "quantity": 5})
        cart_client.put(BASE + f"items/{sku.id}/", {"selected": False})
        resp = cart_client.get(BASE)
        item = resp.data["data"]["items"][0]
        assert item["quantity"] == 5
        assert item["selected"] is False
