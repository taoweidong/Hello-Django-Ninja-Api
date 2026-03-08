# -*- coding: utf-8 -*-
"""简单代码检查"""
import subprocess
import os

os.chdir("e:/GitHub/Hello-Django-Ninja-Api")

print("=" * 60)
print("RUFF 代码检查")
print("=" * 60)

result = subprocess.run(
    [".venv/Scripts/python.exe", "-m", "ruff", "check", "src/", "tests/", "config/"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="ignore"
)

if result.returncode == 0:
    print("[OK] Ruff 检查通过！")
else:
    print(result.stdout)
    print(result.stderr)

print("\n" + "=" * 60)
print("MyPy 类型检查")
print("=" * 60)

result2 = subprocess.run(
    [".venv/Scripts/python.exe", "-m", "mypy", "src/"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="ignore"
)

if result2.returncode == 0:
    print("[OK] MyPy 检查通过！")
else:
    print(result2.stdout)
    print(result2.stderr)

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)
