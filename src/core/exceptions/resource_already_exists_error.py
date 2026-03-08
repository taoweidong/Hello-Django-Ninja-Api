"""
资源已存在异常
Resource Already Exists Error - 资源已存在异常
"""

from src.core.exceptions.base import BaseAPIError


class ResourceAlreadyExistsError(BaseAPIError):
    """
    资源已存在异常
    用于资源已存在的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "资源已存在"):
        """
        初始化资源已存在错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "RESOURCE_ALREADY_EXISTS")
