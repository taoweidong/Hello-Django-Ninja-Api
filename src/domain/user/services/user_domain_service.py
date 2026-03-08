"""
用户领域服务
User Domain Service - 处理跨实体的业务逻辑
"""

from src.domain.user.entities.user_entity import UserEntity
from src.domain.user.repositories.user_repository import UserRepositoryInterface


class UserDomainService:
    """
    用户领域服务
    处理与用户相关的核心业务逻辑
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def create_user(
        self, username: str, email: str, password: str, first_name: str = "", last_name: str = ""
    ) -> UserEntity:
        """创建用户领域逻辑"""
        # 检查用户名是否存在
        if await self.user_repository.exists_by_username(username):
            raise ValueError(f"用户名 {username} 已存在")

        # 检查邮箱是否存在
        if await self.user_repository.exists_by_email(email):
            raise ValueError(f"邮箱 {email} 已存在")

        # 创建用户实体
        user = UserEntity(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return await self.user_repository.save(user)

    async def update_user_profile(self, user_id: str, **kwargs) -> UserEntity:
        """更新用户资料领域逻辑"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        # 更新用户信息
        user.update_profile(**kwargs)
        return await self.user_repository.update(user)

    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """修改密码领域逻辑"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        # 密码验证逻辑（在应用层处理）
        if user.password != old_password:
            raise ValueError("原密码不正确")

        user.password = new_password
        await self.user_repository.update(user)
        return True

    async def deactivate_user(self, user_id: str) -> UserEntity:
        """停用用户领域逻辑"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        user.deactivate()
        return await self.user_repository.update(user)

    async def activate_user(self, user_id: str) -> UserEntity:
        """激活用户领域逻辑"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        user.activate()
        return await self.user_repository.update(user)

    async def grant_permissions(
        self, user_id: str, is_staff: bool = False, is_superuser: bool = False
    ) -> UserEntity:
        """授予权限领域逻辑"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        if is_staff:
            user.grant_staff()
        if is_superuser:
            user.grant_superuser()

        return await self.user_repository.update(user)

    async def get_user_by_credentials(self, username: str, password: str) -> UserEntity | None:
        """凭据认证领域逻辑"""
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None

        if not user.is_active:
            raise ValueError("用户已被停用")

        # 密码验证（在应用层处理哈希比对）
        if user.password != password:
            return None

        # 更新最后登录时间
        user.update_last_login()
        await self.user_repository.update(user)

        return user
