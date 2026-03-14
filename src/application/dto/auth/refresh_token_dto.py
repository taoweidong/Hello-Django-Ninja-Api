"""
刷新Token DTO
Refresh Token DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class RefreshTokenDTO(BaseModel):
    """刷新Token DTO"""

    refresh_token: str = Field(..., description="刷新令牌")

    class Config:
        json_schema_extra = {
            "example": {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }


# 重建模型以解决循环引用问题
RefreshTokenDTO.model_rebuild()
