"""
URL Configuration
项目所有URL路由配置
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from src.api.app import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # Django-Ninja API路由
]

# 开发环境静态文件配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
