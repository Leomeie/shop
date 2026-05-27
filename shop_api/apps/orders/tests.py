import pytest
from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.products.models import Category, Product, SKU
from apps.cart.models import CartItem
from apps.orders.models import Order, OrderItem
from apps.payment.models import Payment

User = get_user_model()

ORDER_BASE = "/api/v1/orders/"
PAYMENT_BASE = "/api/v1/payment/"


# ── Fixtures ──

def _img(name="test.jpg"):
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


@pytest.fixture
def order_user(db):
    return User.objects.create_user(
        username="order_user",
        email="order_user@example.com",
        password="userpass123",
        phone="1390000001",
    )


@pytest.fixture
def order_client(order_user):
    c = APIClient()
    c.force_authenticate(user=order_user)
    return c


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="other_user",
        email="other@example.com",
        password="userpass123",
        phone="1390000002",
    )


@pytest.fixture
def other_client(other_user):
    c = APIClient()
    c.force_authenticate(user=other_user)
    return c


@pytest.fixture
def category(db):
    return Category.objects.create(name="Order Test Cat")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Order Test Product",
        category=category,
        main_image=_img(),
        file=_file(),
        status="active",
    )


@pytest.fixture
def sku(product):
    return SKU.objects.create(
        product=product,
        name="Standard",
        price=1990,  # 19.90 yuan
        original_price=2990,
        is_active=True,
    )


@pytest.fixture
def sku2(product):
    return SKU.objects.create(
        product=product,
        name="Pro",
        price=4990,
        original_price=5990,
        is_active=True,
    )


@pytest.fixture
def inactive_sku(product):
    return SKU.objects.create(
        product=product,
        name="Discontinued",
        price=990,
        is_active=False,
    )


def _add_to_cart(user, sku, quantity=1, selected=True):
    CartItem.objects.create(user=user, sku=sku, quantity=quantity, selected=selected)


# ── Order Creation ──

class TestOrderCreate:
    def test_create_order_from_selected_cart(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku, quantity=2)
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data["data"]
        assert data["order_no"]
        assert data["total_amount"] == 1990 * 2
        assert data["pay_amount"] == 1990 * 2
        assert data["status"] == "pending"
        assert len(data["items"]) == 2  # quantity=2 → 2 OrderItems

    def test_order_number_is_unique(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        resp1 = order_client.post(f"{ORDER_BASE}create/", format="json")
        _add_to_cart(order_user, sku)
        resp2 = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp1.data["data"]["order_no"] != resp2.data["data"]["order_no"]

    def test_order_items_snapshot_product_info(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        item = resp.data["data"]["items"][0]
        assert item["product_name"] == sku.product.name
        assert item["sku_name"] == sku.name
        assert item["price"] == 1990

    def test_order_removes_selected_items_from_cart(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_client.post(f"{ORDER_BASE}create/", format="json")
        assert CartItem.objects.filter(user=order_user).count() == 0

    def test_order_with_remark(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        resp = order_client.post(
            f"{ORDER_BASE}create/",
            {"remark": "请尽快发货"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        order = Order.objects.get(order_no=resp.data["data"]["order_no"])
        assert order.remark == "请尽快发货"

    def test_order_total_multiple_skus(self, order_client, order_user, sku, sku2):
        _add_to_cart(order_user, sku, quantity=1)
        _add_to_cart(order_user, sku2, quantity=1)
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data["data"]
        assert data["total_amount"] == 1990 + 4990
        assert data["pay_amount"] == 1990 + 4990

    def test_order_fails_empty_cart(self, order_client):
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_order_fails_no_selected_items(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku, selected=False)
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_order_fails_inactive_sku(self, order_client, order_user, inactive_sku):
        _add_to_cart(order_user, inactive_sku)
        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated_cannot_create_order(self, api_client):
        resp = api_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ── Payment Flow ──

class TestPaymentFlow:
    def test_create_payment_for_pending_order(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert data["payment_no"].startswith("PAY")
        assert data["amount"] == 1990
        assert data["amount_yuan"] == 19.9
        assert "pay_url" in data

    def test_payment_callback_completes_order(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        # Create payment
        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)

        # Mock callback (AllowAny)
        callback_client = APIClient()
        resp = callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # Verify order status
        order.refresh_from_db()
        assert order.status == "completed"
        assert order.pay_time is not None
        assert order.complete_time is not None

        # Verify payment status
        payment.refresh_from_db()
        assert payment.status == "success"
        assert payment.paid_at is not None

    def test_payment_increments_download_count(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        product = sku.product
        initial_count = product.download_count

        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)
        callback_client = APIClient()
        callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )

        product.refresh_from_db()
        assert product.download_count == initial_count + 1

    def test_cannot_pay_already_paid_order(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        # First payment
        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)
        callback_client = APIClient()
        callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )

        # Second payment attempt
        resp = order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_pay_others_order(self, order_client, other_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = other_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_pay_nonexistent_order(self, order_client):
        resp = order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": 99999, "method": "mock"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_payment_query(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)

        resp = order_client.get(f"{PAYMENT_BASE}{payment.payment_no}/")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert data["payment_no"] == payment.payment_no
        assert data["status"] == "pending"

    def test_payment_callback_missing_payment_no(self):
        callback_client = APIClient()
        resp = callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_payment_callback_already_processed(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)

        callback_client = APIClient()
        # First callback succeeds
        callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )
        # Second callback fails
        resp = callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── Order Cancel ──

class TestOrderCancel:
    def test_cancel_pending_order(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = order_client.post(f"{ORDER_BASE}{order.id}/cancel/", format="json")
        assert resp.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == "cancelled"

    def test_cannot_cancel_paid_order(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        # Pay the order
        order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        payment = Payment.objects.get(order=order)
        callback_client = APIClient()
        callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment.payment_no},
            format="json",
        )

        resp = order_client.post(f"{ORDER_BASE}{order.id}/cancel/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_cancel_nonexistent_order(self, order_client):
        resp = order_client.post(f"{ORDER_BASE}99999/cancel/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_cancel_others_order(self, order_client, other_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = other_client.post(f"{ORDER_BASE}{order.id}/cancel/", format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── Order List & Detail ──

class TestOrderListDetail:
    def test_list_orders(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_client.post(f"{ORDER_BASE}create/", format="json")

        resp = order_client.get(ORDER_BASE)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 1

    def test_list_orders_filter_by_status(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_client.post(f"{ORDER_BASE}create/", format="json")

        resp = order_client.get(f"{ORDER_BASE}?status=pending")
        assert resp.data["count"] == 1

        resp = order_client.get(f"{ORDER_BASE}?status=completed")
        assert resp.data["count"] == 0

    def test_order_detail(self, order_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = order_client.get(f"{ORDER_BASE}{order.id}/")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data
        assert data["order_no"] == order_no
        assert "items" in data

    def test_cannot_view_others_order(self, order_client, other_client, order_user, sku):
        _add_to_cart(order_user, sku)
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)

        resp = other_client.get(f"{ORDER_BASE}{order.id}/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthenticated_cannot_list_orders(self, api_client):
        resp = api_client.get(ORDER_BASE)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ── Full Integration: Cart → Order → Payment → Download ──

class TestFullFlow:
    def test_cart_to_order_to_payment_to_download(self, order_client, order_user, sku):
        # 1. Add to cart
        _add_to_cart(order_user, sku, quantity=1)

        # 2. Create order
        order_resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert order_resp.status_code == status.HTTP_201_CREATED
        order_no = order_resp.data["data"]["order_no"]
        order = Order.objects.get(order_no=order_no)
        assert order.status == "pending"

        # 3. Create payment
        pay_resp = order_client.post(
            f"{PAYMENT_BASE}create/",
            {"order_id": order.id, "method": "mock"},
            format="json",
        )
        assert pay_resp.status_code == status.HTTP_200_OK
        payment_no = pay_resp.data["data"]["payment_no"]

        # 4. Mock callback
        callback_client = APIClient()
        cb_resp = callback_client.post(
            f"{PAYMENT_BASE}callback/",
            {"payment_no": payment_no},
            format="json",
        )
        assert cb_resp.status_code == status.HTTP_200_OK

        # 5. Verify order completed
        order.refresh_from_db()
        assert order.status == "completed"

        # 6. Download token available
        item = order.items.first()
        dl_resp = order_client.get(f"{ORDER_BASE}{order.id}/items/{item.id}/download/")
        assert dl_resp.status_code == status.HTTP_200_OK
        assert "download_token" in dl_resp.data["data"]

    def test_full_flow_cart_cleared_after_order(self, order_client, order_user, sku, sku2):
        _add_to_cart(order_user, sku, quantity=1)
        _add_to_cart(order_user, sku2, quantity=1)

        order_client.post(f"{ORDER_BASE}create/", format="json")

        # Cart should be empty after order creation
        assert CartItem.objects.filter(user=order_user).count() == 0

    def test_partial_order_selected_items_only(self, order_client, order_user, sku, sku2):
        _add_to_cart(order_user, sku, selected=True)
        _add_to_cart(order_user, sku2, selected=False)

        resp = order_client.post(f"{ORDER_BASE}create/", format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data["data"]
        # Only sku (1990) should be in the order
        assert data["total_amount"] == 1990

        # sku2 should still be in cart
        assert CartItem.objects.filter(user=order_user, sku=sku2).exists()
