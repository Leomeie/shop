from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    phone = models.CharField("手机号", max_length=11, unique=True, null=True, blank=True)
    nickname = models.CharField("昵称", max_length=50, blank=True)
    avatar = models.ImageField("头像", upload_to="avatars/", blank=True)
    is_active = models.BooleanField("是否启用", default=True)

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class DownloadLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="download_logs", verbose_name="用户")
    order_item = models.ForeignKey("orders.OrderItem", on_delete=models.CASCADE, verbose_name="订单项")
    ip = models.GenericIPAddressField("IP地址", null=True, blank=True)
    user_agent = models.CharField("User-Agent", max_length=500, blank=True)
    downloaded_at = models.DateTimeField("下载时间", auto_now_add=True)

    class Meta:
        db_table = "download_logs"
        verbose_name = "下载记录"
        verbose_name_plural = verbose_name
        ordering = ["-downloaded_at"]

    def __str__(self):
        return f"{self.user.username} - {self.downloaded_at}"
