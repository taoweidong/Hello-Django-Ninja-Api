"""
用户角色响应DTO
User Roles Response DTO - 数据传输对象
"""

from pydantic import BaseModel, Field

from src.application.dto.rbac.role_response_dto import RoleResponseDTO


class UserRolesResponseDTO(BaseModel):
    """用户角色响应DTO"""

    user_id: str = Field(..., description="用户ID")
    roles: list[RoleResponseDTO] = Field(default_factory=list, description="角色列表")
    permissions: list[str] = Field(default_factory=list, description="权限代码列表")
