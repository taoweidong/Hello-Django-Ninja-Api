"""
权限不足异常
Permission Denied Error - 用户权限不足异常
"""

from src.core.exceptions.base import BaseAPIError


class PermissionDeniedError(BaseAPIError):
    """
    权限不足异常
    用于用户权限不足的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "权限不足"):
        """
        初始化权限不足错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "PERMISSION_DENIED")
