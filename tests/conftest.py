"""
Pytest 配置文件
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def db_setup(django_db_setup, django_db_blocker):
    """数据库设置 fixture"""
    pass


@pytest.fixture
def user_data():
    """测试用户数据 fixture"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "phone": "13800138000",
    }


@pytest.fixture
def admin_user_data():
    """管理员用户数据 fixture"""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpass123",
        "phone": "13800138001",
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def role_data():
    """角色数据 fixture"""
    return {"name": "管理员", "code": "admin", "description": "系统管理员角色"}


@pytest.fixture
def permission_data():
    """权限数据 fixture"""
    return {"name": "用户查看", "code": "user:view", "resource": "user", "action": "view"}
