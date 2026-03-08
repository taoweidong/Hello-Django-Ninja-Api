"""
IP被封禁异常
IP Blocked Error - IP地址被封禁异常
"""

from src.core.exceptions.base import BaseAPIError


class IPBlockedError(BaseAPIError):
    """
    IP被封禁异常
    用于IP地址被封禁的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "IP已被封禁"):
        """
        初始化IP被封禁错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "IP_BLOCKED")
