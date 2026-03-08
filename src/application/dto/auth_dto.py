"""
认证DTO
Auth DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class TokenResponseDTO(BaseModel):
    """Token响应DTO"""

    access_token: str = Field(..., description="访问令牌")
    refresh_token: str | None = Field(None, description="刷新令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    user: dict | None = Field(None, description="用户信息")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 3600,
                "user": {"user_id": "uuid", "username": "john_doe", "email": "john@example.com"},
            }
        }


class RefreshTokenDTO(BaseModel):
    """刷新Token DTO"""

    refresh_token: str = Field(..., description="刷新令牌")

    class Config:
        json_schema_extra = {
            "example": {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }


class LoginLogDTO(BaseModel):
    """登录日志DTO"""

    id: str = Field(..., description="日志ID")
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    ip_address: str = Field(..., description="IP地址")
    user_agent: str | None = Field(None, description="用户代理")
    device_info: str | None = Field(None, description="设备信息")
    login_status: bool = Field(..., description="登录状态")
    fail_reason: str | None = Field(None, description="失败原因")
    login_time: datetime = Field(..., description="登录时间")

    class Config:
        from_attributes = True
