from django.db import connection
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class HealthCheckView(APIView):
    """Health check endpoint for monitoring and load balancing."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        checks = {}

        # Database check
        try:
            connection.ensure_connection()
            checks["db"] = "ok"
        except Exception:
            checks["db"] = "error"

        # Cache check
        try:
            cache.set("_health_check", "ok", 5)
            val = cache.get("_health_check")
            checks["cache"] = "ok" if val == "ok" else "error"
        except Exception:
            checks["cache"] = "error"

        status_ok = all(v == "ok" for v in checks.values())
        checks["status"] = "ok" if status_ok else "error"

        http_status = 200 if status_ok else 503
        return Response(checks, status=http_status)
