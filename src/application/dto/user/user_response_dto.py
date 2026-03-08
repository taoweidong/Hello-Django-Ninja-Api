"""
用户响应DTO
User Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


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
