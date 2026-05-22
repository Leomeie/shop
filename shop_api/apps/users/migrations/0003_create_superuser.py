from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model("users", "User")
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123456",
        )


def reverse(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(username="admin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_downloadlog_delete_address"),
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse),
    ]
