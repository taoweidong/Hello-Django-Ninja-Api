"""
DTO模块
DTO Module - 数据传输对象
"""

from src.application.dto.auth import LoginLogDTO, RefreshTokenDTO, TokenResponseDTO
from src.application.dto.rbac import AssignRoleDTO, PermissionResponseDTO, RoleCreateDTO, RoleResponseDTO, RoleUpdateDTO, UserRolesResponseDTO
from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
    RateLimitStatusDTO,
)
from src.application.dto.user import ChangePasswordDTO, UserCreateDTO, UserLoginDTO, UserResponseDTO, UserUpdateDTO

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

# 重建所有 DTO 模型以解决 Pydantic 2.5+ 前向引用问题
for dto_class in [
    TokenResponseDTO,
    RefreshTokenDTO,
    LoginLogDTO,
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
    UserLoginDTO,
    ChangePasswordDTO,
    RoleCreateDTO,
    RoleUpdateDTO,
    RoleResponseDTO,
    PermissionResponseDTO,
    AssignRoleDTO,
    UserRolesResponseDTO,
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
    RateLimitStatusDTO,
]:
    if hasattr(dto_class, "model_rebuild"):
        dto_class.model_rebuild()
