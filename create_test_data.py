#!/usr/bin/env python
"""测试脚本 - 创建初始测试数据"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from src.infrastructure.persistence.models.system_models import (
    SystemDeptInfo,
    SystemMenu,
    SystemMenuMeta,
    SystemUserRole,
    SystemUserInfoRoles,
)
from src.infrastructure.persistence.models.user_models import User


async def create_test_data():
    """创建测试数据"""
    print("创建测试数据...")

    # 创建用户
    user, _ = await User.objects.aupdate_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "is_superuser": True,
            "is_active": True,
        },
    )

    # 创建部门
    dept, _ = await SystemDeptInfo.objects.aupdate_or_create(
        code="root_dept",
        defaults={
            "name": "根部门",
            "rank": 1,
            "is_active": True,
        },
    )

    # 创建菜单元数据
    meta, _ = await SystemMenuMeta.objects.aupdate_or_create(
        id="meta_dashboard",
        defaults={
            "title": "仪表盘",
            "icon": "dashboard",
            "is_show_menu": True,
        },
    )

    # 创建菜单
    menu, _ = await SystemMenu.objects.aupdate_or_create(
        name="dashboard",
        defaults={
            "menu_type": 1,  # 菜单
            "path": "/dashboard",
            "component": "Dashboard/index",
            "rank": 1,
            "is_active": True,
            "meta": meta,
        },
    )

    # 创建角色
    role, _ = await SystemUserRole.objects.aupdate_or_create(
        code="admin_role",
        defaults={
            "name": "管理员",
            "is_active": True,
        },
    )

    # 为角色分配菜单
    await role.menus.aadd(menu)

    # 为用户分配角色
    await SystemUserInfoRoles.objects.aupdate_or_create(
        userinfo=user,
        userrole=role,
    )

    print("✅ 测试数据创建成功！")
    print(f"用户: {user.username}")
    print(f"部门: {dept.name}")
    print(f"菜单: {menu.name}")
    print(f"角色: {role.name}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_test_data())
