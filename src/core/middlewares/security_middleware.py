"""
安全中间件
Security Middleware - 处理安全相关的请求头和防护
"""

import logging

from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """
    安全中间件
    处理安全相关的请求头和防护

    功能:
        - 添加安全响应头（X-Content-Type-Options, X-Frame-Options等）
        - 生产环境启用严格安全策略
    """

    def __init__(self, get_response):
        """
        初始化中间件

        参数:
            get_response: 下一个中间件或视图
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """
        处理请求

        参数:
            request: HTTP请求对象

        返回:
            HTTP响应对象
        """
        # 处理请求
        response = self.get_response(request)

        # 生产环境添加安全头
        if not settings.DEBUG:
            response["X-Content-Type-Options"] = "nosniff"
            response["X-Frame-Options"] = "DENY"
            response["X-XSS-Protection"] = "1; mode=block"
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
