"""
认证API
Auth API - 认证相关接口
"""

from ninja import Header, Router
from pydantic import BaseModel

from src.application.dto.auth_dto import RefreshTokenDTO, TokenResponseDTO
from src.application.dto.user_dto import UserLoginDTO
from src.application.services.auth_service import auth_service

router = Router(tags=["认证"])


class MessageResponse(BaseModel):
    """消息响应"""

    message: str


@router.post("/login", response=TokenResponseDTO, summary="用户登录")
async def login(request, login_dto: UserLoginDTO):
    """
    用户登录接口
    - 用户名和密码登录
    - 返回JWT访问令牌和刷新令牌
    """
    # 获取客户端IP
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    user_agent = request.META.get("HTTP_USER_AGENT", "")

    try:
        result = await auth_service.login(
            login_dto=login_dto,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=login_dto.device_info,
        )
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.post("/refresh", response=TokenResponseDTO, summary="刷新访问令牌")
async def refresh_token(refresh_dto: RefreshTokenDTO):
    """
    刷新访问令牌
    - 使用刷新令牌获取新的访问令牌
    """
    try:
        result = await auth_service.refresh_access_token(refresh_dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.post("/logout", response=MessageResponse, summary="用户登出")
async def logout(authorization: str | None = Header(None)):
    """
    用户登出
    - 撤销当前访问令牌
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        await auth_service.logout(token)

    return MessageResponse(message="登出成功")
