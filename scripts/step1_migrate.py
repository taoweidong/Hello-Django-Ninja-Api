#!/usr/bin/env python
"""步骤1: 数据库迁移"""
import subprocess
import os

os.chdir("e:/GitHub/Hello-Django-Ninja-Api")

print("="*60)
print("步骤1: 创建和应用数据库迁移")
print("="*60)

# 创建迁移
print("\n1. 创建迁移文件...")
result = subprocess.run(
    ["python", "manage.py", "makemigrations"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# 应用迁移
print("\n2. 应用迁移...")
result = subprocess.run(
    ["python", "manage.py", "migrate", "--run-syncdb"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\n✓ 数据库迁移完成!")
