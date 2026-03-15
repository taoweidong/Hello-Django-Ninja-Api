"""
认证控制器
Auth Controller - 认证API控制器
"""

from ninja import Body, Header
from ninja_extra import api_controller, http_post
from ninja_extra.permissions import AllowAny

from src.api.common.responses import MessageResponse
from src.application.dto.auth import RefreshTokenDTO, TokenResponseDTO
from src.application.dto.user import UserLoginDTO
from src.application.services.auth_service import AuthService


@api_controller("/v1/auth", tags=["认证"], permissions=[AllowAny])
class AuthController:
    """
    认证控制器
    处理认证相关API请求

    遵循SOLID原则:
    - 单一职责: 只处理认证相关的HTTP请求
    - 依赖倒置: 通过构造函数注入 AuthService
    """

    def __init__(self, auth_service: AuthService | None = None) -> None:
        """
        初始化认证控制器

        Args:
            auth_service: 认证服务实例（可选，用于依赖注入）
        """
        self._auth_service = auth_service or AuthService()

    @http_post("/login", response=TokenResponseDTO, summary="用户登录", operation_id="auth_login")
    async def login(self, request, login_dto: UserLoginDTO = Body(...)) -> TokenResponseDTO:
        """
        用户登录接口

        - 用户名和密码登录
        - 返回 JWT 访问令牌和刷新令牌

        Args:
            request: Django HTTP 请求对象
            login_dto: 登录数据传输对象

        Returns:
            TokenResponseDTO: 包含访问令牌和刷新令牌

        Raises:
            ValueError: 登录失败时抛出
        """
        # 获取客户端 IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip_address = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR", "")

        user_agent = request.META.get("HTTP_USER_AGENT", "")

        result = await self._auth_service.login(login_dto=login_dto, ip_address=ip_address, user_agent=user_agent, device_info=login_dto.device_info)
        return result

    @http_post("/refresh", response=TokenResponseDTO, summary="刷新访问令牌", operation_id="auth_refresh_token")
    async def refresh_token(self, refresh_dto: RefreshTokenDTO) -> TokenResponseDTO:
        """
        刷新访问令牌

        - 使用刷新令牌获取新的访问令牌

        Args:
            refresh_dto: 刷新令牌数据传输对象

        Returns:
            TokenResponseDTO: 新的访问令牌和刷新令牌

        Raises:
            ValueError: 刷新令牌无效时抛出
        """
        result = await self._auth_service.refresh_access_token(refresh_dto)
        return result

    @http_post("/logout", response=MessageResponse, summary="用户登出", operation_id="auth_logout")
    async def logout(self, authorization: str | None = Header(None, description="Bearer Token")) -> MessageResponse:
        """
        用户登出

        - 撤销当前访问令牌

        Args:
            authorization: Authorization 请求头

        Returns:
            MessageResponse: 操作结果消息
        """
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
            await self._auth_service.logout(token)

        return MessageResponse(message="登出成功")
