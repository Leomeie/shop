import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            phone="13800000001",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")
        assert user.phone == "13800000001"

    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username="testadmin",
            email="testadmin@example.com",
            password="adminpass123",
            phone="13800000002",
        )
        assert admin.is_staff
        assert admin.is_superuser


@pytest.mark.django_db
class TestRegister:
    URL = "/api/v1/auth/register/"

    def test_register_success(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "newuser",
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.data["data"]
        assert "user" in data
        assert "access" in data
        assert "refresh" in data
        assert data["user"]["username"] == "newuser"
        assert get_user_model().objects.filter(username="newuser").exists()

    def test_register_duplicate_username(self, api_client, test_user):
        resp = api_client.post(self.URL, {
            "username": "testuser",
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "用户名已存在" in str(resp.data)

    def test_register_password_too_short(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "shortpwd",
            "password": "ab1",
            "password_confirm": "ab1",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_no_letter(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "numbersonly",
            "password": "123456",
            "password_confirm": "123456",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "字母" in str(resp.data)

    def test_register_password_no_digit(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "lettersonly",
            "password": "abcdef",
            "password_confirm": "abcdef",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "数字" in str(resp.data)

    def test_register_missing_username(self, api_client):
        resp = api_client.post(self.URL, {
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_password(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "nopwd",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_password_confirm(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "noconfirm",
            "password": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "mismatch",
            "password": "pass1234",
            "password_confirm": "pass5678",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "不一致" in str(resp.data)

    def test_register_invalid_username_special_chars(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "user@#$",
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_username_pure_digits(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "12345",
            "password": "pass1234",
            "password_confirm": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "纯数字" in str(resp.data)


@pytest.mark.django_db
class TestLogin:
    URL = "/api/v1/auth/login/"

    def test_login_success(self, api_client, test_user):
        resp = api_client.post(self.URL, {
            "username": "testuser",
            "password": "testpass123",
        })
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["data"]
        assert "user" in data
        assert "access" in data
        assert "refresh" in data
        assert data["user"]["username"] == "testuser"

    def test_login_wrong_password(self, api_client, test_user):
        resp = api_client.post(self.URL, {
            "username": "testuser",
            "password": "wrongpass",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "用户名或密码错误" in str(resp.data)

    def test_login_nonexistent_user(self, api_client):
        resp = api_client.post(self.URL, {
            "username": "ghost",
            "password": "pass1234",
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "用户名或密码错误" in str(resp.data)

    def test_login_missing_fields(self, api_client):
        resp = api_client.post(self.URL, {})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestJWTAuth:
    REFRESH_URL = "/api/v1/auth/token/refresh/"

    def test_refresh_token_success(self, api_client, test_user):
        refresh = RefreshToken.for_user(test_user)
        resp = api_client.post(self.REFRESH_URL, {"refresh": str(refresh)})
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data

    def test_refresh_token_invalid(self, api_client):
        resp = api_client.post(self.REFRESH_URL, {"refresh": "invalid.token.here"})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_me_requires_auth(self, api_client):
        resp = api_client.get("/api/v1/auth/me/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_me_authenticated(self, auth_client):
        resp = auth_client.get("/api/v1/auth/me/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["username"] == "testuser"


@pytest.mark.django_db
class TestGuestAccess:
    def test_guest_can_browse_products(self, api_client):
        resp = api_client.get("/api/v1/products/")
        assert resp.status_code == status.HTTP_200_OK

    def test_unauthenticated_cannot_create_order(self, api_client):
        resp = api_client.post("/api/v1/orders/create/", {})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthenticated_cannot_access_cart(self, api_client):
        resp = api_client.get("/api/v1/cart/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
