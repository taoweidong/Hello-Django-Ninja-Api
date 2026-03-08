"""
认证令牌实体
Token Entity - JWT令牌实体
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class TokenEntity:
    """
    认证令牌实体
    包含JWT Token的相关信息
    """

    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    username: str = ""
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    org_id: str | None = None
    access_token: str = ""
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(minutes=60))
    issued_at: datetime = field(default_factory=datetime.now)
    device_info: str | None = None
    ip_address: str | None = None
    is_revoked: bool = False

    def __post_init__(self):
        if not self.user_id:
            raise ValueError("用户ID不能为空")

    def is_expired(self) -> bool:
        """检查令牌是否过期"""
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """检查令牌是否有效"""
        return not self.is_expired() and not self.is_revoked

    def revoke(self) -> None:
        """撤销令牌"""
        self.is_revoked = True

    def get_payload(self) -> dict:
        """获取Token载荷"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "roles": self.roles,
            "permissions": self.permissions,
            "org_id": self.org_id,
            "exp": int(self.expires_at.timestamp()),
            "iat": int(self.issued_at.timestamp()),
            "jti": self.token_id,
        }

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "token_id": self.token_id,
            "user_id": self.user_id,
            "username": self.username,
            "roles": self.roles,
            "permissions": self.permissions,
            "org_id": self.org_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_at": self.expires_at.isoformat(),
            "issued_at": self.issued_at.isoformat(),
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "is_revoked": self.is_revoked,
        }


@dataclass
class TokenBlacklistEntity:
    """
    Token黑名单实体
    用于存储已撤销的Token
    """

    blacklist_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    token_jti: str = ""  # Token的唯一标识
    user_id: str = ""
    revoked_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = None  # Token原过期时间

    def __post_init__(self):
        if not self.token_jti:
            raise ValueError("Token JTI不能为空")
        if not self.expires_at:
            # 默认保留7天
            self.expires_at = datetime.now() + timedelta(days=7)

    def is_expired(self) -> bool:
        """检查是否过期（可以删除）"""
        return datetime.now() > self.expires_at
