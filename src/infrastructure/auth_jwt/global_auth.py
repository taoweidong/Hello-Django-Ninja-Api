"""
全局认证类
Global Authentication - 用于 NinjaExtraAPI 的全局认证配置
"""

from ninja.security import HttpBearer

from src.infrastructure.auth_jwt.token_validator import token_validator


class GlobalAuth(HttpBearer):
    """
    全局认证类
    基于 JWT Bearer Token 的全局认证

    使用方式:
        # 在控制器中配置
        @api_controller("/v1/users", auth=GlobalAuth())
        class UserController:
            pass

        # 豁免特定接口
        @http_post("/login", auth=None)
        async def login(self, ...):
            pass

    获取用户信息:
        # authenticate 返回的 payload 会存储在 request.auth 中
        user_id = request.auth.get("user_id")
    """

    def authenticate(self, request, token: str):
        """
        验证 Token 并返回用户信息

        Args:
            request: HTTP 请求对象
            token: JWT Token 字符串

        Returns:
            dict: 用户信息（认证成功时），会存储在 request.auth 中
            None: 认证失败时
        """
        is_valid, error_msg, payload = token_validator.is_token_valid(token)

        if is_valid and payload:
            # 返回的 payload 会存储在 request.auth 中
            return payload

        return None
