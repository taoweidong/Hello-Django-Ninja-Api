"""
异常模块
Exceptions Module - 统一导出所有自定义异常类
"""

from src.core.exceptions.authentication_error import AuthenticationError
from src.core.exceptions.base import BaseAPIError
from src.core.exceptions.invalid_credentials_error import InvalidCredentialsError
from src.core.exceptions.ip_blocked_error import IPBlockedError
from src.core.exceptions.permission_denied_error import PermissionDeniedError
from src.core.exceptions.rate_limit_error import RateLimitError
from src.core.exceptions.resource_already_exists_error import ResourceAlreadyExistsError
from src.core.exceptions.resource_not_found_error import ResourceNotFoundError
from src.core.exceptions.token_error import TokenError, TokenExpiredError
from src.core.exceptions.user_inactive_error import UserInactiveError
from src.core.exceptions.validation_error import ValidationError

__all__ = [
    "BaseAPIError",
    "ValidationError",
    "AuthenticationError",
    "PermissionDeniedError",
    "ResourceNotFoundError",
    "ResourceAlreadyExistsError",
    "TokenError",
    "TokenExpiredError",
    "RateLimitError",
    "IPBlockedError",
    "InvalidCredentialsError",
    "UserInactiveError",
]
