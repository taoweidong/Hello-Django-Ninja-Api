"""
IP黑名单实体
IP Blacklist Entity - IP黑名单管理
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class IPBlacklistEntity:
    """
    IP黑名单实体
    存储被禁止访问的IP地址
    """

    blacklist_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ip_address: str = ""
    reason: str = ""  # 封禁原因
    is_permanent: bool = False  # 是否永久封禁
    expires_at: datetime | None = None  # 过期时间（临时封禁）
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str | None = None

    def __post_init__(self):
        if not self.ip_address:
            raise ValueError("IP地址不能为空")

    def is_active(self) -> bool:
        """检查是否处于封禁状态"""
        if self.is_permanent:
            return True
        if self.expires_at:
            return datetime.now() < self.expires_at
        return False

    def unban(self) -> None:
        """解除封禁"""
        self.expires_at = datetime.now()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "blacklist_id": self.blacklist_id,
            "ip_address": self.ip_address,
            "reason": self.reason,
            "is_permanent": self.is_permanent,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
