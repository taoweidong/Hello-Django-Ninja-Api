"""
DTO模块
DTO Module - 数据传输对象
"""

from src.application.dto.auth import (
    LoginLogDTO,
    RefreshTokenDTO,
    TokenResponseDTO,
)
from src.application.dto.rbac import (
    AssignRoleDTO,
    PermissionResponseDTO,
    RoleCreateDTO,
    RoleResponseDTO,
    RoleUpdateDTO,
    UserRolesResponseDTO,
)
from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
    RateLimitStatusDTO,
)
from src.application.dto.user import (
    ChangePasswordDTO,
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
    UserUpdateDTO,
)

__all__ = [
    # Auth DTOs
    "TokenResponseDTO",
    "RefreshTokenDTO",
    "LoginLogDTO",
    # User DTOs
    "UserCreateDTO",
    "UserUpdateDTO",
    "UserResponseDTO",
    "UserLoginDTO",
    "ChangePasswordDTO",
    # RBAC DTOs
    "RoleCreateDTO",
    "RoleUpdateDTO",
    "RoleResponseDTO",
    "PermissionResponseDTO",
    "AssignRoleDTO",
    "UserRolesResponseDTO",
    # Security DTOs
    "IPBlacklistDTO",
    "IPBlacklistResponseDTO",
    "IPWhitelistDTO",
    "IPWhitelistResponseDTO",
    "RateLimitRuleDTO",
    "RateLimitRuleResponseDTO",
    "RateLimitStatusDTO",
]
