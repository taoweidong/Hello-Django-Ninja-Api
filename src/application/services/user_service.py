"""
用户服务
User Service - 用户业务逻辑处理
"""

import uuid

from django.contrib.auth.hashers import make_password

from src.application.dto.user import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.infrastructure.cache.cache_manager import cache_manager
from src.infrastructure.persistence.models.user_models import User
from src.infrastructure.repositories.user_repo_impl import UserRepositoryImpl


class UserService:
    """
    用户应用服务
    处理用户相关的业务逻辑
    """

    def __init__(self):
        self.user_repo = UserRepositoryImpl()

    def _hash_password(self, password: str) -> str:
        """密码哈希 - 使用Django的密码哈希"""
        return make_password(password)

    async def create_user(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        """创建用户"""
        # 检查用户名是否存在
        if await self.user_repo.exists_by_username(user_dto.username):
            raise ValueError(f"用户名 {user_dto.username} 已存在")

        # 检查邮箱是否存在
        if await self.user_repo.exists_by_email(user_dto.email):
            raise ValueError(f"邮箱 {user_dto.email} 已存在")

        # 创建用户 - 不指定id，让数据库自动生成
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            password=self._hash_password(user_dto.password),
            first_name=user_dto.first_name or "",
            last_name=user_dto.last_name or "",
            phone=user_dto.phone,
        )
        await user.asave()

        return self._to_response_dto(user)

    async def get_user_by_id(self, user_id: str) -> UserResponseDTO | None:
        """根据ID获取用户"""
        # 尝试从缓存获取
        cached = cache_manager.get_user_cache(user_id)
        if cached:
            return UserResponseDTO(**cached)

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None

        response = self._to_response_dto(user)
        # 缓存用户信息
        cache_manager.set_user_cache(user_id, response.model_dump())
        return response

    async def get_user_by_username(self, username: str) -> UserResponseDTO | None:
        """根据用户名获取用户"""
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None
        return self._to_response_dto(user)

    async def get_user_by_email(self, email: str) -> UserResponseDTO | None:
        """根据邮箱获取用户"""
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        return self._to_response_dto(user)

    async def update_user(self, user_id: str, user_dto: UserUpdateDTO) -> UserResponseDTO:
        """更新用户"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        # 更新字段
        update_data = user_dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await user.asave()

        # 清除缓存
        cache_manager.delete_user_cache(user_id)

        return self._to_response_dto(user)

    async def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        result = await self.user_repo.delete(user_id)
        if result:
            # 清除缓存
            cache_manager.delete_user_cache(user_id)
            cache_manager.delete_permissions_cache(user_id)
            cache_manager.delete_roles_cache(user_id)
        return result

    async def list_users(
        self, page: int = 1, page_size: int = 10
    ) -> tuple[list[UserResponseDTO], int]:
        """获取用户列表"""
        users = await self.user_repo.list_all(page, page_size)
        total = await self.user_repo.count()
        return [self._to_response_dto(user) for user in users], total

    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """修改密码"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        from django.contrib.auth.hashers import check_password
        if not check_password(old_password, user.password):
            raise ValueError("原密码不正确")

        user.password = make_password(new_password)
        await user.asave()
        return True

    async def authenticate(self, username: str, password: str) -> UserResponseDTO | None:
        """用户认证"""
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None

        if not user.is_active:
            raise ValueError("用户已被停用")

        from django.contrib.auth.hashers import check_password
        if not check_password(password, user.password):
            return None

        # 更新最后登录时间
        from django.utils import timezone

        user.last_login = timezone.now()
        await user.asave()

        return self._to_response_dto(user)

    def _to_response_dto(self, user) -> UserResponseDTO:
        """转换为响应DTO (支持User模型和UserEntity)"""
        # 处理 UserEntity 对象
        if hasattr(user, 'user_id'):
            return UserResponseDTO(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
                avatar=user.avatar,
                phone=user.phone,
                bio=user.bio,
                date_joined=user.date_joined,
                last_login=user.last_login,
            )
        # 处理 User 模型对象
        else:
            return UserResponseDTO(
                user_id=str(user.id),
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
                avatar=user.avatar,
                phone=user.phone,
                bio=getattr(user, 'bio', None),
                date_joined=user.date_joined,
                last_login=user.last_login,
            )


# 全局实例
user_service = UserService()
