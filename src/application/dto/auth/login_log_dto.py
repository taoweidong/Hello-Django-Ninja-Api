"""
登录日志DTO
Login Log DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class LoginLogDTO(BaseModel):
    """登录日志DTO"""

    id: str = Field(..., description="日志ID")
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    ip_address: str = Field(..., description="IP地址")
    user_agent: str | None = Field(None, description="用户代理")
    device_info: str | None = Field(None, description="设备信息")
    login_status: bool = Field(..., description="登录状态")
    fail_reason: str | None = Field(None, description="失败原因")
    login_time: datetime = Field(..., description="登录时间")

    class Config:
        from_attributes = True
