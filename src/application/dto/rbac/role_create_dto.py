"""
角色创建DTO
Role Create DTO - 数据传输对象
"""

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


# 重建模型以解决循环引用问题
RoleCreateDTO.model_rebuild()
