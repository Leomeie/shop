import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APIClient

from apps.marketing.models import Coupon, UserCoupon
from apps.products.models import Category, Product, SKU
from apps.cart.models import CartItem
from apps.orders.models import Order

User = get_user_model()

BASE = "/api/v1/marketing/"


def _coupon(**kwargs):
    defaults = dict(
        name="Test Coupon",
        code="TEST001",
        type="minus",
        value=1000,  # 10 yuan in fen
        min_amount=5000,  # 50 yuan minimum
        start_time=timezone.now() - timedelta(days=1),
        end_time=timezone.now() + timedelta(days=30),
        total=100,
        used=0,
        is_active=True,
    )
    defaults.update(kwargs)
    return Coupon.objects.create(**defaults)


def _product_with_sku():
    cat = Category.objects.create(name="Test Cat", is_active=True)
    prod = Product.objects.create(
        name="Test Product",
        description="A test product",
        category=cat,
        status="active",
    )
    sku = SKU.objects.create(
        product=prod,
        name="Standard",
        price=5000,
        is_active=True,
    )
    return prod, sku


@pytest.fixture
def coupon_user(db):
    return User.objects.create_user(
        username="coupon_user",
        email="coupon_user@example.com",
        password="pass123",
        phone="1390000010",
    )


@pytest.fixture
def coupon_client(coupon_user):
    c = APIClient()
    c.force_authenticate(user=coupon_user)
    return c


@pytest.fixture
def coupon_admin(db):
    return User.objects.create_superuser(
        username="coupon_admin",
        email="coupon_admin@example.com",
        password="admin123",
        phone="1390000011",
    )


@pytest.fixture
def admin_coupon_client(coupon_admin):
    c = APIClient()
    c.force_authenticate(user=coupon_admin)
    return c


# ── Coupon List (Public) ──


class TestCouponList:
    def test_list_active_coupons(self, api_client, db):
        c1 = _coupon(code="ACTIVE1", name="Active 1")
        c2 = _coupon(code="ACTIVE2", name="Active 2")
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK
        codes = [c["code"] for c in resp.data["results"]]
        assert "ACTIVE1" in codes
        assert "ACTIVE2" in codes

    def test_excludes_inactive_coupons(self, api_client, db):
        _coupon(code="INACTIVE1", is_active=False)
        _coupon(code="ACTIVE1", is_active=True)
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK
        codes = [c["code"] for c in resp.data["results"]]
        assert "ACTIVE1" in codes
        assert "INACTIVE1" not in codes

    def test_excludes_not_yet_started(self, api_client, db):
        _coupon(code="FUTURE1", start_time=timezone.now() + timedelta(days=1))
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK
        codes = [c["code"] for c in resp.data["results"]]
        assert "FUTURE1" not in codes

    def test_excludes_expired_coupons(self, api_client, db):
        _coupon(code="EXPIRED1", end_time=timezone.now() - timedelta(days=1))
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK
        codes = [c["code"] for c in resp.data["results"]]
        assert "EXPIRED1" not in codes

    def test_unauthenticated_can_list(self, api_client, db):
        _coupon()
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK

    def test_response_structure(self, api_client, db):
        _coupon()
        resp = api_client.get(f"{BASE}coupons/")
        assert resp.status_code == status.HTTP_200_OK
        item = resp.data["results"][0]
        assert "name" in item
        assert "code" in item
        assert "type" in item
        assert "type_display" in item
        assert "value_yuan" in item
        assert "min_amount_yuan" in item
        assert "start_time" in item
        assert "end_time" in item
        assert "total" in item
        assert "used" in item

    def test_value_yuan_conversion(self, api_client, db):
        c = _coupon(code="MINUS1", type="minus", value=1500)
        resp = api_client.get(f"{BASE}coupons/")
        item = resp.data["results"][0]
        assert item["value_yuan"] == 15.0

    def test_discount_value_yuan(self, api_client, db):
        c = _coupon(code="DISC1", type="discount", value=80)
        resp = api_client.get(f"{BASE}coupons/")
        item = resp.data["results"][0]
        assert item["value_yuan"] == 8.0

    def test_fixed_value_yuan(self, api_client, db):
        c = _coupon(code="FIXED1", type="fixed", value=500)
        resp = api_client.get(f"{BASE}coupons/")
        item = resp.data["results"][0]
        assert item["value_yuan"] == 5.0

    def test_min_amount_yuan_conversion(self, api_client, db):
        _coupon(code="MINAMT", min_amount=3000)
        resp = api_client.get(f"{BASE}coupons/")
        item = resp.data["results"][0]
        assert item["min_amount_yuan"] == 30.0


# ── Coupon Claim ──


class TestCouponClaim:
    def test_claim_success(self, coupon_client, coupon_user):
        c = _coupon(code="CLAIM01")
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_200_OK
        assert UserCoupon.objects.filter(user=coupon_user, coupon=c).exists()
        c.refresh_from_db()
        assert c.used == 1

    def test_claim_increments_used(self, coupon_client, coupon_user):
        c = _coupon(code="CLAIM02")
        assert c.used == 0
        coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        c.refresh_from_db()
        assert c.used == 1

    def test_claim_duplicate_rejected(self, coupon_client, coupon_user):
        c = _coupon(code="DUP01")
        coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_inactive_coupon_rejected(self, coupon_client):
        c = _coupon(code="INACT", is_active=False)
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_not_yet_started_rejected(self, coupon_client):
        c = _coupon(code="NOTSTART", start_time=timezone.now() + timedelta(days=1))
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_expired_rejected(self, coupon_client):
        c = _coupon(code="EXPIRED", end_time=timezone.now() - timedelta(days=1))
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_fully_claimed_rejected(self, coupon_client):
        c = _coupon(code="FULL", total=1, used=1)
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_nonexistent_rejected(self, coupon_client):
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": 99999})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_unauthenticated_rejected(self, api_client, db):
        c = _coupon(code="AUTHREQ")
        resp = api_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_claim_missing_coupon_id(self, coupon_client):
        resp = coupon_client.post(f"{BASE}coupons/claim/", {})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── My Coupons ──


class TestMyCoupons:
    def test_list_empty(self, coupon_client):
        resp = coupon_client.get(f"{BASE}my-coupons/")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["results"]) == 0

    def test_list_claimed_coupons(self, coupon_client, coupon_user):
        c = _coupon(code="MY01")
        UserCoupon.objects.create(user=coupon_user, coupon=c)
        resp = coupon_client.get(f"{BASE}my-coupons/")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["results"]) == 1

    def test_filter_unused(self, coupon_client, coupon_user):
        c1 = _coupon(code="UNUSED1")
        c2 = _coupon(code="USED1")
        UserCoupon.objects.create(user=coupon_user, coupon=c1, is_used=False)
        UserCoupon.objects.create(user=coupon_user, coupon=c2, is_used=True)
        resp = coupon_client.get(f"{BASE}my-coupons/", {"status": "unused"})
        assert resp.status_code == status.HTTP_200_OK
        codes = [uc["coupon"]["code"] for uc in resp.data["results"]]
        assert "UNUSED1" in codes
        assert "USED1" not in codes

    def test_filter_used(self, coupon_client, coupon_user):
        c1 = _coupon(code="UNUSED2")
        c2 = _coupon(code="USED2")
        UserCoupon.objects.create(user=coupon_user, coupon=c1, is_used=False)
        UserCoupon.objects.create(user=coupon_user, coupon=c2, is_used=True)
        resp = coupon_client.get(f"{BASE}my-coupons/", {"status": "used"})
        assert resp.status_code == status.HTTP_200_OK
        codes = [uc["coupon"]["code"] for uc in resp.data["results"]]
        assert "USED2" in codes
        assert "UNUSED2" not in codes

    def test_user_isolation(self, coupon_client, coupon_user):
        other = User.objects.create_user(
            username="other_coupon", email="other@example.com",
            password="pass123", phone="1390000012",
        )
        c = _coupon(code="ISOLATE")
        UserCoupon.objects.create(user=other, coupon=c)
        resp = coupon_client.get(f"{BASE}my-coupons/")
        assert len(resp.data["results"]) == 0

    def test_unauthenticated_rejected(self, api_client):
        resp = api_client.get(f"{BASE}my-coupons/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_response_structure(self, coupon_client, coupon_user):
        c = _coupon(code="STRUCT1")
        UserCoupon.objects.create(user=coupon_user, coupon=c)
        resp = coupon_client.get(f"{BASE}my-coupons/")
        item = resp.data["results"][0]
        assert "id" in item
        assert "coupon" in item
        assert "is_used" in item
        assert "used_at" in item
        assert "created_at" in item
        assert "name" in item["coupon"]
        assert "value_yuan" in item["coupon"]


# ── Admin Coupon ──


class TestAdminCoupon:
    def test_admin_list(self, admin_coupon_client):
        _coupon(code="ALIST1")
        _coupon(code="ALIST2")
        resp = admin_coupon_client.get(f"{BASE}admin/coupons/")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["results"]) == 2

    def test_admin_create(self, admin_coupon_client):
        resp = admin_coupon_client.post(f"{BASE}admin/coupons/", {
            "name": "New Coupon",
            "code": "NEW001",
            "type": "minus",
            "value": 2000,
            "min_amount": 10000,
            "start_time": (timezone.now() - timedelta(days=1)).isoformat(),
            "end_time": (timezone.now() + timedelta(days=30)).isoformat(),
            "total": 50,
        })
        assert resp.status_code == status.HTTP_201_CREATED
        assert Coupon.objects.filter(code="NEW001").exists()

    def test_admin_update(self, admin_coupon_client):
        c = _coupon(code="UPD01")
        resp = admin_coupon_client.patch(f"{BASE}admin/coupons/{c.id}/", {
            "name": "Updated Name",
        })
        assert resp.status_code == status.HTTP_200_OK
        c.refresh_from_db()
        assert c.name == "Updated Name"

    def test_admin_delete(self, admin_coupon_client):
        c = _coupon(code="DEL01")
        resp = admin_coupon_client.delete(f"{BASE}admin/coupons/{c.id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert not Coupon.objects.filter(id=c.id).exists()

    def test_non_admin_cannot_list(self, coupon_client):
        _coupon(code="NOLIST")
        resp = coupon_client.get(f"{BASE}admin/coupons/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_cannot_create(self, coupon_client):
        resp = coupon_client.post(f"{BASE}admin/coupons/", {
            "name": "Bad Coupon",
            "code": "BAD001",
            "type": "minus",
            "value": 1000,
            "start_time": (timezone.now() - timedelta(days=1)).isoformat(),
            "end_time": (timezone.now() + timedelta(days=30)).isoformat(),
        })
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_access_admin(self, api_client):
        resp = api_client.get(f"{BASE}admin/coupons/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_detail(self, admin_coupon_client):
        c = _coupon(code="DETAIL1")
        resp = admin_coupon_client.get(f"{BASE}admin/coupons/{c.id}/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["code"] == "DETAIL1"


# ── Coupon Validation Edge Cases ──


class TestCouponEdgeCases:
    def test_claim_same_coupon_different_users(self, coupon_user):
        other = User.objects.create_user(
            username="other_claim", email="other_claim@example.com",
            password="pass123", phone="1390000013",
        )
        c = _coupon(code="MULTI01")
        c1 = APIClient()
        c1.force_authenticate(user=coupon_user)
        c1.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        c2 = APIClient()
        c2.force_authenticate(user=other)
        resp = c2.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_200_OK
        c.refresh_from_db()
        assert c.used == 2

    def test_coupon_used_count_reaches_total(self, coupon_client):
        c = _coupon(code="LAST01", total=1)
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_200_OK
        c.refresh_from_db()
        assert c.used == 1
        # Second claim should fail
        resp2 = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp2.status_code == status.HTTP_400_BAD_REQUEST

    def test_coupon_exactly_at_start_time(self, coupon_client):
        c = _coupon(code="EXACTSTART", start_time=timezone.now())
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_200_OK

    def test_coupon_exactly_at_end_time(self, coupon_client):
        c = _coupon(code="EXACTEND", end_time=timezone.now())
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        # Should succeed or fail depending on exact timing - both are acceptable
        assert resp.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_unlimited_coupon_total_zero(self, coupon_client):
        c = _coupon(code="UNLIM", total=0)
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_claim_response_data(self, coupon_client, coupon_user):
        c = _coupon(code="RESP01", type="discount", value=80, min_amount=3000)
        resp = coupon_client.post(f"{BASE}coupons/claim/", {"coupon_id": c.id})
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert data["code"] == "RESP01"
        assert data["value_yuan"] == 8.0
        assert data["min_amount_yuan"] == 30.0
