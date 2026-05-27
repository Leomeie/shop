from django.db import models
from django.conf import settings


class Payment(models.Model):
    """支付记录，关联订单，记录支付方式、流水号和状态。"""
    METHOD_CHOICES = [
        ("mock", "模拟支付"),
        ("alipay", "支付宝"),
        ("wechat", "微信支付"),
        ("stripe", "Stripe"),
    ]
    STATUS_CHOICES = [
        ("pending", "待支付"),
        ("success", "成功"),
        ("failed", "失败"),
    ]

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="payments", verbose_name="订单")
    payment_no = models.CharField("支付流水号", max_length=40, unique=True)
    amount = models.IntegerField("金额（分）")
    method = models.CharField("支付方式", max_length=10, choices=METHOD_CHOICES, default="mock")
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="pending")
    paid_at = models.DateTimeField("支付时间", null=True, blank=True)

    class Meta:
        db_table = "payments"
        verbose_name = "支付记录"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.payment_no
