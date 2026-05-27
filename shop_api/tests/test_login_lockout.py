import pytest
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db
class TestLoginLockout:
    def _login(self, api_client, username="testuser", password="wrong"):
        return api_client.post(
            "/api/v1/auth/login/",
            {"username": username, "password": password},
            format="json",
        )

    def test_success_login_not_locked(self, api_client, test_user):
        resp = self._login(api_client, username="testuser", password="testpass123")
        assert resp.status_code == status.HTTP_200_OK

    def test_lockout_after_5_failures(self, api_client, test_user):
        for _ in range(5):
            self._login(api_client)
        resp = self._login(api_client)
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "锁定" in resp.data["message"]

    def test_locked_returns_429(self, api_client, test_user):
        for _ in range(5):
            self._login(api_client)
        resp = self._login(api_client)
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_success_resets_fail_counter(self, api_client, test_user):
        for _ in range(4):
            self._login(api_client)
        # Successful login resets counter
        self._login(api_client, username="testuser", password="testpass123")
        # Next failure should not be locked (counter was reset)
        resp = self._login(api_client)
        assert resp.status_code != status.HTTP_429_TOO_MANY_REQUESTS

    def test_different_users_independent_lockout(self, api_client, test_user, db):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user2 = User.objects.create_user(
            username="lockout_user2",
            email="lock2@example.com",
            password="pass1234",
            phone="13900000002",
        )
        # Lock user 1
        for _ in range(5):
            self._login(api_client, username="testuser")
        resp = self._login(api_client, username="testuser")
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS

        # User 2 should not be locked
        resp = self._login(api_client, username="lockout_user2", password="pass1234")
        assert resp.status_code == status.HTTP_200_OK

    def test_lockout_message_is_friendly(self, api_client, test_user):
        for _ in range(5):
            self._login(api_client)
        resp = self._login(api_client)
        assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "message" in resp.data
        assert "锁定" in resp.data["message"]
