"""
凭据无效异常
Invalid Credentials Error - 用户凭据无效异常
"""

from src.core.exceptions.authentication_error import AuthenticationError


class InvalidCredentialsError(AuthenticationError):
    """
    凭据无效异常
    用于用户名或密码错误的场景

    继承自:
        AuthenticationError
    """

    def __init__(self, message: str = "用户名或密码错误"):
        """
        初始化凭据无效错误

        参数:
            message: 错误消息
        """
        super().__init__(message)
