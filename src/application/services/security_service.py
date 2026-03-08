"""
Security服务
Security Service - 安全相关业务逻辑处理
"""

from datetime import datetime

from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
    RateLimitStatusDTO,
)
from src.domain.security.entities.ip_blacklist_entity import IPBlacklistEntity
from src.domain.security.entities.ip_whitelist_entity import IPWhitelistEntity
from src.domain.security.entities.rate_limit_entity import RateLimitEntity
from src.domain.security.repositories.security_repository import SecurityRepository
from src.infrastructure.repositories.security_repo_impl import SecurityRepositoryImpl


class SecurityService:
    """
    安全应用服务
    处理IP黑白名单和限流相关业务逻辑
    """

    def __init__(self, repository: SecurityRepository = None):
        self._repository = repository or SecurityRepositoryImpl()

    # ========== IP黑名单管理 ==========

    async def add_to_blacklist(
        self, dto: IPBlacklistDTO, created_by: str = None
    ) -> IPBlacklistResponseDTO:
        """添加IP到黑名单"""
        # 检查是否已存在
        existing = await self._repository.get_blacklist_entry(dto.ip_address)
        if existing and existing.is_active():
            raise ValueError(f"IP {dto.ip_address} 已在黑名单中")

        entity = IPBlacklistEntity(
            ip_address=dto.ip_address,
            reason=dto.reason or "",
            is_permanent=dto.is_permanent,
            expires_at=dto.expires_at,
            created_by=created_by,
        )

        saved_entity = await self._repository.add_to_blacklist(entity)
        return self._to_blacklist_response(saved_entity)

    async def remove_from_blacklist(self, ip_address: str) -> bool:
        """从黑名单移除IP"""
        return await self._repository.remove_from_blacklist(ip_address)

    async def get_blacklist_entry(self, ip_address: str) -> IPBlacklistResponseDTO | None:
        """获取黑名单条目"""
        entity = await self._repository.get_blacklist_entry(ip_address)
        if not entity:
            return None
        return self._to_blacklist_response(entity)

    async def list_blacklist(self) -> list[IPBlacklistResponseDTO]:
        """获取黑名单列表"""
        entities = await self._repository.list_blacklist()
        return [self._to_blacklist_response(e) for e in entities]

    # ========== IP白名单管理 ==========

    async def add_to_whitelist(
        self, dto: IPWhitelistDTO, created_by: str = None
    ) -> IPWhitelistResponseDTO:
        """添加IP到白名单"""
        # 检查是否已存在
        existing = await self._repository.get_whitelist_entry(dto.ip_address)
        if existing and existing.is_active:
            raise ValueError(f"IP {dto.ip_address} 已在白名单中")

        entity = IPWhitelistEntity(
            ip_address=dto.ip_address,
            description=dto.description or "",
            is_active=True,
            created_by=created_by,
        )

        saved_entity = await self._repository.add_to_whitelist(entity)
        return self._to_whitelist_response(saved_entity)

    async def remove_from_whitelist(self, ip_address: str) -> bool:
        """从白名单移除IP"""
        return await self._repository.remove_from_whitelist(ip_address)

    async def list_whitelist(self) -> list[IPWhitelistResponseDTO]:
        """获取白名单列表"""
        entities = await self._repository.list_whitelist()
        return [self._to_whitelist_response(e) for e in entities]

    # ========== 限流规则管理 ==========

    async def create_rate_limit_rule(self, dto: RateLimitRuleDTO) -> RateLimitRuleResponseDTO:
        """创建限流规则"""
        # 检查是否已存在
        existing = await self._repository.get_rate_limit_rule(dto.endpoint, dto.method)
        if existing:
            raise ValueError(f"端点 {dto.method}:{dto.endpoint} 的限流规则已存在")

        entity = RateLimitEntity(
            name=dto.name,
            endpoint=dto.endpoint,
            method=dto.method,
            rate=dto.rate,
            period=dto.period,
            scope=dto.scope,
            description=dto.description or "",
            is_active=True,
        )

        saved_entity = await self._repository.create_rate_limit_rule(entity)
        return self._to_rate_limit_response(saved_entity)

    async def toggle_rate_limit_rule(self, limit_id: str) -> RateLimitRuleResponseDTO:
        """切换限流规则状态"""
        rules = await self._repository.list_rate_limit_rules()
        rule = next((r for r in rules if r.limit_id == limit_id), None)
        if not rule:
            raise ValueError("限流规则不存在")

        rule.is_active = not rule.is_active
        rule.updated_at = datetime.now()
        updated_entity = await self._repository.update_rate_limit_rule(rule)
        return self._to_rate_limit_response(updated_entity)

    async def delete_rate_limit_rule(self, limit_id: str) -> bool:
        """删除限流规则"""
        return await self._repository.delete_rate_limit_rule(limit_id)

    async def list_rate_limit_rules(self) -> list[RateLimitRuleResponseDTO]:
        """获取限流规则列表"""
        entities = await self._repository.list_rate_limit_rules()
        return [self._to_rate_limit_response(e) for e in entities]

    async def get_rate_limit_status(self, key: str, endpoint: str, method: str) -> RateLimitStatusDTO:
        """获取限流状态"""
        rule = await self._repository.get_rate_limit_rule(endpoint, method)
        if not rule or not rule.is_active:
            return RateLimitStatusDTO(enabled=False, limit=None, remaining=None, reset_at=None)

        record = await self._repository.get_or_create_rate_limit_record(
            key=key, endpoint=endpoint, method=method, window_seconds=rule.period
        )

        remaining = max(0, rule.rate - record.count)
        reset_at = record.window_start.isoformat() if record.window_start else None

        return RateLimitStatusDTO(
            enabled=True,
            limit=rule.rate,
            remaining=remaining,
            reset_at=reset_at,
        )

    # ========== 安全状态 ==========

    async def get_security_status(self) -> dict:
        """获取安全状态"""
        blacklist = await self._repository.list_blacklist()
        whitelist = await self._repository.list_whitelist()
        active_rules = await self._repository.list_rate_limit_rules(is_active=True)

        return {
            "blacklist_enabled": True,
            "whitelist_enabled": False,
            "rate_limit_enabled": True,
            "blacklist_count": len(blacklist),
            "whitelist_count": len(whitelist),
            "rate_limit_count": len(active_rules),
        }

    # ========== 辅助方法 ==========

    def _to_blacklist_response(self, entity: IPBlacklistEntity) -> IPBlacklistResponseDTO:
        """转换为黑名单响应DTO"""
        return IPBlacklistResponseDTO(
            blacklist_id=entity.blacklist_id,
            ip_address=entity.ip_address,
            reason=entity.reason,
            is_permanent=entity.is_permanent,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

    def _to_whitelist_response(self, entity: IPWhitelistEntity) -> IPWhitelistResponseDTO:
        """转换为白名单响应DTO"""
        return IPWhitelistResponseDTO(
            whitelist_id=entity.whitelist_id,
            ip_address=entity.ip_address,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

    def _to_rate_limit_response(self, entity: RateLimitEntity) -> RateLimitRuleResponseDTO:
        """转换为限流规则响应DTO"""
        return RateLimitRuleResponseDTO(
            limit_id=entity.limit_id,
            name=entity.name,
            endpoint=entity.endpoint,
            method=entity.method,
            rate=entity.rate,
            period=entity.period,
            scope=entity.scope,
            is_active=entity.is_active,
            description=entity.description,
            created_at=entity.created_at,
        )


# 全局实例
security_service = SecurityService()
