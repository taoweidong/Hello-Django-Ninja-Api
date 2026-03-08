"""
Redis缓存实现
Redis Cache - 基于Redis的缓存实现
"""

import json
import logging
from typing import Any

from django.core.cache import cache

logger = logging.getLogger(__name__)


class RedisCache:
    """
    Redis缓存封装类
    提供常用的缓存操作方法
    """

    # 缓存前缀
    PREFIX = "hello_api"

    # 默认过期时间（秒）
    DEFAULT_TIMEOUT = 3600

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        获取缓存值
        """
        try:
            full_key = f"{cls.PREFIX}:{key}"
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
    def set(cls, key: str, value: Any, timeout: int = None) -> bool:
        """
        设置缓存值
        """
        try:
            full_key = f"{cls.PREFIX}:{key}"
            timeout = timeout or cls.DEFAULT_TIMEOUT

            # 如果是复杂对象，序列化为JSON
            if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                value = json.dumps(value, default=str)

            cache.set(full_key, value, timeout)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    @classmethod
    def delete(cls, key: str) -> bool:
        """
        删除缓存
        """
        try:
            full_key = f"{cls.PREFIX}:{key}"
            cache.delete(full_key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    @classmethod
    def exists(cls, key: str) -> bool:
        """
        检查缓存键是否存在
        """
        try:
            full_key = f"{cls.PREFIX}:{key}"
            return cache.get(full_key) is not None
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False

    @classmethod
    def get_many(cls, keys: list) -> dict:
        """
        批量获取缓存
        """
        try:
            full_keys = [f"{cls.PREFIX}:{key}" for key in keys]
            result = cache.get_many(full_keys)
            # 移除前缀
            return {k.replace(f"{cls.PREFIX}:", ""): v for k, v in result.items()}
        except Exception as e:
            logger.error(f"Cache get_many error: {e}")
            return {}

    @classmethod
    def set_many(cls, data_dict: dict, timeout: int = None) -> bool:
        """
        批量设置缓存
        """
        try:
            timeout = timeout or cls.DEFAULT_TIMEOUT
            full_data = {f"{cls.PREFIX}:{k}": v for k, v in data_dict.items()}
            cache.set_many(full_data, timeout)
            return True
        except Exception as e:
            logger.error(f"Cache set_many error: {e}")
            return False

    @classmethod
    def clear(cls) -> bool:
        """
        清空所有缓存（仅限本项目前缀）
        """
        try:
            # 注意：Django的cache没有直接清空的方法
            # 这里只清理本项目的缓存键需要结合具体后端实现
            logger.warning("Clear all cache not implemented for safety")
            return False
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    @classmethod
    def increment(cls, key: str, delta: int = 1) -> int | None:
        """
        增加缓存值
        """
        try:
            full_key = f"{cls.PREFIX}:{key}"
            value = cache.get(full_key)
            value = 0 if value is None else int(value) + delta
            cache.set(full_key, value, cls.DEFAULT_TIMEOUT)
            return value
        except Exception as e:
            logger.error(f"Cache increment error: {e}")
            return None


# 便捷函数
def cache_get(key: str, default: Any = None) -> Any:
    """获取缓存"""
    return RedisCache.get(key, default)


def cache_set(key: str, value: Any, timeout: int = None) -> bool:
    """设置缓存"""
    return RedisCache.set(key, value, timeout)


def cache_delete(key: str) -> bool:
    """删除缓存"""
    return RedisCache.delete(key)


def cache_exists(key: str) -> bool:
    """检查缓存是否存在"""
    return RedisCache.exists(key)
