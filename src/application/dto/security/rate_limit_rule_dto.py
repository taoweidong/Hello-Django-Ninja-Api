"""
限流规则DTO
Rate Limit Rule DTO - 数据传输对象
"""

from pydantic import BaseModel, Field


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


# 重建模型以解决循环引用问题
RateLimitRuleDTO.model_rebuild()
