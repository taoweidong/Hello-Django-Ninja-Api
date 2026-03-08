"""
IP黑名单响应DTO
IP Blacklist Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class IPBlacklistResponseDTO(BaseModel):
    """IP黑名单响应DTO"""

    blacklist_id: str = Field(..., description="黑名单ID")
    ip_address: str = Field(..., description="IP地址")
    reason: str | None = Field(None, description="封禁原因")
    is_permanent: bool = Field(..., description="是否永久封禁")
    expires_at: datetime | None = Field(None, description="过期时间")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
