"""
JWT管理器
JWT Manager - JWT Token生成和验证
"""

import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings


class JWTManager:
    """
    JWT令牌管理器
    负责Token的生成、验证和刷新
    """

    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.SIMPLE_JWT.get("ALGORITHM", "HS256")
        self.access_token_lifetime = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", 60)
        self.refresh_token_lifetime = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", 1440)

    def create_access_token(
        self,
        user_id: str,
        username: str,
        roles: list = None,
        permissions: list = None,
        org_id: str = None,
        additional_claims: dict = None,
    ) -> tuple[str, datetime]:
        """
        创建访问令牌
        """
        now = datetime.utcnow()
        expire = now + timedelta(minutes=int(self.access_token_lifetime))

        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles or [],
            "permissions": permissions or [],
            "org_id": org_id,
            "type": "access",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": str(uuid.uuid4()),
        }

        if additional_claims:
            payload.update(additional_claims)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, expire

    def create_refresh_token(
        self, user_id: str, username: str, additional_claims: dict = None
    ) -> tuple[str, datetime]:
        """
        创建刷新令牌
        """
        now = datetime.utcnow()
        expire = now + timedelta(minutes=int(self.refresh_token_lifetime))

        payload = {
            "user_id": user_id,
            "username": username,
            "type": "refresh",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": str(uuid.uuid4()),
        }

        if additional_claims:
            payload.update(additional_claims)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, expire

    def decode_token(self, token: str) -> dict | None:
        """
        解码令牌
        """
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def verify_token(self, token: str) -> tuple[bool, dict | None]:
        """
        验证令牌
        """
        payload = self.decode_token(token)
        if not payload:
            return False, None
        return True, payload

    def get_token_claims(self, token: str) -> dict | None:
        """
        获取令牌声明
        """
        return self.decode_token(token)

    def get_user_id_from_token(self, token: str) -> str | None:
        """
        从令牌获取用户ID
        """
        payload = self.decode_token(token)
        return payload.get("user_id") if payload else None

    def get_username_from_token(self, token: str) -> str | None:
        """
        从令牌获取用户名
        """
        payload = self.decode_token(token)
        return payload.get("username") if payload else None

    def is_token_expired(self, token: str) -> bool:
        """
        检查令牌是否过期
        """
        payload = self.decode_token(token)
        if not payload:
            return True
        exp = payload.get("exp")
        if not exp:
            return True
        return datetime.utcnow() > datetime.fromtimestamp(exp)

    def get_token_type(self, token: str) -> str | None:
        """
        获取令牌类型
        """
        payload = self.decode_token(token)
        return payload.get("type") if payload else None


# 全局实例
jwt_manager = JWTManager()
