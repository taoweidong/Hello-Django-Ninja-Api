"""
API响应工具
API Response Utilities - 统一的响应对象和工厂
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class MessageResponse(BaseModel):
    """
    消息响应
    用于返回简单的操作结果消息
    """

    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    """
    通用分页响应
    用于返回分页数据列表

    类型参数:
        T: 列表项的数据类型
    """

    items: list[T]
    total: int
    page: int
    page_size: int


class ResponseFactory:
    """
    响应工厂
    提供统一的响应对象创建方法
    """

    @staticmethod
    def message(msg: str) -> dict[str, str]:
        """
        创建消息响应

        参数:
            msg: 消息内容

        返回:
            包含消息的字典
        """
        return {"message": msg}

    @staticmethod
    def paginated(items: list[Any], total: int, page: int, page_size: int) -> dict[str, Any]:
        """
        创建分页响应

        参数:
            items: 数据列表
            total: 总数
            page: 当前页码
            page_size: 每页数量

        返回:
            包含分页数据的字典
        """
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> dict[str, Any]:
        """
        创建成功响应

        参数:
            data: 响应数据
            message: 成功消息

        返回:
            包含数据和消息的字典
        """
        response = {"success": True, "message": message}
        if data is not None:
            response["data"] = data
        return response

    @staticmethod
    def error(message: str, code: str = None) -> dict[str, Any]:
        """
        创建错误响应

        参数:
            message: 错误消息
            code: 错误代码

        返回:
            包含错误信息的字典
        """
        response = {"success": False, "message": message}
        if code:
            response["code"] = code
        return response
