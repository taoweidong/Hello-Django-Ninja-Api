"""
IP黑名单DTO
IP Blacklist DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class IPBlacklistDTO(BaseModel):
    """IP黑名单DTO"""

    ip_address: str = Field(..., description="IP地址")
    reason: str | None = Field(None, description="封禁原因")
    is_permanent: bool = Field(default=False, description="是否永久封禁")
    expires_at: datetime | None = Field(None, description="过期时间")

    class Config:
        json_schema_extra = {
            "example": {"ip_address": "192.168.1.100", "reason": "恶意攻击", "is_permanent": True}
        }


# 重建模型以解决循环引用问题
IPBlacklistDTO.model_rebuild()
