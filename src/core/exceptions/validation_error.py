"""
验证错误异常
Validation Error - 数据验证失败异常
"""

from src.core.exceptions.base import BaseAPIError


class ValidationError(BaseAPIError):
    """
    验证错误异常
    用于数据验证失败的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "数据验证失败"):
        """
        初始化验证错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "VALIDATION_ERROR")
