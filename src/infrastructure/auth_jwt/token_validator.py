"""
Token验证器
Token Validator - Token验证和黑名单检查
"""

from django.core.cache import cache

from src.infrastructure.auth_jwt.jwt_manager import jwt_manager


class TokenValidator:
    """
    Token验证器
    负责验证Token的有效性
    """

    def __init__(self):
        self.jwt_manager = jwt_manager
        self.blacklist_prefix = "token_blacklist:"

    def is_token_valid(self, token: str) -> tuple[bool, str | None, dict | None]:
        """
        验证Token是否有效
        返回: (是否有效, 错误信息, Token载荷)
        """
        # 1. 检查Token格式
        is_valid, payload = self.jwt_manager.verify_token(token)
        if not is_valid:
            return False, "无效的Token", None

        # 2. 检查Token类型
        token_type = payload.get("type")
        if token_type != "access":
            return False, "Token类型不正确", None

        # 3. 检查是否在黑名单中
        jti = payload.get("jti")
        if self.is_blacklisted(jti):
            return False, "Token已失效", None

        # 4. 检查是否过期
        if self.jwt_manager.is_token_expired(token):
            return False, "Token已过期", None

        return True, None, payload

    def is_blacklisted(self, jti: str) -> bool:
        """
        检查Token是否在黑名单中
        """
        key = f"{self.blacklist_prefix}{jti}"
        return cache.get(key) is not None

    def add_to_blacklist(self, jti: str, expires_at: int) -> None:
        """
        将Token加入黑名单
        """
        key = f"{self.blacklist_prefix}{jti}"
        # 设置过期时间与Token过期时间一致
        cache.set(key, True, timeout=expires_at)

    def validate_refresh_token(self, token: str) -> tuple[bool, str | None, dict | None]:
        """
        验证刷新Token
        """
        is_valid, payload = self.jwt_manager.verify_token(token)
        if not is_valid:
            return False, "无效的刷新Token", None

        token_type = payload.get("type")
        if token_type != "refresh":
            return False, "Token类型不正确", None

        # 检查是否在黑名单中
        jti = payload.get("jti")
        if self.is_blacklisted(jti):
            return False, "刷新Token已失效", None

        return True, None, payload

    def revoke_token(self, token: str) -> bool:
        """
        撤销Token
        """
        payload = self.jwt_manager.get_token_claims(token)
        if not payload:
            return False

        jti = payload.get("jti")
        exp = payload.get("exp")

        if not jti or not exp:
            return False

        # 计算剩余有效时间
        from datetime import datetime

        remaining_seconds = exp - int(datetime.utcnow().timestamp())

        if remaining_seconds > 0:
            self.add_to_blacklist(jti, remaining_seconds)

        return True


# 全局实例
token_validator = TokenValidator()
