"""
角色DTO
Role DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RoleCreateDTO(BaseModel):
    """角色创建DTO"""

    name: str = Field(..., min_length=1, max_length=128, description="角色名称")
    code: str = Field(..., min_length=1, max_length=128, description="角色编码")
    is_active: bool = Field(default=True, description="是否激活")
    description: str | None = Field(None, max_length=256, description="描述")
    menu_ids: list[str] = Field(default_factory=list, description="菜单ID列表")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "管理员",
                "code": "ADMIN",
                "is_active": True,
                "description": "系统管理员",
                "menu_ids": ["menu_id_1", "menu_id_2"],
            }
        }


class RoleUpdateDTO(BaseModel):
    """角色更新DTO"""

    name: str | None = Field(None, min_length=1, max_length=128, description="角色名称")
    code: str | None = Field(None, min_length=1, max_length=128, description="角色编码")
    is_active: bool | None = Field(None, description="是否激活")
    description: str | None = Field(None, max_length=256, description="描述")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "超级管理员",
                "description": "系统超级管理员（更新）",
            }
        }


class RoleAssignMenuDTO(BaseModel):
    """角色分配菜单DTO"""

    menu_ids: list[str] = Field(..., description="菜单ID列表")

    class Config:
        json_schema_extra = {
            "example": {
                "menu_ids": ["menu_id_1", "menu_id_2", "menu_id_3"],
            }
        }


class RoleResponseDTO(BaseModel):
    """角色响应DTO"""

    id: str = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    code: str = Field(..., description="角色编码")
    is_active: bool = Field(..., description="是否激活")
    description: str | None = Field(None, description="描述")
    menu_count: int = Field(default=0, description="菜单数量")
    created_time: datetime = Field(..., description="创建时间")
    updated_time: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
