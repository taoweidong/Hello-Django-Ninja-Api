"""
缓存清理策略
Cache Clear Strategies - 统一的缓存清理策略模式实现
"""

from abc import ABC, abstractmethod
from typing import List


class CacheClearStrategy(ABC):
    """
    缓存清理策略基类
    定义缓存清理的接口
    """

    @abstractmethod
    def clear_user_cache(self, user_id: str) -> None:
        """
        清理用户缓存

        参数:
            user_id: 用户ID
        """
        pass

    @abstractmethod
    def clear_permissions_cache(self, user_id: str) -> None:
        """
        清理权限缓存

        参数:
            user_id: 用户ID
        """
        pass

    @abstractmethod
    def clear_roles_cache(self, user_id: str) -> None:
        """
        清理角色缓存

        参数:
            user_id: 用户ID
        """
        pass


class AllCacheStrategy(CacheClearStrategy):
    """
    清理所有缓存策略
    清理用户信息、权限、角色等所有相关缓存
    """

    def clear_user_cache(self, user_id: str) -> None:
        """清理用户信息缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_user_cache(user_id)

    def clear_permissions_cache(self, user_id: str) -> None:
        """清理权限缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_permissions_cache(user_id)

    def clear_roles_cache(self, user_id: str) -> None:
        """清理角色缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_roles_cache(user_id)

    def clear_user_cache(self, user_id: str) -> None:
        """
        清理用户所有缓存（重写父类方法）
        一次性清理所有相关缓存
        """
        self.clear_user_cache(user_id)
        self.clear_permissions_cache(user_id)
        self.clear_roles_cache(user_id)


class PermissionOnlyStrategy(CacheClearStrategy):
    """
    只清理权限缓存策略
    仅清理权限和角色缓存，保留用户信息缓存
    """

    def clear_user_cache(self, user_id: str) -> None:
        """不清理用户信息缓存"""
        pass

    def clear_permissions_cache(self, user_id: str) -> None:
        """清理权限缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_permissions_cache(user_id)

    def clear_roles_cache(self, user_id: str) -> None:
        """清理角色缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_roles_cache(user_id)


class UserOnlyStrategy(CacheClearStrategy):
    """
    只清理用户缓存策略
    仅清理用户信息缓存，保留权限和角色缓存
    """

    def clear_user_cache(self, user_id: str) -> None:
        """清理用户信息缓存"""
        from src.infrastructure.cache.cache_manager import cache_manager

        cache_manager.delete_user_cache(user_id)

    def clear_permissions_cache(self, user_id: str) -> None:
        """不清理权限缓存"""
        pass

    def clear_roles_cache(self, user_id: str) -> None:
        """不清理角色缓存"""
        pass


class SelectiveCacheStrategy(CacheClearStrategy):
    """
    选择性缓存清理策略
    根据配置选择性清理特定缓存
    """

    def __init__(
        self,
        clear_user: bool = True,
        clear_permissions: bool = True,
        clear_roles: bool = True,
    ):
        """
        初始化选择性缓存策略

        参数:
            clear_user: 是否清理用户缓存
            clear_permissions: 是否清理权限缓存
            clear_roles: 是否清理角色缓存
        """
        self._clear_user = clear_user
        self._clear_permissions = clear_permissions
        self._clear_roles = clear_roles

    def clear_user_cache(self, user_id: str) -> None:
        """根据配置清理用户缓存"""
        if self._clear_user:
            from src.infrastructure.cache.cache_manager import cache_manager

            cache_manager.delete_user_cache(user_id)

    def clear_permissions_cache(self, user_id: str) -> None:
        """根据配置清理权限缓存"""
        if self._clear_permissions:
            from src.infrastructure.cache.cache_manager import cache_manager

            cache_manager.delete_permissions_cache(user_id)

    def clear_roles_cache(self, user_id: str) -> None:
        """根据配置清理角色缓存"""
        if self._clear_roles:
            from src.infrastructure.cache.cache_manager import cache_manager

            cache_manager.delete_roles_cache(user_id)


class CacheManagerAdapter:
    """
    缓存管理器适配器
    使用策略模式管理缓存清理
    """

    def __init__(self, strategy: CacheClearStrategy = None):
        """
        初始化缓存管理器适配器

        参数:
            strategy: 缓存清理策略，默认使用AllCacheStrategy
        """
        self._strategy = strategy or AllCacheStrategy()

    def set_strategy(self, strategy: CacheClearStrategy) -> None:
        """
        设置缓存清理策略

        参数:
            strategy: 新的缓存清理策略
        """
        self._strategy = strategy

    def clear_user(self, user_id: str) -> None:
        """
        清理用户缓存（使用当前策略）

        参数:
            user_id: 用户ID
        """
        self._strategy.clear_user_cache(user_id)

    def clear_permissions(self, user_id: str) -> None:
        """
        清理权限缓存（使用当前策略）

        参数:
            user_id: 用户ID
        """
        self._strategy.clear_permissions_cache(user_id)

    def clear_roles(self, user_id: str) -> None:
        """
        清理角色缓存（使用当前策略）

        参数:
            user_id: 用户ID
        """
        self._strategy.clear_roles_cache(user_id)

    def clear_all(self, user_id: str) -> None:
        """
        清理所有缓存（使用当前策略）

        参数:
            user_id: 用户ID
        """
        self.clear_user(user_id)
        self.clear_permissions(user_id)
        self.clear_roles(user_id)

    def clear_batch(self, user_ids: List[str]) -> None:
        """
        批量清理用户缓存

        参数:
            user_ids: 用户ID列表
        """
        for user_id in user_ids:
            self.clear_all(user_id)


# 全局实例，默认使用全缓存清理策略
cache_adapter = CacheManagerAdapter()
