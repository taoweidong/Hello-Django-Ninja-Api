"""
认证错误异常
Authentication Error - 用户认证失败异常
"""

from src.core.exceptions.base import BaseAPIError


class AuthenticationError(BaseAPIError):
    """
    认证错误异常
    用于用户认证失败的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "认证失败"):
        """
        初始化认证错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "AUTHENTICATION_ERROR")
