from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    if Category.objects.exists():
        return

    # 一级分类
    c1 = Category.objects.create(name="Prompt 模板", level=1, icon="icon-prompt", sort_order=0, is_active=True)
    c2 = Category.objects.create(name="ComfyUI 工作流", level=1, icon="icon-workflow", sort_order=1, is_active=True)
    c3 = Category.objects.create(name="LoRA 模型", level=1, icon="icon-lora", sort_order=2, is_active=True)
    c4 = Category.objects.create(name="设计素材", level=1, icon="icon-design", sort_order=3, is_active=True)

    # 二级分类
    Category.objects.create(name="营销文案", parent=c1, level=2, icon="icon-copy", sort_order=0, is_active=True)
    Category.objects.create(name="角色设定", parent=c1, level=2, icon="icon-character", sort_order=1, is_active=True)
    Category.objects.create(name="图像生成", parent=c2, level=2, icon="icon-image", sort_order=0, is_active=True)
    Category.objects.create(name="视频生成", parent=c2, level=2, icon="icon-video", sort_order=1, is_active=True)
    Category.objects.create(name="写实风格", parent=c3, level=2, icon="icon-realistic", sort_order=0, is_active=True)
    Category.objects.create(name="动漫风格", parent=c3, level=2, icon="icon-anime", sort_order=1, is_active=True)
    Category.objects.create(name="封面设计", parent=c4, level=2, icon="icon-cover", sort_order=0, is_active=True)
    Category.objects.create(name="海报设计", parent=c4, level=2, icon="icon-poster", sort_order=1, is_active=True)


def remove_categories(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]
