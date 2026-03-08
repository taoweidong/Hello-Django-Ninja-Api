"""
安全控制器
Security Controller - 安全管理API控制器
"""

from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
)
from src.application.services.security_service import SecurityService


class SecurityController:
    """
    安全控制器
    处理安全管理相关API请求
    """

    def __init__(self, security_service: SecurityService = None):
        self._security_service = security_service or SecurityService()

    # ========== IP黑名单管理 ==========

    async def add_to_blacklist(
        self, blacklist_dto: IPBlacklistDTO, created_by: str = None
    ) -> IPBlacklistResponseDTO:
        """添加IP到黑名单"""
        return await self._security_service.add_to_blacklist(blacklist_dto, created_by)

    async def remove_from_blacklist(self, ip_address: str) -> bool:
        """从黑名单移除IP"""
        result = await self._security_service.remove_from_blacklist(ip_address)
        if not result:
            raise ValueError("IP不在黑名单中")
        return result

    async def list_blacklist(self) -> list[IPBlacklistResponseDTO]:
        """获取黑名单列表"""
        return await self._security_service.list_blacklist()

    # ========== IP白名单管理 ==========

    async def add_to_whitelist(
        self, whitelist_dto: IPWhitelistDTO, created_by: str = None
    ) -> IPWhitelistResponseDTO:
        """添加IP到白名单"""
        return await self._security_service.add_to_whitelist(whitelist_dto, created_by)

    async def remove_from_whitelist(self, ip_address: str) -> bool:
        """从白名单移除IP"""
        result = await self._security_service.remove_from_whitelist(ip_address)
        if not result:
            raise ValueError("IP不在白名单中")
        return result

    async def list_whitelist(self) -> list[IPWhitelistResponseDTO]:
        """获取白名单列表"""
        return await self._security_service.list_whitelist()

    # ========== 限流规则管理 ==========

    async def create_rate_limit_rule(self, rule_dto: RateLimitRuleDTO) -> RateLimitRuleResponseDTO:
        """创建限流规则"""
        return await self._security_service.create_rate_limit_rule(rule_dto)

    async def toggle_rate_limit_rule(self, rule_id: str) -> RateLimitRuleResponseDTO:
        """切换限流规则状态"""
        return await self._security_service.toggle_rate_limit_rule(rule_id)

    async def delete_rate_limit_rule(self, rule_id: str) -> bool:
        """删除限流规则"""
        result = await self._security_service.delete_rate_limit_rule(rule_id)
        if not result:
            raise ValueError("限流规则不存在")
        return result

    async def list_rate_limit_rules(self) -> list[RateLimitRuleResponseDTO]:
        """获取限流规则列表"""
        return await self._security_service.list_rate_limit_rules()

    # ========== 安全状态 ==========

    async def get_security_status(self) -> dict:
        """获取安全状态"""
        return await self._security_service.get_security_status()
