#!/usr/bin/env python
"""直接创建所有表"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from django.core.management import call_command

# 创建所有迁移
print("创建迁移文件...")
call_command("makemigrations", "persistence", verbosity=2)

# 应用迁移
print("\n应用迁移...")
call_command("migrate", verbosity=2)

print("\n✅ 表创建完成！")
