"""
用户创建DTO
User Create DTO - 数据传输对象
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreateDTO(BaseModel):
    """用户创建DTO"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    first_name: str | None = Field(None, max_length=30, description="名")
    last_name: str | None = Field(None, max_length=30, description="姓")
    phone: str | None = Field(None, description="手机号")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "13800138000",
            }
        }
