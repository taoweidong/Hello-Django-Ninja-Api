"""
Security仓储实现
Security Repository Implementation - 实现安全相关数据访问
"""

import uuid
from datetime import datetime, timedelta

from src.domain.security.entities.ip_blacklist_entity import IPBlacklistEntity
from src.domain.security.entities.ip_whitelist_entity import IPWhitelistEntity
from src.domain.security.entities.rate_limit_entity import RateLimitEntity, RateLimitRecordEntity
from src.domain.security.repositories.security_repository import SecurityRepository
from src.infrastructure.persistence.models.security_models import IPBlacklist, IPWhitelist, RateLimitRecord, RateLimitRule


class SecurityRepositoryImpl(SecurityRepository):
    """
    安全仓储实现
    实现安全相关数据访问
    """

    # ========== IP黑名单 ==========

    async def add_to_blacklist(self, entity: IPBlacklistEntity) -> IPBlacklistEntity:
        """添加IP到黑名单"""
        model = await IPBlacklist.objects.acreate(
            id=uuid.UUID(entity.blacklist_id),
            ip_address=entity.ip_address,
            reason=entity.reason,
            is_permanent=entity.is_permanent,
            expires_at=entity.expires_at,
            created_by_id=entity.created_by,
        )
        return self._blacklist_model_to_entity(model)

    async def remove_from_blacklist(self, ip_address: str) -> bool:
        """从黑名单移除IP"""
        deleted_count, _ = await IPBlacklist.objects.filter(ip_address=ip_address).adelete()
        return deleted_count > 0

    async def get_blacklist_entry(self, ip_address: str) -> IPBlacklistEntity | None:
        """获取黑名单条目"""
        try:
            model = await IPBlacklist.objects.aget(ip_address=ip_address)
            return self._blacklist_model_to_entity(model)
        except IPBlacklist.DoesNotExist:
            return None

    async def is_blacklisted(self, ip_address: str) -> bool:
        """检查IP是否在黑名单中"""
        try:
            model = await IPBlacklist.objects.aget(ip_address=ip_address)
            return model.is_active()
        except IPBlacklist.DoesNotExist:
            return False

    async def list_blacklist(self, include_expired: bool = False) -> list[IPBlacklistEntity]:
        """列出黑名单"""
        queryset = IPBlacklist.objects.all()
        if not include_expired:
            queryset = queryset.filter(is_permanent=True) | queryset.filter(expires_at__gt=datetime.now())
        models = [m async for m in queryset]
        return [self._blacklist_model_to_entity(m) for m in models]

    # ========== IP白名单 ==========

    async def add_to_whitelist(self, entity: IPWhitelistEntity) -> IPWhitelistEntity:
        """添加IP到白名单"""
        model = await IPWhitelist.objects.acreate(
            id=uuid.UUID(entity.whitelist_id),
            ip_address=entity.ip_address,
            description=entity.description,
            is_active=entity.is_active,
            created_by_id=entity.created_by,
        )
        return self._whitelist_model_to_entity(model)

    async def remove_from_whitelist(self, ip_address: str) -> bool:
        """从白名单移除IP"""
        deleted_count, _ = await IPWhitelist.objects.filter(ip_address=ip_address).adelete()
        return deleted_count > 0

    async def get_whitelist_entry(self, ip_address: str) -> IPWhitelistEntity | None:
        """获取白名单条目"""
        try:
            model = await IPWhitelist.objects.aget(ip_address=ip_address)
            return self._whitelist_model_to_entity(model)
        except IPWhitelist.DoesNotExist:
            return None

    async def is_whitelisted(self, ip_address: str) -> bool:
        """检查IP是否在白名单中"""
        return await IPWhitelist.objects.filter(ip_address=ip_address, is_active=True).aexists()

    async def list_whitelist(self, include_inactive: bool = False) -> list[IPWhitelistEntity]:
        """列出白名单"""
        queryset = IPWhitelist.objects.all()
        if not include_inactive:
            queryset = queryset.filter(is_active=True)
        models = [m async for m in queryset]
        return [self._whitelist_model_to_entity(m) for m in models]

    # ========== 限流规则 ==========

    async def create_rate_limit_rule(self, entity: RateLimitEntity) -> RateLimitEntity:
        """创建限流规则"""
        model = await RateLimitRule.objects.acreate(
            id=uuid.UUID(entity.limit_id),
            name=entity.name,
            endpoint=entity.endpoint,
            method=entity.method,
            rate=entity.rate,
            period=entity.period,
            scope=entity.scope,
            description=entity.description,
            is_active=entity.is_active,
        )
        return self._rate_limit_model_to_entity(model)

    async def get_rate_limit_rule(self, endpoint: str, method: str) -> RateLimitEntity | None:
        """获取限流规则"""
        try:
            model = await RateLimitRule.objects.aget(endpoint=endpoint, method=method)
            return self._rate_limit_model_to_entity(model)
        except RateLimitRule.DoesNotExist:
            return None

    async def update_rate_limit_rule(self, entity: RateLimitEntity) -> RateLimitEntity:
        """更新限流规则"""
        model = await RateLimitRule.objects.aget(id=uuid.UUID(entity.limit_id))
        model.name = entity.name
        model.rate = entity.rate
        model.period = entity.period
        model.scope = entity.scope
        model.description = entity.description
        model.is_active = entity.is_active
        await model.asave()
        return self._rate_limit_model_to_entity(model)

    async def delete_rate_limit_rule(self, limit_id: str) -> bool:
        """删除限流规则"""
        deleted_count, _ = await RateLimitRule.objects.filter(id=uuid.UUID(limit_id)).adelete()
        return deleted_count > 0

    async def list_rate_limit_rules(self, is_active: bool | None = None) -> list[RateLimitEntity]:
        """列出限流规则"""
        queryset = RateLimitRule.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        models = [m async for m in queryset]
        return [self._rate_limit_model_to_entity(m) for m in models]

    # ========== 限流记录 ==========

    async def get_or_create_rate_limit_record(self, key: str, endpoint: str, method: str, window_seconds: int) -> RateLimitRecordEntity:
        """获取或创建限流记录"""
        now = datetime.now()
        expires_at = now + timedelta(seconds=window_seconds)

        try:
            model = await RateLimitRecord.objects.aget(key=key, endpoint=endpoint, method=method)
            # 检查是否过期
            if model.expires_at < now:
                model.count = 0
                model.window_start = now
                model.expires_at = expires_at
                await model.asave()
            return self._rate_limit_record_model_to_entity(model)
        except RateLimitRecord.DoesNotExist:
            model = await RateLimitRecord.objects.acreate(
                id=uuid.uuid4(), key=key, endpoint=endpoint, method=method, count=0, window_start=now, expires_at=expires_at
            )
            return self._rate_limit_record_model_to_entity(model)

    async def increment_rate_limit_count(self, record_id: str) -> int:
        """增加限流计数"""
        model = await RateLimitRecord.objects.aget(id=uuid.UUID(record_id))
        model.count += 1
        await model.asave()
        return model.count

    async def reset_rate_limit_record(self, record_id: str) -> None:
        """重置限流记录"""
        model = await RateLimitRecord.objects.aget(id=uuid.UUID(record_id))
        model.count = 0
        model.window_start = datetime.now()
        await model.asave()

    # ========== 辅助方法 ==========

    def _blacklist_model_to_entity(self, model: IPBlacklist) -> IPBlacklistEntity:
        """黑名单模型转实体"""
        return IPBlacklistEntity(
            blacklist_id=str(model.id),
            ip_address=model.ip_address,
            reason=model.reason or "",
            is_permanent=model.is_permanent,
            expires_at=model.expires_at,
            created_at=model.created_at,
            created_by=str(model.created_by_id) if model.created_by_id else None,
        )

    def _whitelist_model_to_entity(self, model: IPWhitelist) -> IPWhitelistEntity:
        """白名单模型转实体"""
        return IPWhitelistEntity(
            whitelist_id=str(model.id),
            ip_address=model.ip_address,
            description=model.description or "",
            is_active=model.is_active,
            created_at=model.created_at,
            created_by=str(model.created_by_id) if model.created_by_id else None,
        )

    def _rate_limit_model_to_entity(self, model: RateLimitRule) -> RateLimitEntity:
        """限流规则模型转实体"""
        return RateLimitEntity(
            limit_id=str(model.id),
            name=model.name,
            endpoint=model.endpoint,
            method=model.method,
            rate=model.rate,
            period=model.period,
            scope=model.scope,
            is_active=model.is_active,
            description=model.description or "",
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _rate_limit_record_model_to_entity(self, model: RateLimitRecord) -> RateLimitRecordEntity:
        """限流记录模型转实体"""
        return RateLimitRecordEntity(
            record_id=str(model.id),
            key=model.key,
            endpoint=model.endpoint,
            method=model.method,
            count=model.count,
            window_start=model.window_start,
            expires_at=model.expires_at,
        )


# 全局实例
security_repository = SecurityRepositoryImpl()
