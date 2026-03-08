"""
安全DTO
Security DTO - 数据传输对象
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


class IPWhitelistDTO(BaseModel):
    """IP白名单DTO"""

    ip_address: str = Field(..., description="IP地址")
    description: str | None = Field(None, description="描述")

    class Config:
        json_schema_extra = {"example": {"ip_address": "10.0.0.1", "description": "内部网络"}}


class IPWhitelistResponseDTO(BaseModel):
    """IP白名单响应DTO"""

    whitelist_id: str = Field(..., description="白名单ID")
    ip_address: str = Field(..., description="IP地址")
    description: str | None = Field(None, description="描述")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class RateLimitRuleDTO(BaseModel):
    """限流规则DTO"""

    name: str = Field(..., description="规则名称")
    endpoint: str = Field(..., description="API端点")
    method: str = Field(default="*", description="HTTP方法")
    rate: int = Field(default=60, ge=1, description="允许的请求次数")
    period: int = Field(default=60, ge=1, description="时间周期(秒)")
    scope: str = Field(default="ip", description="限流范围")
    description: str | None = Field(None, description="描述")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "用户API限流",
                "endpoint": "/api/v1/users",
                "method": "GET",
                "rate": 60,
                "period": 60,
                "scope": "ip",
                "description": "用户列表接口限流",
            }
        }


class RateLimitRuleResponseDTO(BaseModel):
    """限流规则响应DTO"""

    limit_id: str = Field(..., description="规则ID")
    name: str = Field(..., description="规则名称")
    endpoint: str = Field(..., description="API端点")
    method: str = Field(..., description="HTTP方法")
    rate: int = Field(..., description="允许的请求次数")
    period: int = Field(..., description="时间周期(秒)")
    scope: str = Field(..., description="限流范围")
    is_active: bool = Field(..., description="是否激活")
    description: str | None = Field(None, description="描述")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class RateLimitStatusDTO(BaseModel):
    """限流状态DTO"""

    enabled: bool = Field(..., description="是否启用")
    limit: int | None = Field(None, description="限制次数")
    remaining: int | None = Field(None, description="剩余次数")
    reset_at: str | None = Field(None, description="重置时间")
