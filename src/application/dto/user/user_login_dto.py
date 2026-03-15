"""
用户登录DTO
User Login DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class UserLoginDTO(BaseModel):
    """用户登录 DTO"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    device_info: str | None = Field(None, description="设备信息")

    class Config:
        json_schema_extra = {"example": {"username": "john_doe", "password": "password123", "device_info": "iPhone 14 Pro"}}


# 重建模型以解决循环引用问题
UserLoginDTO.model_rebuild()
