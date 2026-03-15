"""
限流领域服务
Rate Limit Domain Service - 处理API限流核心业务逻辑
"""

from datetime import timedelta

from src.domain.security.entities.rate_limit_entity import RateLimitEntity, RateLimitRecordEntity


class RateLimitDomainService:
    """
    限流领域服务
    处理API限流核心业务逻辑
    """

    def __init__(self):
        self.rules: dict[str, RateLimitEntity] = {}
        self.records: dict[str, RateLimitRecordEntity] = {}

    async def create_rate_limit_rule(
        self, name: str, endpoint: str, method: str = "GET", rate: int = 60, period: int = 60, scope: str = "ip", description: str = ""
    ) -> RateLimitEntity:
        """创建限流规则"""
        rule = RateLimitEntity(name=name, endpoint=endpoint, method=method, rate=rate, period=period, scope=scope, description=description)
        self.rules[f"{method}:{endpoint}"] = rule
        return rule

    async def get_rate_limit_rule(self, endpoint: str, method: str = "GET") -> RateLimitEntity | None:
        """获取限流规则"""
        return self.rules.get(f"{method}:{endpoint}")

    async def check_rate_limit(self, key: str, endpoint: str, method: str = "GET") -> tuple[bool, int]:
        """
        检查是否超过限流限制
        返回: (是否允许, 剩余次数)
        """
        rule = await self.get_rate_limit_rule(endpoint, method)
        if not rule or not rule.is_active:
            return True, -1  # 无规则，允许通过

        record_key = f"{key}:{method}:{endpoint}"
        record = self.records.get(record_key)

        # 检查记录是否过期
        if record and record.is_expired():
            record.reset()

        # 创建新记录
        if not record:
            record = RateLimitRecordEntity(key=key, endpoint=endpoint, method=method)
            self.records[record_key] = record

        # 检查限制
        current_count = record.increment()
        allowed = rule.check_limit(current_count)
        remaining = max(0, rule.rate - current_count)

        return allowed, remaining

    async def get_rate_limit_info(self, key: str, endpoint: str, method: str = "GET") -> dict:
        """获取限流信息"""
        rule = await self.get_rate_limit_rule(endpoint, method)
        if not rule or not rule.is_active:
            return {"enabled": False}

        record_key = f"{key}:{method}:{endpoint}"
        record = self.records.get(record_key)

        if record and record.is_expired():
            record.reset()

        current_count = record.count if record else 0
        remaining = max(0, rule.rate - current_count)
        reset_time = (record.window_start + timedelta(seconds=rule.period)) if record else None

        return {"enabled": True, "limit": rule.rate, "remaining": remaining, "reset_at": reset_time.isoformat() if reset_time else None}

    async def enable_rule(self, endpoint: str, method: str = "GET") -> bool:
        """启用限流规则"""
        rule = await self.get_rate_limit_rule(endpoint, method)
        if rule:
            rule.activate()
            return True
        return False

    async def disable_rule(self, endpoint: str, method: str = "GET") -> bool:
        """禁用限流规则"""
        rule = await self.get_rate_limit_rule(endpoint, method)
        if rule:
            rule.deactivate()
            return True
        return False

    async def list_rules(self) -> list:
        """列出所有限流规则"""
        return [rule.to_dict() for rule in self.rules.values()]
