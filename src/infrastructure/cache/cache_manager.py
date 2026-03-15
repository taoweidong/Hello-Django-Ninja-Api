"""
缓存管理器
Cache Manager - 统一缓存管理
"""

import hashlib
import json
import logging
from typing import Any

from django.core.cache import cache

logger = logging.getLogger(__name__)


class CacheManager:
    """
    缓存管理器
    提供统一的缓存操作接口
    """

    # 缓存键前缀
    PREFIX = "hello_api"

    # 缓存分组
    GROUPS = {"user": "user", "rbac": "rbac", "auth": "auth", "security": "security", "system": "system"}

    @classmethod
    def _make_key(cls, key: str, group: str = None) -> str:
        """生成缓存键"""
        if group:
            return f"{cls.PREFIX}:{group}:{key}"
        return f"{cls.PREFIX}:{key}"

    @classmethod
    def get(cls, key: str, group: str = None, default: Any = None) -> Any:
        """获取缓存"""
        full_key = cls._make_key(key, group)
        try:
            value = cache.get(full_key)
            if value is None:
                return default
            # 尝试解析JSON
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return value
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return default

    @classmethod
    def set(cls, key: str, value: Any, timeout: int = 3600, group: str = None) -> bool:
        """设置缓存"""
        full_key = cls._make_key(key, group)
        try:
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                value = json.dumps(value, default=str)
            cache.set(full_key, value, timeout)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    @classmethod
    def delete(cls, key: str, group: str = None) -> bool:
        """删除缓存"""
        full_key = cls._make_key(key, group)
        try:
            cache.delete(full_key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    @classmethod
    def delete_pattern(cls, pattern: str, _group: str = None) -> int:
        """删除匹配的所有缓存（需要后端支持）"""
        # Django cache不一定支持pattern删除
        # 这里记录警告
        logger.warning(f"Pattern deletion not fully supported: {pattern}")
        return 0

    @classmethod
    def get_user_cache(cls, user_id: str) -> dict | None:
        """获取用户缓存"""
        return cls.get(f"user:{user_id}", group="user")

    @classmethod
    def set_user_cache(cls, user_id: str, data: dict, timeout: int = 1800) -> bool:
        """设置用户缓存"""
        return cls.set(f"user:{user_id}", data, timeout, group="user")

    @classmethod
    def delete_user_cache(cls, user_id: str) -> bool:
        """删除用户缓存"""
        return cls.delete(f"user:{user_id}", group="user")

    @classmethod
    def get_permissions_cache(cls, user_id: str) -> list[str] | None:
        """获取用户权限缓存"""
        return cls.get(f"permissions:{user_id}", group="rbac")

    @classmethod
    def set_permissions_cache(cls, user_id: str, permissions: list[str], timeout: int = 600) -> bool:
        """设置用户权限缓存"""
        return cls.set(f"permissions:{user_id}", permissions, timeout, group="rbac")

    @classmethod
    def delete_permissions_cache(cls, user_id: str) -> bool:
        """删除用户权限缓存"""
        return cls.delete(f"permissions:{user_id}", group="rbac")

    @classmethod
    def get_roles_cache(cls, user_id: str) -> list[dict] | None:
        """获取用户角色缓存"""
        return cls.get(f"roles:{user_id}", group="rbac")

    @classmethod
    def set_roles_cache(cls, user_id: str, roles: list[dict], timeout: int = 600) -> bool:
        """设置用户角色缓存"""
        return cls.set(f"roles:{user_id}", roles, timeout, group="rbac")

    @classmethod
    def delete_roles_cache(cls, user_id: str) -> bool:
        """删除用户角色缓存"""
        return cls.delete(f"roles:{user_id}", group="rbac")

    @classmethod
    def generate_cache_key(cls, *args, **kwargs) -> str:
        """根据参数生成缓存键"""
        key_data = "_".join(str(arg) for arg in args)
        key_data += "_".join(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()


# 全局实例
cache_manager = CacheManager()
