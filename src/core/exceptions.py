"""
自定义异常
Custom Exceptions - 项目自定义异常类
"""


class BaseAPIError(Exception):
    """基础API异常"""

    def __init__(self, message: str = "服务器错误", code: str = "SERVER_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(BaseAPIError):
    """验证错误"""

    def __init__(self, message: str = "数据验证失败"):
        super().__init__(message, "VALIDATION_ERROR")


class AuthenticationError(BaseAPIError):
    """认证错误"""

    def __init__(self, message: str = "认证失败"):
        super().__init__(message, "AUTHENTICATION_ERROR")


class PermissionDeniedError(BaseAPIError):
    """权限不足错误"""

    def __init__(self, message: str = "权限不足"):
        super().__init__(message, "PERMISSION_DENIED")


class ResourceNotFoundError(BaseAPIError):
    """资源不存在错误"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, "RESOURCE_NOT_FOUND")


class ResourceAlreadyExistsError(BaseAPIError):
    """资源已存在错误"""

    def __init__(self, message: str = "资源已存在"):
        super().__init__(message, "RESOURCE_ALREADY_EXISTS")


class TokenError(BaseAPIError):
    """Token错误"""

    def __init__(self, message: str = "Token无效"):
        super().__init__(message, "TOKEN_ERROR")


class TokenExpiredError(TokenError):
    """Token过期错误"""

    def __init__(self, message: str = "Token已过期"):
        super().__init__(message)
        self.code = "TOKEN_EXPIRED"


class RateLimitError(BaseAPIError):
    """限流错误"""

    def __init__(self, message: str = "请求过于频繁"):
        super().__init__(message, "RATE_LIMIT_ERROR")


class IPBlockedError(BaseAPIError):
    """IP被封禁错误"""

    def __init__(self, message: str = "IP已被封禁"):
        super().__init__(message, "IP_BLOCKED")


class InvalidCredentialsError(AuthenticationError):
    """凭据无效错误"""

    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(message)


class UserInactiveError(AuthenticationError):
    """用户未激活错误"""

    def __init__(self, message: str = "用户已被停用"):
        super().__init__(message)
