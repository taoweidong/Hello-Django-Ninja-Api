"""
角色更新DTO
Role Update DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


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


# 重建模型以解决循环引用问题
RoleUpdateDTO.model_rebuild()
