"""
用户控制器
User Controller - 用户管理API控制器
"""

from src.application.dto.user import (
    ChangePasswordDTO,
    UserCreateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from src.application.services.user_service import UserService


class UserController:
    """
    用户控制器
    处理用户相关API请求
    """

    def __init__(self, user_service: UserService = None):
        self._user_service = user_service or UserService()

    async def create_user(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        """创建用户"""
        return await self._user_service.create_user(user_dto)

    async def get_user(self, user_id: str) -> UserResponseDTO:
        """获取用户详情"""
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        return user

    async def list_users(self, page: int, page_size: int) -> tuple[list[UserResponseDTO], int]:
        """获取用户列表"""
        return await self._user_service.list_users(page, page_size)

    async def update_user(self, user_id: str, user_dto: UserUpdateDTO) -> UserResponseDTO:
        """更新用户"""
        return await self._user_service.update_user(user_id, user_dto)

    async def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        result = await self._user_service.delete_user(user_id)
        if not result:
            raise ValueError("用户不存在")
        return result

    async def change_password(self, user_id: str, password_dto: ChangePasswordDTO) -> bool:
        """修改密码"""
        return await self._user_service.change_password(
            user_id, password_dto.old_password, password_dto.new_password
        )

    async def get_current_user(self, user_id: str) -> UserResponseDTO:
        """获取当前用户信息"""
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        return user
