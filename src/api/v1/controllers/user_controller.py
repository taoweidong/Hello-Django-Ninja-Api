"""
用户控制器
User Controller - 用户管理API控制器
"""

from typing import Annotated

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from src.api.common.responses import MessageResponse
from src.application.dto.user import ChangePasswordDTO, UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.application.services.user_service import UserService
from src.infrastructure.auth_jwt import GlobalAuth


class UserListResponse(MessageResponse):
    """用户列表响应"""

    users: list[UserResponseDTO]
    total: int
    page: int
    page_size: int


@api_controller("/v1", tags=["用户"], auth=GlobalAuth())
class UserController:
    """
    用户控制器
    处理用户相关API请求

    遵循SOLID原则:
    - 单一职责: 只处理用户相关的HTTP请求
    - 依赖倒置: 通过构造函数注入 UserService

    权限说明:
    - 默认需要鉴权（控制器级别配置）
    - 只有注册接口豁免鉴权（auth=None）
    """

    def __init__(self, user_service: UserService | None = None) -> None:
        """
        初始化用户控制器

        Args:
            user_service: 用户服务实例（可选，用于依赖注入）
        """
        self._user_service = user_service or UserService()

    @http_post("/users", response=UserResponseDTO, summary="创建用户", operation_id="user_create", auth=None)
    async def create_user(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        """
        创建用户（公开接口，无需鉴权）

        - 注册新用户

        Args:
            user_dto: 用户创建数据传输对象

        Returns:
            UserResponseDTO: 创建的用户信息

        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._user_service.create_user(user_dto)
        return result

    @http_get("/users/{user_id}", response=UserResponseDTO, summary="获取用户详情", operation_id="user_get")
    async def get_user(self, user_id: str) -> UserResponseDTO:
        """
        获取用户详情

        - 根据用户ID获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            UserResponseDTO: 用户信息

        Raises:
            ValueError: 用户不存在时抛出
        """
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        return user

    @http_get("/users", response=UserListResponse, summary="获取用户列表", operation_id="user_list")
    async def list_users(self, page: Annotated[int, Query(ge=1)] = 1, page_size: Annotated[int, Query(ge=1, le=100)] = 10) -> UserListResponse:
        """
        获取用户列表

        - 分页获取用户列表

        Args:
            page: 页码（从1开始）
            page_size: 每页数量（最大100）

        Returns:
            UserListResponse: 用户列表响应
        """
        users, total = await self._user_service.list_users(page, page_size)
        return UserListResponse(message="获取成功", users=users, total=total, page=page, page_size=page_size)

    @http_put("/users/{user_id}", response=UserResponseDTO, summary="更新用户", operation_id="user_update")
    async def update_user(self, user_id: str, user_dto: UserUpdateDTO) -> UserResponseDTO:
        """
        更新用户信息

        - 更新用户的基本信息

        Args:
            user_id: 用户ID
            user_dto: 用户更新数据传输对象

        Returns:
            UserResponseDTO: 更新后的用户信息

        Raises:
            ValueError: 更新失败时抛出
        """
        result = await self._user_service.update_user(user_id, user_dto)
        return result

    @http_delete("/users/{user_id}", response=MessageResponse, summary="删除用户", operation_id="user_delete")
    async def delete_user(self, user_id: str) -> MessageResponse:
        """
        删除用户

        - 软删除用户

        Args:
            user_id: 用户ID

        Returns:
            MessageResponse: 操作结果消息

        Raises:
            ValueError: 用户不存在时抛出
        """
        result = await self._user_service.delete_user(user_id)
        if not result:
            raise ValueError("用户不存在")
        return MessageResponse(message="用户删除成功")

    @http_post("/users/change-password", response=MessageResponse, summary="修改密码", operation_id="user_change_password")
    async def change_password(self, request: Annotated[object, "Django HttpRequest"], password_dto: ChangePasswordDTO) -> MessageResponse:
        """
        修改密码

        - 修改当前用户密码

        Args:
            request: Django HTTP请求对象
            password_dto: 修改密码数据传输对象

        Returns:
            MessageResponse: 操作结果消息
        """
        user_id = request.auth.get("user_id")  # type: ignore
        await self._user_service.change_password(user_id, password_dto.old_password, password_dto.new_password)
        return MessageResponse(message="密码修改成功")

    @http_get("/me", response=UserResponseDTO, summary="获取当前用户信息", operation_id="user_get_current")
    async def get_current_user_info(self, request: Annotated[object, "Django HttpRequest"]) -> UserResponseDTO:
        """
        获取当前用户信息

        - 获取已登录用户的信息

        Args:
            request: Django HTTP请求对象

        Returns:
            UserResponseDTO: 当前用户信息

        Raises:
            ValueError: 用户不存在时抛出
        """
        user_id = request.auth.get("user_id")  # type: ignore
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        return user
