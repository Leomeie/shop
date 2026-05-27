from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class PaymentRateThrottle(UserRateThrottle):
    """Rate limit payment endpoints to 10/min for all users."""
    scope = "payment"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f"throttle_payment_{ident}"
