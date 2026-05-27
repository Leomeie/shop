"""
Run this script after installing drf-spectacular to enable API documentation.

Usage:
    pip install drf-spectacular
    python setup_spectacular.py
"""
import sys

BASE_SETTINGS = "config/settings/base.py"


def patch_settings():
    with open(BASE_SETTINGS, "r", encoding="utf-8") as f:
        content = f.read()

    changes = []

    # 1. Add drf_spectacular to INSTALLED_APPS
    if '"drf_spectacular"' not in content:
        content = content.replace(
            '"django_filters",',
            '"django_filters",\n    "drf_spectacular",',
        )
        changes.append("Added drf_spectacular to INSTALLED_APPS")

    # 2. Add DEFAULT_SCHEMA_CLASS to REST_FRAMEWORK
    if '"DEFAULT_SCHEMA_CLASS"' not in content:
        content = content.replace(
            '"DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",',
            '"DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",\n'
            '    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",',
        )
        changes.append("Added DEFAULT_SCHEMA_CLASS to REST_FRAMEWORK")

    # 3. Add SPECTACULAR_SETTINGS
    if "SPECTACULAR_SETTINGS" not in content:
        content = content.replace(
            "CORS_ALLOW_CREDENTIALS = True\n\n# Cache",
            "CORS_ALLOW_CREDENTIALS = True\n\n"
            "# drf-spectacular\n"
            "SPECTACULAR_SETTINGS = {\n"
            '    "TITLE": "ShopEase API",\n'
            '    "DESCRIPTION": "ShopEase 电商平台 API 文档",\n'
            '    "VERSION": "1.0.0",\n'
            '    "SERVE_INCLUDE_SCHEMA": False,\n'
            "}\n\n# Cache",
        )
        changes.append("Added SPECTACULAR_SETTINGS")

    if changes:
        with open(BASE_SETTINGS, "w", encoding="utf-8") as f:
            f.write(content)
        print("Settings updated:")
        for c in changes:
            print(f"  - {c}")
        print("\nAPI documentation available at:")
        print("  - Swagger UI: http://localhost:8000/api/docs/")
        print("  - Schema JSON: http://localhost:8000/api/schema/")
    else:
        print("Settings already configured.")


if __name__ == "__main__":
    patch_settings()
