"""
测试环境配置
"""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# 测试环境使用SQLite内存数据库
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# 禁用缓存用于测试
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# 密码哈希器使用快速版本
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# 禁用速率限制
RATE_LIMIT_ENABLED = False
