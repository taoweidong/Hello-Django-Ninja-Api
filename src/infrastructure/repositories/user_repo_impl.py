"""
用户仓储实现
User Repository Implementation - 用户数据持久化实现
"""

import uuid

from src.domain.user.entities.user_entity import UserEntity
from src.domain.user.repositories.user_repository import UserRepositoryInterface
from src.infrastructure.persistence.models.user_models import User


class UserRepositoryImpl(UserRepositoryInterface):
    """
    用户仓储实现
    负责用户数据的数据库操作
    """

    def _to_entity(self, user_model: User) -> UserEntity:
        """模型转换为实体"""
        return UserEntity(
            user_id=str(user_model.id),
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            is_active=user_model.is_active,
            is_staff=user_model.is_staff,
            is_superuser=user_model.is_superuser,
            date_joined=user_model.date_joined,
            last_login=user_model.last_login,
            avatar=user_model.avatar,
            phone=user_model.phone,
            bio=getattr(user_model, "bio", None),
        )

    def _to_model(self, entity: UserEntity) -> User:
        """实体转换为模型"""
        if entity.user_id:
            try:
                user = User.objects.get(id=entity.user_id)
                user.username = entity.username
                user.email = entity.email
                user.first_name = entity.first_name
                user.last_name = entity.last_name
                user.is_active = entity.is_active
                user.is_staff = entity.is_staff
                user.is_superuser = entity.is_superuser
                user.avatar = entity.avatar
                user.phone = entity.phone
                # bio 字段不在 User 模型中,跳过
                return user
            except User.DoesNotExist:
                pass

        return User(
            id=uuid.UUID(entity.user_id) if entity.user_id else uuid.uuid4(),
            username=entity.username,
            email=entity.email,
            password=entity.password,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            is_staff=entity.is_staff,
            is_superuser=entity.is_superuser,
            avatar=entity.avatar,
            phone=entity.phone,
            # bio 字段不在 User 模型中,跳过
        )

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """根据ID获取用户"""
        try:
            user = await User.objects.aget(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    async def get_by_username(self, username: str) -> UserEntity | None:
        """根据用户名获取用户"""
        try:
            user = await User.objects.aget(username=username)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    async def get_by_email(self, email: str) -> UserEntity | None:
        """根据邮箱获取用户"""
        try:
            user = await User.objects.aget(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    async def save(self, user: UserEntity) -> UserEntity:
        """保存用户"""
        user_model = self._to_model(user)
        await user_model.asave()
        return user

    async def update(self, user: UserEntity) -> UserEntity:
        """更新用户"""
        user_model = self._to_model(user)
        await user_model.asave()
        return user

    async def delete(self, user_id: str) -> bool:
        """删除用户"""
        try:
            user = await User.objects.aget(id=user_id)
            await user.adelete()
            return True
        except User.DoesNotExist:
            return False

    async def list_all(self, page: int = 1, page_size: int = 10) -> list[UserEntity]:
        """获取用户列表"""
        offset = (page - 1) * page_size
        # 使用 async iterator 获取分页数据
        queryset = User.objects.all()[offset : offset + page_size]
        users = [user async for user in queryset]
        return [self._to_entity(user) for user in users]

    async def exists_by_username(self, username: str) -> bool:
        """检查用户名是否存在"""
        return await User.objects.filter(username=username).aexists()

    async def exists_by_email(self, email: str) -> bool:
        """检查邮箱是否存在"""
        return await User.objects.filter(email=email).aexists()

    async def count(self) -> int:
        """获取用户总数"""
        return await User.objects.acount()


# 全局实例
user_repository = UserRepositoryImpl()
