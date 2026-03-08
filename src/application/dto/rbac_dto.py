"""
RBAC DTO
RBAC DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RoleCreateDTO(BaseModel):
    """角色创建DTO"""

    name: str = Field(..., min_length=1, max_length=100, description="角色名称")
    code: str = Field(..., min_length=1, max_length=50, description="角色代码")
    description: str | None = Field(None, description="角色描述")
    permissions: list[str] = Field(default_factory=list, description="权限代码列表")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "管理员",
                "code": "admin",
                "description": "系统管理员",
                "permissions": ["user:read", "user:write", "user:delete"],
            }
        }


class RoleUpdateDTO(BaseModel):
    """角色更新DTO"""

    name: str | None = Field(None, min_length=1, max_length=100, description="角色名称")
    description: str | None = Field(None, description="角色描述")
    permissions: list[str] | None = Field(None, description="权限代码列表")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "超级管理员",
                "description": "系统超级管理员",
                "permissions": ["user:read", "user:write", "user:delete", "role:manage"],
            }
        }


class RoleResponseDTO(BaseModel):
    """角色响应DTO"""

    role_id: str = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    code: str = Field(..., description="角色代码")
    description: str | None = Field(None, description="角色描述")
    permissions: list[str] = Field(default_factory=list, description="权限代码列表")
    is_system: bool = Field(..., description="是否系统角色")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class PermissionResponseDTO(BaseModel):
    """权限响应DTO"""

    permission_id: str = Field(..., description="权限ID")
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限代码")
    resource: str = Field(..., description="资源类型")
    action: str = Field(..., description="操作类型")
    description: str | None = Field(None, description="权限描述")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class AssignRoleDTO(BaseModel):
    """分配角色DTO"""

    user_id: str = Field(..., description="用户ID")
    role_id: str = Field(..., description="角色ID")

    class Config:
        json_schema_extra = {"example": {"user_id": "uuid", "role_id": "uuid"}}


class UserRolesResponseDTO(BaseModel):
    """用户角色响应DTO"""

    user_id: str = Field(..., description="用户ID")
    roles: list[RoleResponseDTO] = Field(default_factory=list, description="角色列表")
    permissions: list[str] = Field(default_factory=list, description="权限代码列表")
