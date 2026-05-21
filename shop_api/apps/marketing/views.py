from django.utils import timezone
from rest_framework import generics, permissions
from .models import Coupon, UserCoupon
from .serializers import CouponSerializer, UserCouponSerializer, CouponClaimSerializer
from common.pagination import StandardPagination
from common.permissions import IsAdminUser
from common.response import success, error


class CouponListView(generics.ListAPIView):
    """Public: list available coupons."""
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(is_active=True, start_time__lte=now, end_time__gte=now)


class CouponClaimView(generics.GenericAPIView):
    """Claim a coupon."""
    serializer_class = CouponClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.save()
        return success(CouponSerializer(coupon).data)


class MyCouponListView(generics.ListAPIView):
    """List user's coupons."""
    serializer_class = UserCouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = UserCoupon.objects.filter(user=self.request.user).select_related("coupon")
        status = self.request.query_params.get("status")
        if status == "unused":
            qs = qs.filter(is_used=False)
        elif status == "used":
            qs = qs.filter(is_used=True)
        return qs


# ── Admin ──

class AdminCouponListCreateView(generics.ListCreateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination
    queryset = Coupon.objects.all()


class AdminCouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all()
