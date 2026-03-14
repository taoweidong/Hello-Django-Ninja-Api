"""
Token响应DTO
Token Response DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class TokenResponseDTO(BaseModel):
    """Token 响应 DTO"""

    access_token: str = Field(..., description="访问令牌")
    refresh_token: str | None = Field(None, description="刷新令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间 (秒)")
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


# 重建模型以解决循环引用问题
TokenResponseDTO.model_rebuild()
