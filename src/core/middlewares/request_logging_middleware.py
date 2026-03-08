"""
请求日志中间件
Request Logging Middleware - 记录请求日志
"""

import logging
import time

from django.http import HttpRequest

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    请求日志中间件
    记录请求日志

    功能:
        - 记录请求开始和完成信息
        - 记录请求耗时
        - 记录用户信息和IP地址
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
        # 记录请求开始时间
        start_time = time.time()

        # 获取请求信息
        method = request.method
        path = request.path
        ip = self._get_client_ip(request)
        user = request.user if request.user.is_authenticated else "anonymous"

        logger.info(f"Request started: {method} {path} from {ip} by {user}")

        # 处理请求
        response = self.get_response(request)

        # 计算请求耗时
        duration = time.time() - start_time

        # 记录响应信息
        logger.info(
            f"Request completed: {method} {path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.3f}s"
        )

        return response

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
