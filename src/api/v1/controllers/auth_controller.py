"""
认证控制器
Auth Controller - 认证API控制器
"""

from src.application.dto.auth import RefreshTokenDTO, TokenResponseDTO
from src.application.dto.user import UserLoginDTO
from src.application.services.auth_service import AuthService


class AuthController:
    """
    认证控制器
    处理认证相关API请求
    """

    def __init__(self, auth_service: AuthService = None):
        self._auth_service = auth_service or AuthService()

    async def login(
        self,
        login_dto: UserLoginDTO,
        ip_address: str = None,
        user_agent: str = None,
        device_info: str = None,
    ) -> TokenResponseDTO:
        """用户登录"""
        return await self._auth_service.login(
            login_dto=login_dto,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info,
        )

    async def refresh_token(self, refresh_dto: RefreshTokenDTO) -> TokenResponseDTO:
        """刷新访问令牌"""
        return await self._auth_service.refresh_access_token(refresh_dto)

    async def logout(self, access_token: str) -> bool:
        """用户登出"""
        return await self._auth_service.logout(access_token)

    async def verify_token(self, token: str) -> tuple[bool, dict | None]:
        """验证Token"""
        return await self._auth_service.verify_token(token)
