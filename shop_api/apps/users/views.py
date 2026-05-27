from django.core.cache import cache
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from common.response import success, error

LOGIN_FAIL_LIMIT = 5
LOGIN_LOCKOUT_SECONDS = 15 * 60  # 15 minutes


def _fail_cache_key(identifier):
    return f"login_fail_{identifier}"


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return success({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, code=201)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("username", "").strip().lower()

        # Check lockout
        lock_key = f"login_lock_{identifier}"
        if cache.get(lock_key):
            return error("账号已锁定，请稍后再试", code=429)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            # Track failed attempt
            fail_key = _fail_cache_key(identifier)
            fails = cache.get(fail_key, 0) + 1
            if fails >= LOGIN_FAIL_LIMIT:
                cache.set(lock_key, True, LOGIN_LOCKOUT_SECONDS)
                cache.delete(fail_key)
                return error("账号已锁定，请稍后再试", code=429)
            cache.set(fail_key, fails, LOGIN_LOCKOUT_SECONDS)
            raise

        # Success — reset fail counter
        cache.delete(_fail_cache_key(identifier))

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return success({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
