"""
用户更新DTO
User Update DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


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
