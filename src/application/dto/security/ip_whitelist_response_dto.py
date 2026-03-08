"""
IP白名单响应DTO
IP Whitelist Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class IPWhitelistResponseDTO(BaseModel):
    """IP白名单响应DTO"""

    whitelist_id: str = Field(..., description="白名单ID")
    ip_address: str = Field(..., description="IP地址")
    description: str | None = Field(None, description="描述")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
