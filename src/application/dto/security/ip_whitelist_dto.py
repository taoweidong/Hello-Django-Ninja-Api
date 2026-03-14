"""
IP白名单DTO
IP Whitelist DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class IPWhitelistDTO(BaseModel):
    """IP白名单DTO"""

    ip_address: str = Field(..., description="IP地址")
    description: str | None = Field(None, description="描述")

    class Config:
        json_schema_extra = {"example": {"ip_address": "10.0.0.1", "description": "内部网络"}}


# 重建模型以解决循环引用问题
IPWhitelistDTO.model_rebuild()
