"""
Django应用配置
"""

from django.apps import AppConfig


class PersistenceConfig(AppConfig):
    """应用配置类"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.infrastructure.persistence"
    verbose_name = "Hello Django Ninja API"
