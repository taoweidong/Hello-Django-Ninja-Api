"""
限流规则响应DTO
Rate Limit Rule Response DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


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
