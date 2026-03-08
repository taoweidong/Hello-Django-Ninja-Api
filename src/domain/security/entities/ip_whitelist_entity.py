"""
IP白名单实体
IP Whitelist Entity - IP白名单管理
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class IPWhitelistEntity:
    """
    IP白名单实体
    存储允许访问的IP地址
    """

    whitelist_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ip_address: str = ""
    description: str = ""  # 描述
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str | None = None

    def __post_init__(self):
        if not self.ip_address:
            raise ValueError("IP地址不能为空")

    def deactivate(self) -> None:
        """停用白名单"""
        self.is_active = False

    def activate(self) -> None:
        """激活白名单"""
        self.is_active = True

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "whitelist_id": self.whitelist_id,
            "ip_address": self.ip_address,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
