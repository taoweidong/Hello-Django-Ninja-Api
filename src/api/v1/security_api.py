"""
安全API
Security API - 安全防护相关接口
"""

from ninja import Router
from pydantic import BaseModel

from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
)
from src.infrastructure.persistence.models.security_models import (
    IPBlacklist,
    IPWhitelist,
    RateLimitRule,
)

router = Router(tags=["安全"])


class MessageResponse(BaseModel):
    """消息响应"""

    message: str


# ========== IP黑名单管理 ==========


@router.post("/security/blacklist", response=IPBlacklistResponseDTO, summary="添加IP到黑名单")
async def add_to_blacklist(blacklist_dto: IPBlacklistDTO):
    """
    添加IP到黑名单
    - 禁止指定IP访问
    """
    # 检查是否已存在
    exists = await IPBlacklist.objects.filter(ip_address=blacklist_dto.ip_address).aexists()
    if exists:
        raise ValueError("IP已在黑名单中")

    entry = await IPBlacklist.objects.acreate(
        ip_address=blacklist_dto.ip_address,
        reason=blacklist_dto.reason,
        is_permanent=blacklist_dto.is_permanent,
        expires_at=blacklist_dto.expires_at,
    )

    return IPBlacklistResponseDTO(
        blacklist_id=str(entry.id),
        ip_address=entry.ip_address,
        reason=entry.reason,
        is_permanent=entry.is_permanent,
        expires_at=entry.expires_at,
        created_at=entry.created_at,
    )


@router.delete(
    "/security/blacklist/{ip_address}", response=MessageResponse, summary="从黑名单移除IP"
)
async def remove_from_blacklist(ip_address: str):
    """
    从黑名单移除IP
    - 解除IP的访问禁止
    """
    deleted_count, _ = await IPBlacklist.objects.filter(ip_address=ip_address).adelete()
    if deleted_count == 0:
        raise ValueError("IP不在黑名单中")
    return MessageResponse(message="IP已从黑名单移除")


@router.get("/security/blacklist", response=list[IPBlacklistResponseDTO], summary="获取黑名单列表")
async def list_blacklist():
    """
    获取黑名单列表
    - 获取所有黑名单IP
    """
    entries = await IPBlacklist.objects.all().alist()
    return [
        IPBlacklistResponseDTO(
            blacklist_id=str(e.id),
            ip_address=e.ip_address,
            reason=e.reason,
            is_permanent=e.is_permanent,
            expires_at=e.expires_at,
            created_at=e.created_at,
        )
        for e in entries
    ]


# ========== IP白名单管理 ==========


@router.post("/security/whitelist", response=IPWhitelistResponseDTO, summary="添加IP到白名单")
async def add_to_whitelist(whitelist_dto: IPWhitelistDTO):
    """
    添加IP到白名单
    - 允许指定IP访问（白名单模式下）
    """
    # 检查是否已存在
    exists = await IPWhitelist.objects.filter(ip_address=whitelist_dto.ip_address).aexists()
    if exists:
        raise ValueError("IP已在白名单中")

    entry = await IPWhitelist.objects.acreate(
        ip_address=whitelist_dto.ip_address,
        description=whitelist_dto.description,
    )

    return IPWhitelistResponseDTO(
        whitelist_id=str(entry.id),
        ip_address=entry.ip_address,
        description=entry.description,
        is_active=entry.is_active,
        created_at=entry.created_at,
    )


@router.delete(
    "/security/whitelist/{ip_address}", response=MessageResponse, summary="从白名单移除IP"
)
async def remove_from_whitelist(ip_address: str):
    """
    从白名单移除IP
    - 移除IP的访问许可
    """
    deleted_count, _ = await IPWhitelist.objects.filter(ip_address=ip_address).adelete()
    if deleted_count == 0:
        raise ValueError("IP不在白名单中")
    return MessageResponse(message="IP已从白名单移除")


@router.get("/security/whitelist", response=list[IPWhitelistResponseDTO], summary="获取白名单列表")
async def list_whitelist():
    """
    获取白名单列表
    - 获取所有白名单IP
    """
    entries = await IPWhitelist.objects.all().alist()
    return [
        IPWhitelistResponseDTO(
            whitelist_id=str(e.id),
            ip_address=e.ip_address,
            description=e.description,
            is_active=e.is_active,
            created_at=e.created_at,
        )
        for e in entries
    ]


# ========== 限流管理 ==========


@router.post("/security/rate-limit", response=RateLimitRuleResponseDTO, summary="创建限流规则")
async def create_rate_limit_rule(rule_dto: RateLimitRuleDTO):
    """
    创建限流规则
    - 为API端点创建访问频率限制
    """
    # 检查是否已存在
    exists = await RateLimitRule.objects.filter(
        endpoint=rule_dto.endpoint, method=rule_dto.method
    ).aexists()
    if exists:
        raise ValueError("该端点的限流规则已存在")

    rule = await RateLimitRule.objects.acreate(
        name=rule_dto.name,
        endpoint=rule_dto.endpoint,
        method=rule_dto.method,
        rate=rule_dto.rate,
        period=rule_dto.period,
        scope=rule_dto.scope,
        description=rule_dto.description,
    )

    return RateLimitRuleResponseDTO(
        limit_id=str(rule.id),
        name=rule.name,
        endpoint=rule.endpoint,
        method=rule.method,
        rate=rule.rate,
        period=rule.period,
        scope=rule.scope,
        is_active=rule.is_active,
        description=rule.description,
        created_at=rule.created_at,
    )


@router.put(
    "/security/rate-limit/{rule_id}/toggle",
    response=RateLimitRuleResponseDTO,
    summary="切换限流规则状态",
)
async def toggle_rate_limit_rule(rule_id: str):
    """
    切换限流规则状态
    - 启用或禁用限流规则
    """
    rule = await RateLimitRule.objects.aget(id=rule_id)
    rule.is_active = not rule.is_active
    await rule.asave()

    return RateLimitRuleResponseDTO(
        limit_id=str(rule.id),
        name=rule.name,
        endpoint=rule.endpoint,
        method=rule.method,
        rate=rule.rate,
        period=rule.period,
        scope=rule.scope,
        is_active=rule.is_active,
        description=rule.description,
        created_at=rule.created_at,
    )


@router.delete("/security/rate-limit/{rule_id}", response=MessageResponse, summary="删除限流规则")
async def delete_rate_limit_rule(rule_id: str):
    """
    删除限流规则
    - 删除指定的限流规则
    """
    deleted_count, _ = await RateLimitRule.objects.filter(id=rule_id).adelete()
    if deleted_count == 0:
        raise ValueError("限流规则不存在")
    return MessageResponse(message="限流规则删除成功")


@router.get(
    "/security/rate-limit", response=list[RateLimitRuleResponseDTO], summary="获取限流规则列表"
)
async def list_rate_limit_rules():
    """
    获取限流规则列表
    - 获取所有限流规则
    """
    rules = await RateLimitRule.objects.all().alist()
    return [
        RateLimitRuleResponseDTO(
            limit_id=str(r.id),
            name=r.name,
            endpoint=r.endpoint,
            method=r.method,
            rate=r.rate,
            period=r.period,
            scope=r.scope,
            is_active=r.is_active,
            description=r.description,
            created_at=r.created_at,
        )
        for r in rules
    ]


# ========== 安全状态 ==========


@router.get("/security/status", summary="获取安全状态")
async def get_security_status():
    """
    获取安全状态
    - 获取当前安全配置状态
    """
    blacklist_count = await IPBlacklist.objects.acount()
    whitelist_count = await IPWhitelist.objects.acount()
    rate_limit_count = await RateLimitRule.objects.filter(is_active=True).acount()

    return {
        "blacklist_enabled": True,
        "whitelist_enabled": False,
        "rate_limit_enabled": True,
        "blacklist_count": blacklist_count,
        "whitelist_count": whitelist_count,
        "rate_limit_count": rate_limit_count,
    }
