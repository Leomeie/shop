from __future__ import annotations

import io
import json
import random
import zipfile

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from PIL import Image, ImageDraw, ImageFont

from apps.orders.models import Order, OrderItem
from apps.products.models import Category, Product, ProductImage, SKU
from apps.users.models import User
from common.utils import generate_order_no


PRODUCT_SEEDS = [
    {
        "name": "Prompt Bundle Pro",
        "category": "Prompt",
        "description": "A premium prompt pack for marketing copy, image prompts, role setup, and structured AI outputs.",
        "version": "1.2.0",
        "changelog": "Added brand campaign prompts and multilingual prompt examples.",
        "status": "active",
        "is_featured": True,
        "download_count": 321,
        "view_count": 1840,
        "skus": [
            {"name": "Personal License", "price": 6900, "original_price": 8900, "license_description": "For personal creator projects."},
            {"name": "Commercial License", "price": 9900, "original_price": 12900, "license_description": "For client and brand delivery."},
        ],
        "accent": ("#F5E8D4", "#C89A53", "#1A2236"),
    },
    {
        "name": "ComfyUI Workflow Kit",
        "category": "Workflow",
        "description": "Production-ready ComfyUI workflows for poster generation, character consistency, and social campaign assets.",
        "version": "2.0.1",
        "changelog": "Refined poster and portrait workflows for SDXL pipelines.",
        "status": "active",
        "is_featured": True,
        "download_count": 211,
        "view_count": 1290,
        "skus": [
            {"name": "Starter", "price": 7900, "original_price": 9900, "license_description": "3 curated workflows."},
            {"name": "Studio", "price": 13900, "original_price": 16900, "license_description": "Full workflow library with docs."},
        ],
        "accent": ("#E8EEF8", "#5E7FCB", "#101828"),
    },
    {
        "name": "Lora Style Vault",
        "category": "LoRA",
        "description": "A curated collection of LoRA models for editorial portraits, product shots, and premium poster styles.",
        "version": "1.0.5",
        "changelog": "Added three new editorial lighting styles.",
        "status": "active",
        "is_featured": False,
        "download_count": 156,
        "view_count": 972,
        "skus": [
            {"name": "Creator Pack", "price": 8800, "original_price": 10800, "license_description": "For solo creators."},
            {"name": "Agency Pack", "price": 15800, "original_price": 19800, "license_description": "For team and agency use."},
        ],
        "accent": ("#EDE7F7", "#8C66D9", "#141627"),
    },
    {
        "name": "Design Delivery Assets",
        "category": "Design Assets",
        "description": "Presentation covers, social cards, and campaign mock assets designed for premium digital delivery.",
        "version": "3.1.0",
        "changelog": "New slide cover set and export-ready layouts.",
        "status": "active",
        "is_featured": True,
        "download_count": 97,
        "view_count": 680,
        "skus": [
            {"name": "Template Pack", "price": 5900, "original_price": 7900, "license_description": "Editable layout templates."},
            {"name": "Delivery Pack", "price": 10800, "original_price": 13800, "license_description": "Templates plus export assets."},
        ],
        "accent": ("#F7EDE4", "#B67A44", "#182235"),
    },
    {
        "name": "AI Brand Launch Pack",
        "category": "Prompt",
        "description": "A launch-ready pack containing prompts, visual directions, and content blocks for AI-native brand campaigns.",
        "version": "1.0.0",
        "changelog": "Initial release.",
        "status": "draft",
        "is_featured": False,
        "download_count": 0,
        "view_count": 143,
        "skus": [
            {"name": "Launch Set", "price": 12800, "original_price": 14800, "license_description": "Launch prompt framework."},
        ],
        "accent": ("#F3E9E7", "#C76D63", "#182235"),
    },
]


class Command(BaseCommand):
    help = "Generate demo products, preview images, downloadable assets, and a sample order/user for local development."

    def handle(self, *args, **options):
        random.seed(7)

        categories = self._ensure_categories()
        products = []
        for index, seed in enumerate(PRODUCT_SEEDS, start=1):
            product = self._create_or_update_product(seed, categories[seed["category"]], index)
            products.append(product)

        self._ensure_sample_user_and_order(products[:2])
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(products)} demo products with assets."))

    def _ensure_categories(self):
        categories = {}
        names = ["Prompt", "Workflow", "LoRA", "Design Assets"]
        for index, name in enumerate(names):
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"sort_order": index, "level": 1, "is_active": True},
            )
            category.sort_order = index
            category.level = 1
            category.is_active = True
            category.save(update_fields=["sort_order", "level", "is_active"])
            categories[name] = category
        return categories

    def _create_or_update_product(self, seed, category, index):
        product, _ = Product.objects.get_or_create(
            name=seed["name"],
            defaults={
                "category": category,
                "description": seed["description"],
                "version": seed["version"],
                "changelog": seed["changelog"],
                "status": seed["status"],
                "is_featured": seed["is_featured"],
                "download_count": seed["download_count"],
                "view_count": seed["view_count"],
            },
        )

        product.category = category
        product.description = seed["description"]
        product.version = seed["version"]
        product.changelog = seed["changelog"]
        product.status = seed["status"]
        product.is_featured = seed["is_featured"]
        product.download_count = seed["download_count"]
        product.view_count = seed["view_count"]

        if not product.main_image:
            product.main_image.save(
                f"seed-{index}-cover.png",
                ContentFile(self._generate_cover(seed["name"], seed["category"], seed["accent"])),
                save=False,
            )

        if not product.file:
            product.file.save(
                f"seed-{index}-bundle.zip",
                ContentFile(self._generate_bundle(seed)),
                save=False,
            )

        if not product.demo_file:
            demo_bytes = self._generate_demo_file(seed)
            product.demo_file.save(
                f"seed-{index}-demo.txt",
                ContentFile(demo_bytes),
                save=False,
            )

        product.save()
        self._sync_preview_images(product, seed, index)
        self._sync_skus(product, seed["skus"])
        return product

    def _sync_preview_images(self, product: Product, seed: dict, index: int):
        existing_count = product.images.count()
        for preview_index in range(existing_count, 2):
            image = ProductImage(product=product, sort_order=preview_index)
            image.image.save(
                f"seed-{index}-preview-{preview_index + 1}.png",
                ContentFile(self._generate_preview(seed["name"], seed["accent"], preview_index)),
                save=False,
            )
            image.save()

    def _sync_skus(self, product: Product, sku_seeds: list[dict]):
        existing = {sku.name: sku for sku in product.skus.all()}
        for sort_order, sku_seed in enumerate(sku_seeds):
            sku = existing.get(sku_seed["name"])
            if not sku:
                sku = SKU(product=product, name=sku_seed["name"])
            sku.price = sku_seed["price"]
            sku.original_price = sku_seed["original_price"]
            sku.license_description = sku_seed["license_description"]
            sku.sort_order = sort_order
            sku.is_active = True
            sku.save()

    def _ensure_sample_user_and_order(self, products):
        user, created = User.objects.get_or_create(
            username="creator_demo",
            defaults={
                "nickname": "Creator Demo",
                "phone": "13900000001",
                "email": "creator_demo@example.com",
                "is_active": True,
            },
        )
        if created:
            user.set_password("creator123")
            user.save(update_fields=["password"])

        if Order.objects.filter(user=user).exists():
            return

        order = Order.objects.create(
            order_no=generate_order_no(),
            user=user,
            total_amount=0,
            pay_amount=0,
            status="completed",
            remark="Seeded sample order",
            pay_time=timezone.now(),
            complete_time=timezone.now(),
        )

        total_amount = 0
        for product in products:
            sku = product.skus.filter(is_active=True).order_by("price").first()
            if not sku:
                continue
            OrderItem.objects.create(
                order=order,
                sku=sku,
                product_name=product.name,
                sku_name=sku.name,
                price=sku.price,
                download_count=random.randint(1, 6),
                download_token=f"seed-{product.id}-{sku.id}",
            )
            total_amount += sku.price

        order.total_amount = total_amount
        order.pay_amount = total_amount
        order.save(update_fields=["total_amount", "pay_amount"])

    def _generate_cover(self, title: str, category: str, accent: tuple[str, str, str]) -> bytes:
        width, height = 1600, 900
        image = Image.new("RGB", (width, height), accent[0])
        draw = ImageDraw.Draw(image)
        dark = accent[2]
        gold = accent[1]

        for i in range(6):
            opacity_width = width - i * 120
            opacity_height = height - i * 90
            draw.rounded_rectangle(
                [(80 + i * 18, 80 + i * 18), (80 + opacity_width, 80 + opacity_height)],
                radius=48,
                outline=gold,
                width=2,
            )

        title_font = ImageFont.truetype("arial.ttf", 92) if self._font_available("arial.ttf") else ImageFont.load_default()
        subtitle_font = ImageFont.truetype("arial.ttf", 34) if self._font_available("arial.ttf") else ImageFont.load_default()
        label_font = ImageFont.truetype("arial.ttf", 26) if self._font_available("arial.ttf") else ImageFont.load_default()

        draw.text((120, 120), "SHOP EASE", fill=gold, font=label_font)
        draw.text((120, 220), title, fill=dark, font=title_font)
        draw.text((120, 360), category.upper(), fill=gold, font=subtitle_font)
        draw.text((120, 430), "Premium AI-native digital asset", fill=dark, font=subtitle_font)
        draw.rounded_rectangle([(120, 660), (520, 760)], radius=28, fill=dark)
        draw.text((168, 694), "READY TO SELL", fill="#ffffff", font=subtitle_font)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    def _generate_preview(self, title: str, accent: tuple[str, str, str], index: int) -> bytes:
        width, height = 1280, 720
        image = Image.new("RGB", (width, height), "#ffffff")
        draw = ImageDraw.Draw(image)
        dark = accent[2]
        gold = accent[1]

        draw.rectangle([(0, 0), (width, height)], fill=accent[0])
        draw.rounded_rectangle([(80, 80), (width - 80, height - 80)], radius=40, outline=dark, width=3)
        draw.rounded_rectangle([(120, 120), (width - 120, 280)], radius=28, fill="#ffffff")
        draw.rounded_rectangle([(120, 320), (width - 120, 600)], radius=28, fill=gold)

        title_font = ImageFont.truetype("arial.ttf", 64) if self._font_available("arial.ttf") else ImageFont.load_default()
        subtitle_font = ImageFont.truetype("arial.ttf", 28) if self._font_available("arial.ttf") else ImageFont.load_default()

        draw.text((160, 150), title, fill=dark, font=title_font)
        draw.text((160, 220), f"Preview panel {index + 1}", fill=dark, font=subtitle_font)
        draw.text((160, 380), "Includes prompts, workflow files, docs, and premium delivery assets.", fill="#ffffff", font=subtitle_font)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    def _generate_bundle(self, seed: dict) -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "README.txt",
                f"{seed['name']}\n\nDescription:\n{seed['description']}\n\nVersion: {seed['version']}\n",
            )
            archive.writestr(
                "metadata.json",
                json.dumps(
                    {
                        "name": seed["name"],
                        "category": seed["category"],
                        "version": seed["version"],
                        "featured": seed["is_featured"],
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
            )
            archive.writestr(
                "assets/example-prompts.txt",
                "\n".join(
                    [
                        "Prompt 01: Build an editorial poster layout with premium spacing.",
                        "Prompt 02: Create a product hero visual using a light-luxury palette.",
                        "Prompt 03: Produce an AI workflow sequence for social asset delivery.",
                    ]
                ),
            )
        return buffer.getvalue()

    def _generate_demo_file(self, seed: dict) -> bytes:
        content = "\n".join(
            [
                seed["name"],
                "",
                "Demo Overview",
                f"Category: {seed['category']}",
                f"Version: {seed['version']}",
                "",
                "This demo file is generated for local development and admin preview.",
            ]
        )
        return content.encode("utf-8")

    @staticmethod
    def _font_available(font_name: str) -> bool:
        try:
            ImageFont.truetype(font_name, 16)
            return True
        except OSError:
            return False
