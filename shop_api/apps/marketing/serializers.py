from django.utils import timezone
from rest_framework import serializers
from .models import Coupon, UserCoupon


class CouponSerializer(serializers.ModelSerializer):
    value_yuan = serializers.SerializerMethodField()
    min_amount_yuan = serializers.SerializerMethodField()
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = Coupon
        fields = ["id", "name", "code", "type", "type_display",
                  "value", "value_yuan", "min_amount", "min_amount_yuan",
                  "start_time", "end_time", "total", "used"]

    def get_value_yuan(self, obj):
        if obj.type == "discount":
            return obj.value / 10  # 80 → 8折
        return obj.value / 100

    def get_min_amount_yuan(self, obj):
        return obj.min_amount / 100


class UserCouponSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = UserCoupon
        fields = ["id", "coupon", "is_used", "used_at", "created_at"]


class CouponClaimSerializer(serializers.Serializer):
    coupon_id = serializers.IntegerField()

    def validate_coupon_id(self, value):
        now = timezone.now()
        coupon = Coupon.objects.filter(id=value, is_active=True).first()
        if not coupon:
            raise serializers.ValidationError("优惠券不存在")
        if coupon.start_time > now:
            raise serializers.ValidationError("优惠券尚未开始")
        if coupon.end_time < now:
            raise serializers.ValidationError("优惠券已过期")
        if coupon.used >= coupon.total:
            raise serializers.ValidationError("优惠券已领完")
        return value

    def validate(self, data):
        user = self.context["request"].user
        coupon_id = data["coupon_id"]
        if UserCoupon.objects.filter(user=user, coupon_id=coupon_id).exists():
            raise serializers.ValidationError("您已领取过该优惠券")
        return data

    def save(self):
        user = self.context["request"].user
        coupon_id = self.validated_data["coupon_id"]
        coupon = Coupon.objects.get(id=coupon_id)
        UserCoupon.objects.create(user=user, coupon=coupon)
        coupon.used += 1
        coupon.save(update_fields=["used"])
        return coupon
