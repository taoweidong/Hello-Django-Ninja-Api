"""
限流状态DTO
Rate Limit Status DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


class RateLimitStatusDTO(BaseModel):
    """限流状态DTO"""

    enabled: bool = Field(..., description="是否启用")
    limit: int | None = Field(None, description="限制次数")
    remaining: int | None = Field(None, description="剩余次数")
    reset_at: str | None = Field(None, description="重置时间")
