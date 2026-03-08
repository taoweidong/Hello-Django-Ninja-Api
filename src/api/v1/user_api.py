"""
用户API
User API - 用户管理相关接口
"""

from ninja import Query, Router
from pydantic import BaseModel

from src.application.dto.user import (
    ChangePasswordDTO,
    UserCreateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from src.application.services.user_service import user_service
from src.infrastructure.auth_jwt.token_validator import token_validator

router = Router(tags=["用户"])


class MessageResponse(BaseModel):
    """消息响应"""

    message: str


class UserListResponse(BaseModel):
    """用户列表响应"""

    users: list[UserResponseDTO]
    total: int
    page: int
    page_size: int


def get_current_user(request) -> dict | None:
    """获取当前用户"""
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header[7:]
    is_valid, payload = token_validator.is_token_valid(token)
    if not is_valid:
        return None

    return payload


@router.post("/users", response=UserResponseDTO, summary="创建用户")
async def create_user(user_dto: UserCreateDTO):
    """
    创建用户
    - 注册新用户
    """
    try:
        result = await user_service.create_user(user_dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/users/{user_id}", response=UserResponseDTO, summary="获取用户详情")
async def get_user(user_id: str):
    """
    获取用户详情
    - 根据用户ID获取用户信息
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise ValueError("用户不存在")
    return user


@router.get("/users", response=UserListResponse, summary="获取用户列表")
async def list_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    获取用户列表
    - 分页获取用户列表
    """
    users, total = await user_service.list_users(page, page_size)
    return UserListResponse(
        users=users,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.put("/users/{user_id}", response=UserResponseDTO, summary="更新用户")
async def update_user(user_id: str, user_dto: UserUpdateDTO):
    """
    更新用户信息
    - 更新用户的基本信息
    """
    try:
        result = await user_service.update_user(user_id, user_dto)
        return result
    except ValueError as e:
        raise ValueError(str(e))


@router.delete("/users/{user_id}", response=MessageResponse, summary="删除用户")
async def delete_user(user_id: str):
    """
    删除用户
    - 软删除用户
    """
    result = await user_service.delete_user(user_id)
    if not result:
        raise ValueError("用户不存在")
    return MessageResponse(message="用户删除成功")


@router.post("/users/change-password", response=MessageResponse, summary="修改密码")
async def change_password(request, password_dto: ChangePasswordDTO):
    """
    修改密码
    - 修改当前用户密码
    """
    current_user = get_current_user(request)
    if not current_user:
        raise ValueError("未登录或令牌无效")

    user_id = current_user.get("user_id")
    try:
        await user_service.change_password(
            user_id, password_dto.old_password, password_dto.new_password
        )
        return MessageResponse(message="密码修改成功")
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/me", response=UserResponseDTO, summary="获取当前用户信息")
async def get_current_user_info(request):
    """
    获取当前用户信息
    - 获取已登录用户的信息
    """
    current_user = get_current_user(request)
    if not current_user:
        raise ValueError("未登录或令牌无效")

    user_id = current_user.get("user_id")
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise ValueError("用户不存在")
    return user
