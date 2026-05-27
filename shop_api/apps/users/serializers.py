import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.Serializer):
    """用户注册序列化器。"""
    username = serializers.CharField(
        min_length=3,
        max_length=20,
        trim_whitespace=True,
        help_text="用户名，3-20个字符，仅支持字母、数字和下划线",
        error_messages={
            "required": "请输入用户名",
            "blank": "用户名不能为空",
            "min_length": "用户名至少需要 3 个字符",
            "max_length": "用户名不能超过 20 个字符",
        },
    )
    password = serializers.CharField(
        min_length=6,
        max_length=20,
        trim_whitespace=False,
        write_only=True,
        help_text="密码，6-20个字符，须包含字母和数字",
        error_messages={
            "required": "请输入密码",
            "blank": "密码不能为空",
            "min_length": "密码至少需要 6 个字符",
            "max_length": "密码不能超过 20 个字符",
        },
    )
    password_confirm = serializers.CharField(
        min_length=6,
        max_length=20,
        trim_whitespace=False,
        write_only=True,
        help_text="确认密码，须与密码一致",
        error_messages={
            "required": "请再次输入密码",
            "blank": "确认密码不能为空",
            "min_length": "确认密码至少需要 6 个字符",
            "max_length": "确认密码不能超过 20 个字符",
        },
    )

    def validate_username(self, value):
        value = value.strip()
        if not re.fullmatch(r"[A-Za-z0-9_]+", value):
            raise serializers.ValidationError("用户名只能包含字母、数字或下划线")
        if value.isdigit():
            raise serializers.ValidationError("用户名不能为纯数字")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("该用户名已存在，请更换一个新的用户名")
        return value

    def validate_password(self, value):
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("密码必须包含至少一个字母")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("密码必须包含至少一个数字")
        return value

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "两次输入的密码不一致"})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """用户登录序列化器。"""
    username = serializers.CharField(
        trim_whitespace=True,
        help_text="用户名或邮箱",
        error_messages={
            "required": "请输入用户名",
            "blank": "用户名不能为空",
        },
    )
    password = serializers.CharField(
        trim_whitespace=False,
        help_text="密码",
        error_messages={
            "required": "请输入密码",
            "blank": "密码不能为空",
        },
    )

    def validate(self, data):
        username = data["username"].strip()
        password = data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"non_field_errors": ["用户名或密码错误，请检查后重试"]})
        if not user.is_active:
            raise serializers.ValidationError({"non_field_errors": ["账号已被禁用，请联系管理员"]})
        data["user"] = user
        data["username"] = username
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "phone",
            "avatar",
            "date_joined",
            "is_staff",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = ["id", "username", "date_joined", "is_staff", "is_superuser", "is_active"]
