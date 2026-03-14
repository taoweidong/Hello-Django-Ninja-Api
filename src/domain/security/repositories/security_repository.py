"""
Security仓储接口
Security Repository Interface - 定义安全相关数据访问接口
"""

from abc import ABC, abstractmethod

from src.domain.security.entities.ip_blacklist_entity import IPBlacklistEntity
from src.domain.security.entities.ip_whitelist_entity import IPWhitelistEntity
from src.domain.security.entities.rate_limit_entity import RateLimitEntity, RateLimitRecordEntity


class SecurityRepository(ABC):
    """
    安全仓储接口
    定义安全相关数据访问的抽象接口
    """

    # ========== IP黑名单 ==========

    @abstractmethod
    async def add_to_blacklist(self, entity: IPBlacklistEntity) -> IPBlacklistEntity:
        """添加IP到黑名单"""
        pass

    @abstractmethod
    async def remove_from_blacklist(self, ip_address: str) -> bool:
        """从黑名单移除IP"""
        pass

    @abstractmethod
    async def get_blacklist_entry(self, ip_address: str) -> IPBlacklistEntity | None:
        """获取黑名单条目"""
        pass

    @abstractmethod
    async def is_blacklisted(self, ip_address: str) -> bool:
        """检查IP是否在黑名单中"""
        pass

    @abstractmethod
    async def list_blacklist(self, include_expired: bool = False) -> list[IPBlacklistEntity]:
        """列出黑名单"""
        pass

    # ========== IP白名单 ==========

    @abstractmethod
    async def add_to_whitelist(self, entity: IPWhitelistEntity) -> IPWhitelistEntity:
        """添加IP到白名单"""
        pass

    @abstractmethod
    async def remove_from_whitelist(self, ip_address: str) -> bool:
        """从白名单移除IP"""
        pass

    @abstractmethod
    async def get_whitelist_entry(self, ip_address: str) -> IPWhitelistEntity | None:
        """获取白名单条目"""
        pass

    @abstractmethod
    async def is_whitelisted(self, ip_address: str) -> bool:
        """检查IP是否在白名单中"""
        pass

    @abstractmethod
    async def list_whitelist(self, include_inactive: bool = False) -> list[IPWhitelistEntity]:
        """列出白名单"""
        pass

    # ========== 限流规则 ==========

    @abstractmethod
    async def create_rate_limit_rule(self, entity: RateLimitEntity) -> RateLimitEntity:
        """创建限流规则"""
        pass

    @abstractmethod
    async def get_rate_limit_rule(self, endpoint: str, method: str) -> RateLimitEntity | None:
        """获取限流规则"""
        pass

    @abstractmethod
    async def update_rate_limit_rule(self, entity: RateLimitEntity) -> RateLimitEntity:
        """更新限流规则"""
        pass

    @abstractmethod
    async def delete_rate_limit_rule(self, limit_id: str) -> bool:
        """删除限流规则"""
        pass

    @abstractmethod
    async def list_rate_limit_rules(self, is_active: bool | None = None) -> list[RateLimitEntity]:
        """列出限流规则"""
        pass

    # ========== 限流记录 ==========

    @abstractmethod
    async def get_or_create_rate_limit_record(
        self, key: str, endpoint: str, method: str, window_seconds: int
    ) -> RateLimitRecordEntity:
        """获取或创建限流记录"""
        pass

    @abstractmethod
    async def increment_rate_limit_count(self, record_id: str) -> int:
        """增加限流计数"""
        pass

    @abstractmethod
    async def reset_rate_limit_record(self, record_id: str) -> None:
        """重置限流记录"""
        pass
