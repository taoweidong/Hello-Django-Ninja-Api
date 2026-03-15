"""
修改密码DTO
Change Password DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class ChangePasswordDTO(BaseModel):
    """修改密码DTO"""

    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")

    class Config:
        json_schema_extra = {"example": {"old_password": "old_password123", "new_password": "new_password123"}}


# 重建模型以解决循环引用问题
ChangePasswordDTO.model_rebuild()
