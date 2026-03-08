"""
认证领域服务
Auth Domain Service - 处理JWT认证相关核心业务逻辑
"""

from datetime import datetime, timedelta

from src.domain.auth.entities.token_entity import TokenBlacklistEntity, TokenEntity


class AuthDomainService:
    """
    认证领域服务
    处理JWT认证相关核心业务逻辑
    """

    def __init__(self):
        self.token_blacklist: dict[str, TokenBlacklistEntity] = {}

    async def create_token(
        self,
        user_id: str,
        username: str,
        roles: list[str] = None,
        permissions: list[str] = None,
        org_id: str = None,
        access_token_lifetime: int = 60,
        _refresh_token_lifetime: int = 1440,
        device_info: str = None,
        ip_address: str = None,
    ) -> TokenEntity:
        """
        创建Token
        """
        now = datetime.now()
        expires_at = now + timedelta(minutes=access_token_lifetime)

        token = TokenEntity(
            user_id=user_id,
            username=username,
            roles=roles or [],
            permissions=permissions or [],
            org_id=org_id,
            expires_at=expires_at,
            issued_at=now,
            device_info=device_info,
            ip_address=ip_address,
        )

        return token

    async def verify_token(self, token: TokenEntity) -> bool:
        """
        验证Token
        """
        # 检查是否在黑名单中
        if token.token_id in self.token_blacklist:
            return False

        # 检查是否过期
        if token.is_expired():
            return False

        # 检查是否已撤销
        return not token.is_revoked


    async def revoke_token(self, token: TokenEntity) -> TokenBlacklistEntity:
        """
        撤销Token
        将Token加入黑名单
        """
        token.revoke()

        blacklist_entry = TokenBlacklistEntity(
            token_jti=token.token_id,
            user_id=token.user_id,
            expires_at=token.expires_at,
        )

        self.token_blacklist[token.token_id] = blacklist_entry
        return blacklist_entry

    async def is_token_revoked(self, token_jti: str) -> bool:
        """
        检查Token是否已撤销
        """
        blacklist_entry = self.token_blacklist.get(token_jti)
        if not blacklist_entry:
            return False

        # 如果已过期，从黑名单中移除
        if blacklist_entry.is_expired():
            del self.token_blacklist[token_jti]
            return False

        return True

    async def refresh_token(
        self, old_token: TokenEntity, access_token_lifetime: int = 60
    ) -> TokenEntity:
        """
        刷新Token
        """
        # 验证原Token
        if not await self.verify_token(old_token):
            raise ValueError("Token无效或已过期")

        # 撤销原Token
        await self.revoke_token(old_token)

        # 创建新Token
        new_token = await self.create_token(
            user_id=old_token.user_id,
            username=old_token.username,
            roles=old_token.roles,
            permissions=old_token.permissions,
            org_id=old_token.org_id,
            access_token_lifetime=access_token_lifetime,
            device_info=old_token.device_info,
            ip_address=old_token.ip_address,
        )

        return new_token

    def get_token_claims(self, token: TokenEntity) -> dict:
        """
        获取Token声明
        """
        return token.get_payload()
