"""
Token错误异常
Token Error - JWT Token相关异常
"""

from src.core.exceptions.base import BaseAPIError


class TokenError(BaseAPIError):
    """
    Token错误异常
    用于Token无效的场景

    继承自:
        BaseAPIError
    """

    def __init__(self, message: str = "Token无效"):
        """
        初始化Token错误

        参数:
            message: 错误消息
        """
        super().__init__(message, "TOKEN_ERROR")


class TokenExpiredError(TokenError):
    """
    Token过期异常
    用于Token过期的场景

    继承自:
        TokenError
    """

    def __init__(self, message: str = "Token已过期"):
        """
        初始化Token过期错误

        参数:
            message: 错误消息
        """
        super().__init__(message)
        self.code = "TOKEN_EXPIRED"
