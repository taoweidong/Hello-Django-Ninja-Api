"""
限流实体
Rate Limit Entity - API限流实体
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class RateLimitEntity:
    """
    限流实体
    定义API访问频率限制规则
    """

    limit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""  # 规则名称
    endpoint: str = ""  # API端点，如 '/api/users'
    method: str = "GET"  # HTTP方法
    rate: int = 60  # 允许的请求次数
    period: int = 60  # 时间周期（秒）
    scope: str = "ip"  # 限流范围：ip, user, global
    is_active: bool = True
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.name:
            raise ValueError("限流规则名称不能为空")
        if not self.endpoint:
            raise ValueError("API端点不能为空")
        if self.rate <= 0:
            raise ValueError("限流次数必须大于0")
        if self.period <= 0:
            raise ValueError("限流时间周期必须大于0")

    def get_rate_string(self) -> str:
        """获取限流字符串，如 '60/minute'"""
        if self.period >= 60:
            return f"{self.rate}/{self.period // 60}minute"
        return f"{self.rate}/{self.period}second"

    def check_limit(self, current_count: int) -> bool:
        """检查是否超过限制"""
        return current_count < self.rate

    def activate(self) -> None:
        """激活限流规则"""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """停用限流规则"""
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "limit_id": self.limit_id,
            "name": self.name,
            "endpoint": self.endpoint,
            "method": self.method,
            "rate": self.rate,
            "period": self.period,
            "scope": self.scope,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class RateLimitRecordEntity:
    """
    限流记录实体
    记录实际请求次数
    """

    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    key: str = ""  # 限流键，如 IP地址或用户ID
    endpoint: str = ""
    method: str = "GET"
    count: int = 0
    window_start: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(minutes=5))

    def increment(self) -> int:
        """增加计数"""
        self.count += 1
        return self.count

    def is_expired(self) -> bool:
        """检查是否过期"""
        return datetime.now() > self.expires_at

    def reset(self) -> None:
        """重置计数"""
        self.count = 0
        self.window_start = datetime.now()
        self.expires_at = datetime.now() + timedelta(minutes=5)
