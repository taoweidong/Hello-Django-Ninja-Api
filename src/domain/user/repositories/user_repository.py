"""
用户仓储接口定义
User Repository Interface - 定义数据访问契约
"""

from abc import ABC, abstractmethod

from src.domain.user.entities.user_entity import UserEntity


class UserRepositoryInterface(ABC):
    """
    用户仓储接口定义
    - 定义数据访问契约
    - 支持CRUD操作
    - 支持查询条件
    """

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """根据ID获取用户"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        """根据用户名获取用户"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        """根据邮箱获取用户"""
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity:
        """保存用户"""
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """更新用户"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """删除用户"""
        pass

    @abstractmethod
    async def list_all(self, page: int = 1, page_size: int = 10) -> list[UserEntity]:
        """获取用户列表"""
        pass

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """检查用户名是否存在"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """检查邮箱是否存在"""
        pass

    @abstractmethod
    async def count(self) -> int:
        """获取用户总数"""
        pass
