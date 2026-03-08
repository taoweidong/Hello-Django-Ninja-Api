"""
IP过滤中间件
IP Limit Middleware - 处理IP黑白名单
"""

import logging
from datetime import datetime

from django.conf import settings
from django.http import HttpRequest, JsonResponse

logger = logging.getLogger(__name__)


class IPLimitMiddleware:
    """
    IP过滤中间件
    处理IP黑白名单

    功能:
        - IP白名单过滤
        - IP黑名单过滤
        - 支持临时和永久封禁

    配置:
        IP_BLACKLIST_ENABLED: 是否启用黑名单（默认False）
        IP_WHITELIST_ENABLED: 是否启用白名单（默认False）
    """

    def __init__(self, get_response):
        """
        初始化中间件

        参数:
            get_response: 下一个中间件或视图
        """
        self.get_response = get_response
        self.blacklist_enabled = getattr(settings, "IP_BLACKLIST_ENABLED", False)
        self.whitelist_enabled = getattr(settings, "IP_WHITELIST_ENABLED", False)

    def __call__(self, request: HttpRequest):
        """
        处理请求

        参数:
            request: HTTP请求对象

        返回:
            HTTP响应对象
        """
        # 获取客户端IP
        ip = self._get_client_ip(request)

        # 白名单模式
        if self.whitelist_enabled and not self._is_whitelisted(ip):
            logger.warning(f"IP not in whitelist: {ip}")
            return JsonResponse(
                {
                    "error": "IP_BLOCKED",
                    "message": "IP不在白名单中",
                },
                status=403,
            )

        # 黑名单模式
        if self.blacklist_enabled and self._is_blacklisted(ip):
            logger.warning(f"IP in blacklist: {ip}")
            return JsonResponse(
                {
                    "error": "IP_BLOCKED",
                    "message": "IP已被封禁",
                },
                status=403,
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

    def _is_whitelisted(self, ip: str) -> bool:
        """
        检查IP是否在白名单中

        参数:
            ip: IP地址

        返回:
            是否在白名单中
        """
        from src.infrastructure.persistence.models.security_models import IPWhitelist

        return IPWhitelist.objects.filter(ip_address=ip, is_active=True).exists()

    def _is_blacklisted(self, ip: str) -> bool:
        """
        检查IP是否在黑名单中

        参数:
            ip: IP地址

        返回:
            是否在黑名单中
        """
        from src.infrastructure.persistence.models.security_models import IPBlacklist

        try:
            entry = IPBlacklist.objects.get(ip_address=ip)
            if entry.is_permanent:
                return True
            if entry.expires_at and entry.expires_at > datetime.now():
                return True
        except IPBlacklist.DoesNotExist:
            pass
        return False
