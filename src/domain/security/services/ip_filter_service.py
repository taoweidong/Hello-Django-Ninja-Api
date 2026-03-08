"""
IP过滤领域服务
IP Filter Domain Service - 处理IP黑白名单核心业务逻辑
"""

from datetime import datetime

from src.domain.security.entities.ip_blacklist_entity import IPBlacklistEntity
from src.domain.security.entities.ip_whitelist_entity import IPWhitelistEntity


class IPFilterDomainService:
    """
    IP过滤领域服务
    处理IP黑白名单核心业务逻辑
    """

    def __init__(self):
        self.blacklist: dict[str, IPBlacklistEntity] = {}
        self.whitelist: dict[str, IPWhitelistEntity] = {}
        self.whitelist_enabled = False
        self.blacklist_enabled = False

    def enable_whitelist_mode(self, enabled: bool = True) -> None:
        """启用白名单模式"""
        self.whitelist_enabled = enabled

    def enable_blacklist_mode(self, enabled: bool = True) -> None:
        """启用黑名单模式"""
        self.blacklist_enabled = enabled

    # ========== 黑名单管理 ==========

    async def add_to_blacklist(
        self,
        ip_address: str,
        reason: str = "",
        is_permanent: bool = False,
        expires_at: datetime = None,
        created_by: str = None,
    ) -> IPBlacklistEntity:
        """添加IP到黑名单"""
        # 检查是否已存在
        existing = self.blacklist.get(ip_address)
        if existing and existing.is_active():
            raise ValueError(f"IP {ip_address} 已在黑名单中")

        entry = IPBlacklistEntity(
            ip_address=ip_address,
            reason=reason,
            is_permanent=is_permanent,
            expires_at=expires_at,
            created_by=created_by,
        )
        self.blacklist[ip_address] = entry
        return entry

    async def remove_from_blacklist(self, ip_address: str) -> bool:
        """从黑名单移除IP"""
        entry = self.blacklist.get(ip_address)
        if entry:
            entry.unban()
            return True
        return False

    async def is_blacklisted(self, ip_address: str) -> bool:
        """检查IP是否在黑名单中"""
        entry = self.blacklist.get(ip_address)
        if not entry:
            return False
        return entry.is_active()

    async def get_blacklist_entry(self, ip_address: str) -> IPBlacklistEntity | None:
        """获取黑名单条目"""
        return self.blacklist.get(ip_address)

    async def list_blacklist(self) -> list[dict]:
        """列出所有黑名单"""
        return [entry.to_dict() for entry in self.blacklist.values() if entry.is_active()]

    # ========== 白名单管理 ==========

    async def add_to_whitelist(
        self, ip_address: str, description: str = "", created_by: str = None
    ) -> IPWhitelistEntity:
        """添加IP到白名单"""
        existing = self.whitelist.get(ip_address)
        if existing and existing.is_active:
            raise ValueError(f"IP {ip_address} 已在白名单中")

        entry = IPWhitelistEntity(
            ip_address=ip_address,
            description=description,
            created_by=created_by,
        )
        self.whitelist[ip_address] = entry
        return entry

    async def remove_from_whitelist(self, ip_address: str) -> bool:
        """从白名单移除IP"""
        entry = self.whitelist.get(ip_address)
        if entry:
            entry.deactivate()
            return True
        return False

    async def is_whitelisted(self, ip_address: str) -> bool:
        """检查IP是否在白名单中"""
        entry = self.whitelist.get(ip_address)
        if not entry:
            return False
        return entry.is_active

    async def list_whitelist(self) -> list[dict]:
        """列出所有白名单"""
        return [entry.to_dict() for entry in self.whitelist.values() if entry.is_active]

    # ========== IP过滤 ==========

    async def check_ip(self, ip_address: str) -> tuple[bool, str]:
        """
        检查IP是否允许访问
        返回: (是否允许, 原因)
        """
        # 白名单优先
        if self.whitelist_enabled:
            if await self.is_whitelisted(ip_address):
                return True, "白名单允许"
            return False, "不在白名单中"

        # 黑名单检查
        if self.blacklist_enabled:
            if await self.is_blacklisted(ip_address):
                entry = await self.get_blacklist_entry(ip_address)
                return False, entry.reason if entry else "黑名单禁止"
            return True, "黑名单检查通过"

        # 默认允许
        return True, "默认允许"

    async def get_filter_status(self) -> dict:
        """获取过滤状态"""
        return {
            "whitelist_enabled": self.whitelist_enabled,
            "blacklist_enabled": self.blacklist_enabled,
            "blacklist_count": len([e for e in self.blacklist.values() if e.is_active()]),
            "whitelist_count": len([e for e in self.whitelist.values() if e.is_active]),
        }
