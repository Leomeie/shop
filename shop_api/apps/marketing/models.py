from django.db import models
from django.conf import settings


class Coupon(models.Model):
    """优惠券模板，定义类型（满减/折扣/固定金额）、面值、有效期和发行量。"""
    TYPE_CHOICES = [
        ("minus", "满减券"),
        ("discount", "折扣券"),
        ("fixed", "固定金额券"),
    ]

    name = models.CharField("优惠券名称", max_length=100)
    code = models.CharField("优惠码", max_length=30, unique=True)
    type = models.CharField("类型", max_length=10, choices=TYPE_CHOICES)
    value = models.IntegerField("面值/折扣（分或百分比）")
    min_amount = models.IntegerField("最低消费（分）", default=0)
    start_time = models.DateTimeField("开始时间")
    end_time = models.DateTimeField("结束时间")
    total = models.IntegerField("发行总量", default=0)
    used = models.IntegerField("已使用数量", default=0)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "coupons"
        verbose_name = "优惠券"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserCoupon(models.Model):
    """用户领取的优惠券实例，记录领取时间和使用状态。"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coupons", verbose_name="用户")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name="优惠券")
    is_used = models.BooleanField("是否已使用", default=False)
    used_at = models.DateTimeField("使用时间", null=True, blank=True)
    created_at = models.DateTimeField("领取时间", auto_now_add=True)

    class Meta:
        db_table = "user_coupons"
        verbose_name = "用户优惠券"
        verbose_name_plural = verbose_name
        unique_together = ["user", "coupon"]

    def __str__(self):
        return f"{self.user.username} - {self.coupon.name}"
