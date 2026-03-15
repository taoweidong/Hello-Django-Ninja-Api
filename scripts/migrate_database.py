#!/usr/bin/env python
"""
数据库迁移和初始化脚本
将数据库从根目录移动到 sql 目录，并重新创建数据库结构
"""

import os
import shutil
import sys
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    print("=" * 60)
    print("数据库迁移和初始化脚本")
    print("=" * 60)

    # 1. 检查旧数据库文件
    old_db = BASE_DIR / "db.sqlite3"
    new_db_dir = BASE_DIR / "sql"
    new_db = new_db_dir / "db.sqlite3"

    # 2. 创建 sql 目录（如果不存在）
    new_db_dir.mkdir(exist_ok=True)
    print(f"\n[OK] SQL目录已就绪: {new_db_dir}")

    # 3. 移动旧数据库文件
    if old_db.exists():
        try:
            shutil.move(str(old_db), str(new_db))
            print(f"[OK] 数据库已移动: {old_db} -> {new_db}")
        except Exception as e:
            print(f"[警告] 无法移动数据库文件: {e}")
            print("  将创建新的数据库")
    else:
        print("[OK] 未找到旧数据库，将创建新数据库")

    # 4. 设置Django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

    # 必须在设置环境变量后导入Django
    import django

    django.setup()

    from django.contrib.auth import get_user_model
    from django.core.management import call_command

    # 5. 创建迁移文件
    print("\n" + "=" * 60)
    print("步骤 1: 创建迁移文件")
    print("=" * 60)
    try:
        call_command("makemigrations", verbosity=1)
        print("[OK] 迁移文件创建成功")
    except Exception as e:
        print(f"[警告] 创建迁移文件时出现警告: {e}")

    # 6. 应用迁移
    print("\n" + "=" * 60)
    print("步骤 2: 应用数据库迁移")
    print("=" * 60)
    try:
        call_command("migrate", verbosity=1)
        print("[OK] 数据库迁移成功")
    except Exception as e:
        print(f"[错误] 数据库迁移失败: {e}")
        sys.exit(1)

    # 7. 创建超级管理员
    print("\n" + "=" * 60)
    print("步骤 3: 创建超级管理员")
    print("=" * 60)

    User = get_user_model()  # noqa: N806

    # 从环境变量获取管理员信息，或使用默认值
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    if not User.objects.filter(username=admin_username).exists():
        try:
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            print("[OK] 超级管理员创建成功")
            print(f"  用户名: {admin_username}")
            print(f"  邮箱: {admin_email}")
            print(f"  密码: {admin_password}")
            print("\n[警告] 请在生产环境中修改默认密码!")
        except Exception as e:
            print(f"[错误] 创建超级管理员失败: {e}")
    else:
        print(f"[OK] 超级管理员已存在: {admin_username}")

    # 8. 验证数据库
    print("\n" + "=" * 60)
    print("步骤 4: 验证数据库")
    print("=" * 60)

    user_count = User.objects.count()
    print(f"[OK] 用户总数: {user_count}")
    print(f"[OK] 数据库位置: {new_db}")

    # 9. 清理临时文件
    print("\n" + "=" * 60)
    print("步骤 5: 清理临时文件")
    print("=" * 60)

    temp_files = [
        BASE_DIR / ".coverage",
        BASE_DIR / "htmlcov",
        BASE_DIR / ".pytest_cache",
        BASE_DIR / ".mypy_cache",
        BASE_DIR / ".ruff_cache",
        BASE_DIR / "test_api.py",
        BASE_DIR / "check_db.py",
    ]

    for temp_file in temp_files:
        if temp_file.exists():
            try:
                if temp_file.is_dir():
                    shutil.rmtree(temp_file)
                else:
                    temp_file.unlink()
                print(f"[OK] 已删除: {temp_file.name}")
            except Exception as e:
                print(f"[警告] 无法删除 {temp_file.name}: {e}")

    print("\n" + "=" * 60)
    print("[完成] 数据库迁移和初始化完成!")
    print("=" * 60)
    print(f"\n数据库文件位置: {new_db}")
    print("管理后台地址: http://127.0.0.1:8000/admin/")
    print("API文档地址: http://127.0.0.1:8000/api/docs")
    print("\n启动服务命令: python manage.py runserver")
    print("=" * 60)


if __name__ == "__main__":
    main()
