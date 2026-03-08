"""
用户未激活异常
User Inactive Error - 用户账户未激活异常
"""

from src.core.exceptions.authentication_error import AuthenticationError


class UserInactiveError(AuthenticationError):
    """
    用户未激活异常
    用于用户账户被停用的场景

    继承自:
        AuthenticationError
    """

    def __init__(self, message: str = "用户已被停用"):
        """
        初始化用户未激活错误

        参数:
            message: 错误消息
        """
        super().__init__(message)
