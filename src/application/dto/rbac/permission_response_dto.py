"""
权限响应DTO
Permission Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


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
