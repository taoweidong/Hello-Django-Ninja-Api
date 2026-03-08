"""
资源不存在异常
Resource Not Found Error - 请求的资源不存在异常
"""

from src.core.exceptions.base import BaseAPIError


class ResourceNotFoundError(BaseAPIError):
    """
    资源不存在异常
    用于请求的资源不存在的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "资源不存在"):
        """
        初始化资源不存在错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "RESOURCE_NOT_FOUND")
