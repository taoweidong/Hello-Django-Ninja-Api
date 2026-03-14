"""
DTO基类
DTO Base Classes - 提供通用的数据传输对象基类
"""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseDTO(BaseModel):
    """
    DTO基类
    提供通用的配置和方法
    """

    class Config:
        """Pydantic配置"""

        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class BasePaginatedResponse(BaseModel, Generic[T]):
    """
    通用分页响应基类
    用于所有分页查询的响应

    类型参数:
        T: 列表项的数据类型

    属性:
        items: 数据列表
        total: 总数
        page: 当前页码
        page_size: 每页数量
        has_next: 是否有下一页
        has_prev: 是否有上一页
    """

    items: list[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    has_next: bool = Field(False, description="是否有下一页")
    has_prev: bool = Field(False, description="是否有上一页")

    class Config:
        """Pydantic配置"""

        from_attributes = True

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "BasePaginatedResponse[T]":
        """
        创建分页响应

        参数:
            items: 数据列表
            total: 总数
            page: 当前页码
            page_size: 每页数量

        返回:
            分页响应实例
        """
        has_next = page * page_size < total
        has_prev = page > 1

        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev,
        )


class BaseCreateDTO(BaseDTO):
    """
    创建操作DTO基类
    用于创建实体的数据传输
    """

    pass


class BaseUpdateDTO(BaseDTO):
    """
    更新操作DTO基类
    用于更新实体的数据传输
    """

    pass


class BaseResponseDTO(BaseDTO):
    """
    响应DTO基类
    用于返回实体数据的响应
    """

    pass


class TimestampMixin:
    """
    时间戳混入类
    为DTO添加创建和更新时间字段
    """

    created_at: datetime | None = Field(None, description="创建时间")
    updated_at: datetime | None = Field(None, description="更新时间")


class IDMixin:
    """
    ID混入类
    为DTO添加ID字段
    """

    id: str = Field(..., description="唯一标识符")


class AuditMixin:
    """
    审计混入类
    为DTO添加审计字段
    """

    created_by: str | None = Field(None, description="创建者ID")
    updated_by: str | None = Field(None, description="更新者ID")


class StatusMixin:
    """
    状态混入类
    为DTO添加状态字段
    """

    is_active: bool = Field(True, description="是否激活")
    is_deleted: bool = Field(False, description="是否删除")


class BaseEntityDTO(BaseResponseDTO, IDMixin, TimestampMixin):
    """
    实体DTO基类
    包含ID和时间戳字段
    """

    pass


class FullEntityDTO(BaseEntityDTO, AuditMixin, StatusMixin):
    """
    完整实体DTO基类
    包含ID、时间戳、审计和状态字段
    """

    pass


class MessageResponse(BaseModel):
    """
    消息响应
    用于返回简单的操作结果消息
    """

    message: str = Field(..., description="消息内容")
    code: str | None = Field(None, description="消息代码")
    data: Any | None = Field(None, description="附加数据")

    class Config:
        """Pydantic配置"""

        from_attributes = True


class ErrorResponse(BaseModel):
    """
    错误响应
    用于返回错误信息
    """

    success: bool = Field(False, description="是否成功")
    message: str = Field(..., description="错误消息")
    code: str | None = Field(None, description="错误代码")
    details: dict[str, Any] | None = Field(None, description="错误详情")

    class Config:
        """Pydantic配置"""

        from_attributes = True
