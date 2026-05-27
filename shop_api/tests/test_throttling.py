import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.throttling import SimpleRateThrottle

from common.throttles import PaymentRateThrottle

User = get_user_model()

LOW_RATES = {
    "anon": "2/min",
    "user": "2/min",
    "payment": "2/min",
}


@pytest.fixture(autouse=True)
def _throttle_test():
    """Temporarily set low throttle rates for testing."""
    original = SimpleRateThrottle.THROTTLE_RATES.copy()
    SimpleRateThrottle.THROTTLE_RATES = LOW_RATES
    cache.clear()
    yield
    SimpleRateThrottle.THROTTLE_RATES = original
    cache.clear()


@pytest.mark.django_db
class TestAnonThrottle:
    def test_first_request_succeeds(self, api_client):
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code != status.HTTP_429_TOO_MANY_REQUESTS

    def test_throttled_after_limit(self, api_client):
        for _ in range(3):
            api_client.get("/api/v1/products/")
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "message" in resp.data

    def test_throttle_response_has_detail(self, api_client):
        for _ in range(3):
            api_client.get("/api/v1/products/")
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "message" in resp.data


@pytest.mark.django_db
class TestUserThrottle:
    def test_first_request_succeeds(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code != status.HTTP_429_TOO_MANY_REQUESTS

    def test_throttled_after_limit(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        for _ in range(3):
            api_client.get("/api/v1/products/")
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_different_users_have_separate_limits(self, test_user, db):
        user2 = User.objects.create_user(
            username="throttle_user2",
            email="t2@example.com",
            password="pass1234",
            phone="13900000001",
        )
        c1 = APIClient()
        c1.force_authenticate(user=test_user)
        c2 = APIClient()
        c2.force_authenticate(user=user2)

        for _ in range(3):
            c1.get("/api/v1/products/")

        resp = c2.get("/api/v1/products/")
        assert resp.status_code != status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
class TestPaymentThrottle:
    def test_payment_throttle_applied(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        for _ in range(3):
            api_client.post("/api/v1/payment/create/", {"order_id": 99999}, format="json")
        resp = api_client.post("/api/v1/payment/create/", {"order_id": 99999}, format="json")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_payment_callback_throttled(self, api_client):
        for _ in range(3):
            api_client.post("/api/v1/payment/callback/", {"payment_no": "fake"}, format="json")
        resp = api_client.post("/api/v1/payment/callback/", {"payment_no": "fake"}, format="json")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
class TestThrottleConfig:
    def test_anon_rate_configured(self):
        from django.conf import settings
        rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        assert rates.get("anon") == "20/min"

    def test_user_rate_configured(self):
        from django.conf import settings
        rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        assert rates.get("user") == "60/min"

    def test_payment_rate_configured(self):
        from django.conf import settings
        rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        assert rates.get("payment") == "10/min"

    def test_throttle_classes_configured(self):
        from django.conf import settings
        classes = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_CLASSES", [])
        assert "rest_framework.throttling.AnonRateThrottle" in classes
        assert "rest_framework.throttling.UserRateThrottle" in classes
