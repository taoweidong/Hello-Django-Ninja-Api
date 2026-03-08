"""
角色响应DTO
Role Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


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
