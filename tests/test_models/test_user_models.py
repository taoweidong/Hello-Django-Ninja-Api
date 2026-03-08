"""
用户模型测试
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

from src.infrastructure.persistence.models.user_models import UserProfile  # noqa: E402


class TestUserModel:
    """用户模型测试"""

    @pytest.mark.django_db
    def test_create_user_success(self, user_data):
        """测试创建用户成功"""
        user = User.objects.create_user(**user_data)
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.check_password(user_data["password"])
        assert not user.is_staff
        assert not user.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_success(self, admin_user_data):
        """测试创建超级用户成功"""
        user = User.objects.create_superuser(**admin_user_data)
        assert user.username == admin_user_data["username"]
        assert user.is_staff
        assert user.is_superuser

    @pytest.mark.django_db
    def test_create_user_without_email(self):
        """测试创建无邮箱用户"""
        user = User.objects.create_user(username="noemail", password="testpass123")
        assert user.email == ""

    @pytest.mark.django_db
    def test_user_str_representation(self, user_data):
        """测试用户字符串表示"""
        user = User.objects.create_user(**user_data)
        assert str(user) == user.username


class TestUserProfileModel:
    """用户档案模型测试"""

    @pytest.mark.django_db
    def test_create_profile(self, user_data):
        """测试创建用户档案"""
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, nickname="测试昵称", bio="测试简介")
        assert profile.user == user
        assert profile.nickname == "测试昵称"
        assert profile.bio == "测试简介"

    @pytest.mark.django_db
    def test_profile_auto_create_on_user_creation(self, user_data):
        """测试用户创建时自动创建档案"""
        user = User.objects.create_user(**user_data)
        assert hasattr(user, "profile")
        assert user.profile is not None

    @pytest.mark.django_db
    def test_profile_str_representation(self, user_data):
        """测试档案字符串表示"""
        user = User.objects.create_user(**user_data)
        profile = user.profile
        assert str(profile) == f"{user.username}的档案"
