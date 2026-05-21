from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "待支付"),
        ("paid", "已支付"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
    ]

    order_no = models.CharField("订单号", max_length=30, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name="用户")
    total_amount = models.IntegerField("总金额（分）", default=0)
    discount_amount = models.IntegerField("优惠金额（分）", default=0)
    pay_amount = models.IntegerField("应付金额（分）", default=0)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="pending")
    coupon = models.ForeignKey("marketing.Coupon", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="优惠券")
    pay_time = models.DateTimeField("支付时间", null=True, blank=True)
    complete_time = models.DateTimeField("完成时间", null=True, blank=True)
    remark = models.CharField("备注", max_length=200, blank=True)
    is_deleted = models.BooleanField("是否删除", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "orders"
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="订单")
    sku = models.ForeignKey("products.SKU", on_delete=models.SET_NULL, null=True, verbose_name="SKU")
    product_name = models.CharField("商品名称", max_length=200)
    sku_name = models.CharField("版本名称", max_length=50)
    price = models.IntegerField("单价（分）")
    download_count = models.IntegerField("下载次数", default=0)
    download_token = models.CharField("下载令牌", max_length=64, blank=True)

    class Meta:
        db_table = "order_items"
        verbose_name = "订单项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product_name} - {self.sku_name}"
