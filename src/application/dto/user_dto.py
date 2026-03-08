"""
用户DTO
User DTO - 数据传输对象
"""

from datetime import datetime

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


class UserUpdateDTO(BaseModel):
    """用户更新DTO"""

    first_name: str | None = Field(None, max_length=30, description="名")
    last_name: str | None = Field(None, max_length=30, description="姓")
    phone: str | None = Field(None, description="手机号")
    avatar: str | None = Field(None, description="头像URL")
    bio: str | None = Field(None, description="个人简介")

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "13800138000",
                "avatar": "https://example.com/avatar.jpg",
                "bio": "Hello, I'm John!",
            }
        }


class UserResponseDTO(BaseModel):
    """用户响应DTO"""

    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    first_name: str | None = Field(None, description="名")
    last_name: str | None = Field(None, description="姓")
    is_active: bool = Field(..., description="是否激活")
    is_staff: bool = Field(..., description="是否员工")
    is_superuser: bool = Field(..., description="是否超级管理员")
    avatar: str | None = Field(None, description="头像URL")
    phone: str | None = Field(None, description="手机号")
    bio: str | None = Field(None, description="个人简介")
    date_joined: datetime = Field(..., description="注册时间")
    last_login: datetime | None = Field(None, description="最后登录")

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    """用户登录DTO"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    device_info: str | None = Field(None, description="设备信息")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "password123",
                "device_info": "iPhone 14 Pro",
            }
        }


class ChangePasswordDTO(BaseModel):
    """修改密码DTO"""

    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")

    class Config:
        json_schema_extra = {
            "example": {"old_password": "old_password123", "new_password": "new_password123"}
        }
