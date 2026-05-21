from django.db import models


class Category(models.Model):
    """Product category (max 2 levels)."""

    name = models.CharField("分类名称", max_length=50)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="children", verbose_name="父分类",
    )
    level = models.PositiveSmallIntegerField("层级", default=1)
    icon = models.CharField("图标", max_length=50, blank=True)
    sort_order = models.IntegerField("排序", default=0)
    is_active = models.BooleanField("是否显示", default=True)

    class Meta:
        db_table = "categories"
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Digital product."""

    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("active", "上架"),
        ("inactive", "下架"),
    ]

    name = models.CharField("商品名称", max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products", verbose_name="分类",
    )
    description = models.TextField("商品描述", blank=True)
    main_image = models.ImageField("主图", upload_to="images/products/")
    file = models.FileField("商品文件", upload_to="products/files/")
    demo_file = models.FileField("Demo文件", upload_to="products/demo/", blank=True)
    version = models.CharField("版本号", max_length=20, default="1.0.0")
    changelog = models.TextField("更新日志", blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="draft")
    is_deleted = models.BooleanField("是否删除", default=False)
    is_featured = models.BooleanField("是否推荐", default=False)
    download_count = models.IntegerField("下载次数", default=0)
    view_count = models.IntegerField("浏览次数", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def min_price(self):
        skus = self.skus.filter(is_active=True)
        if skus.exists():
            return skus.order_by("price").first().price
        return 0


class ProductImage(models.Model):
    """Product preview images."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="商品")
    image = models.ImageField("图片", upload_to="images/products/")
    sort_order = models.IntegerField("排序", default=0)

    class Meta:
        db_table = "product_images"
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.product.name} - {self.sort_order}"


class SKU(models.Model):
    """Stock Keeping Unit — version/license tier for digital products."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus", verbose_name="商品")
    name = models.CharField("版本名称", max_length=50)
    price = models.IntegerField("价格（分）")
    original_price = models.IntegerField("原价（分）", default=0)
    license_description = models.CharField("授权说明", max_length=200, blank=True)
    sort_order = models.IntegerField("排序", default=0)
    is_active = models.BooleanField("是否启用", default=True)

    class Meta:
        db_table = "skus"
        verbose_name = "SKU"
        verbose_name_plural = verbose_name
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"
