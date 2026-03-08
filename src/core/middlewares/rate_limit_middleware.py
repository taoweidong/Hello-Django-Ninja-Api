"""
限流中间件
Rate Limit Middleware - 基于IP的请求频率限制
"""

import logging

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    限流中间件
    基于IP的请求频率限制

    功能:
        - 基于IP地址限制请求频率
        - 支持自定义限流规则
        - 记录限流日志

    配置:
        RATE_LIMIT_ENABLED: 是否启用限流（默认True）
        RATE_LIMIT_DEFAULT: 默认限流规则（默认100/minute）
    """

    def __init__(self, get_response):
        """
        初始化中间件

        参数:
            get_response: 下一个中间件或视图
        """
        self.get_response = get_response
        self.enabled = getattr(settings, "RATE_LIMIT_ENABLED", True)
        self.default_limit = getattr(settings, "RATE_LIMIT_DEFAULT", "100/minute")

    def __call__(self, request: HttpRequest):
        """
        处理请求

        参数:
            request: HTTP请求对象

        返回:
            HTTP响应对象
        """
        if not self.enabled:
            return self.get_response(request)

        # 获取客户端IP
        ip = self._get_client_ip(request)

        # 检查限流
        if not self._check_rate_limit(ip, request.path, request.method):
            logger.warning(f"Rate limit exceeded for IP: {ip}, Path: {request.path}")
            return JsonResponse(
                {
                    "error": "RATE_LIMIT_ERROR",
                    "message": "请求过于频繁，请稍后再试",
                },
                status=429,
            )

        return self.get_response(request)

    def _get_client_ip(self, request: HttpRequest) -> str:
        """
        获取客户端IP地址

        参数:
            request: HTTP请求对象

        返回:
            客户端IP地址
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
        return ip

    def _check_rate_limit(self, ip: str, path: str, method: str) -> bool:
        """
        检查限流

        参数:
            ip: 客户端IP地址
            path: 请求路径
            method: HTTP方法

        返回:
            是否允许请求通过
        """
        # 简单限流实现
        key = f"rate_limit:{ip}:{method}:{path}"

        # 获取当前请求数
        current = cache.get(key, 0)

        if current >= 100:  # 简单限制：每分钟100次
            return False

        # 增加计数
        cache.set(key, current + 1, 60)  # 60秒过期

        return True
