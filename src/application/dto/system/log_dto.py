"""
操作日志DTO
Operation Log DTO - 数据传输对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class LogResponseDTO(BaseModel):
    """操作日志响应DTO"""

    id: int = Field(..., description="日志ID")
    module: str | None = Field(None, description="模块名称")
    path: str | None = Field(None, description="请求路径")
    method: str | None = Field(None, description="请求方法")
    body: str | None = Field(None, description="请求体")
    ipaddress: str | None = Field(None, description="IP地址")
    browser: str | None = Field(None, description="浏览器")
    system: str | None = Field(None, description="操作系统")
    response_code: int | None = Field(None, description="响应状态码")
    response_result: str | None = Field(None, description="响应结果")
    status_code: int | None = Field(None, description="业务状态码")
    description: str | None = Field(None, description="描述")
    creator_id: int | None = Field(None, description="操作者ID")
    creator_name: str | None = Field(None, description="操作者用户名")
    created_time: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class LogFilterDTO(BaseModel):
    """操作日志过滤DTO"""

    module: str | None = Field(None, description="模块名称")
    method: str | None = Field(None, description="请求方法")
    creator_id: int | None = Field(None, description="操作者ID")
    start_time: datetime | None = Field(None, description="开始时间")
    end_time: datetime | None = Field(None, description="结束时间")
    response_code: int | None = Field(None, description="响应状态码")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")

    class Config:
        json_schema_extra = {
            "example": {
                "module": "用户管理",
                "method": "POST",
                "start_time": "2024-01-01T00:00:00",
                "end_time": "2024-12-31T23:59:59",
                "page": 1,
                "page_size": 20,
            }
        }
