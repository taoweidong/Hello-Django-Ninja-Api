"""
开发环境配置
"""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# 开发环境使用SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 开发环境日志级别
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["src"]["level"] = "DEBUG"

# 开发环境CORS
CORS_ALLOW_ALL_ORIGINS = True
