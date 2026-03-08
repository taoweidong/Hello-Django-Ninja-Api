"""
限流错误异常
Rate Limit Error - 请求频率限制异常
"""

from src.core.exceptions.base import BaseAPIError


class RateLimitError(BaseAPIError):
    """
    限流错误异常
    用于请求过于频繁的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "请求过于频繁"):
        """
        初始化限流错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "RATE_LIMIT_ERROR")
