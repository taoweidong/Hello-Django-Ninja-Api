"""
分配角色DTO
Assign Role DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class AssignRoleDTO(BaseModel):
    """分配角色DTO"""

    user_id: str = Field(..., description="用户ID")
    role_id: str = Field(..., description="角色ID")

    class Config:
        json_schema_extra = {"example": {"user_id": "uuid", "role_id": "uuid"}}


# 重建模型以解决循环引用问题
AssignRoleDTO.model_rebuild()
