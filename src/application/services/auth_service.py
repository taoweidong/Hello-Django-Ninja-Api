"""
认证服务
Auth Service - 认证业务逻辑处理
"""

from datetime import datetime

from django.utils import timezone

from src.application.dto.auth import RefreshTokenDTO, TokenResponseDTO
from src.application.dto.user import UserLoginDTO
from src.infrastructure.auth_jwt.jwt_manager import jwt_manager
from src.infrastructure.auth_jwt.token_validator import token_validator
from src.infrastructure.cache.cache_manager import cache_manager
from src.infrastructure.persistence.models.auth_models import LoginLog, RefreshToken
from src.infrastructure.persistence.models.user_models import User
from src.infrastructure.repositories.rbac_repo_impl import rbac_repository


class AuthService:
    """
    认证应用服务
    处理JWT认证相关业务逻辑
    """

    async def login(
        self,
        login_dto: UserLoginDTO,
        ip_address: str | None = None,
        user_agent: str | None = None,
        device_info: str | None = None,
    ) -> TokenResponseDTO:
        """
        用户登录
        """
        # 验证用户凭据
        try:
            user = await User.objects.aget(username=login_dto.username)
        except User.DoesNotExist:
            raise ValueError("用户名或密码错误")

        # 检查用户是否激活
        if not user.is_active:
            # 记录登录失败日志
            await self._create_login_log(
                user, ip_address, user_agent, device_info, False, "用户已被停用"
            )
            raise ValueError("用户已被停用")

        # 验证密码
        if not user.check_password(login_dto.password):
            # 记录登录失败日志
            await self._create_login_log(
                user, ip_address, user_agent, device_info, False, "密码错误"
            )
            raise ValueError("用户名或密码错误")

        # 获取用户角色和权限
        roles = await rbac_repository.get_user_roles(str(user.id))
        role_codes = [role.code for role in roles]

        permissions = await rbac_repository.get_user_permissions(str(user.id))
        permission_codes = [perm.code for perm in permissions]

        # 生成Token
        access_token, access_expire = jwt_manager.create_access_token(
            user_id=str(user.id),
            username=user.username,
            roles=role_codes,
            permissions=permission_codes,
        )
        refresh_token, refresh_expire = jwt_manager.create_refresh_token(
            user_id=str(user.id),
            username=user.username,
        )

        # 保存刷新Token
        decoded = jwt_manager.decode_token(refresh_token)
        jti = decoded.get("jti") if decoded else None
        await self._save_refresh_token(
            user_id=str(user.id),
            token=refresh_token,
            jti=jti,
            expires_at=refresh_expire,
            ip_address=ip_address,
            device_info=device_info,
        )

        # 更新最后登录时间
        user.last_login = timezone.now()
        await user.asave()

        # 记录登录成功日志
        await self._create_login_log(user, ip_address, user_agent, device_info, True)

        # 计算过期时间（秒）
        from django.conf import settings

        access_lifetime = int(settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", 60))

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=access_lifetime * 60,
            user={
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
        )

    async def refresh_access_token(self, refresh_dto: RefreshTokenDTO) -> TokenResponseDTO:
        """
        刷新访问令牌
        """
        # 验证刷新Token
        is_valid, error, payload = token_validator.validate_refresh_token(refresh_dto.refresh_token)
        if not is_valid or payload is None:
            raise ValueError(f"刷新Token无效或已过期: {error}")

        user_id = payload.get("user_id")
        username = payload.get("username")

        # 获取用户角色和权限
        roles = await rbac_repository.get_user_roles(user_id)
        role_codes = [role.code for role in roles]

        permissions = await rbac_repository.get_user_permissions(user_id)
        permission_codes = [perm.code for perm in permissions]

        # 生成新的访问Token
        access_token, access_expire = jwt_manager.create_access_token(
            user_id=user_id,
            username=username,
            roles=role_codes,
            permissions=permission_codes,
        )

        # 计算过期时间（秒）
        from django.conf import settings

        access_lifetime = int(settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", 60))

        # 获取用户信息
        try:
            user = await User.objects.aget(id=user_id)
            user_info = {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
            }
        except User.DoesNotExist:
            user_info = None

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=None,
            token_type="Bearer",
            expires_in=access_lifetime * 60,
            user=user_info,
        )

    async def logout(self, access_token: str) -> bool:
        """
        用户登出
        """
        # 撤销Token
        token_validator.revoke_token(access_token)

        # 获取用户ID并清除缓存
        payload = jwt_manager.get_token_claims(access_token)
        if payload:
            user_id = payload.get("user_id")
            if user_id:
                cache_manager.delete_user_cache(user_id)
                cache_manager.delete_permissions_cache(user_id)
                cache_manager.delete_roles_cache(user_id)

        return True

    async def verify_token(self, token: str) -> tuple[bool, dict | None]:
        """
        验证Token
        """
        is_valid, error, payload = token_validator.is_token_valid(token)
        if not is_valid:
            return False, None
        return True, payload

    async def _save_refresh_token(
        self,
        user_id: str,
        token: str,
        jti: str | None,
        expires_at: datetime,
        ip_address: str | None = None,
        device_info: str | None = None,
    ) -> None:
        """保存刷新Token"""
        await RefreshToken.objects.acreate(
            user_id=user_id,
            token=token,
            jti=jti,
            expires_at=expires_at,
            ip_address=ip_address,
            device_info=device_info,
        )

    async def _create_login_log(
        self,
        user: User,
        ip_address: str | None,
        user_agent: str | None,
        device_info: str | None,
        status: bool,
        fail_reason: str | None = None,
    ) -> None:
        """创建登录日志"""
        await LoginLog.objects.acreate(
            user=user,
            username=user.username,
            ip_address=ip_address or "unknown",
            user_agent=user_agent,
            device_info=device_info,
            login_status=status,
            fail_reason=fail_reason,
        )


# 全局实例
auth_service = AuthService()
