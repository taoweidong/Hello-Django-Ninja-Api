"""
API装饰器
API Decorators - 统一的错误处理和权限检查装饰器
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from ninja.errors import HttpError


def handle_errors(func: Callable) -> Callable:
    """
    统一错误处理装饰器
    捕获常见异常并转换为HTTP错误

    用法:
        @router.post("/users")
        @handle_errors
        async def create_user(request, data: UserCreateDTO):
            # 业务逻辑
            pass

    异常映射:
        ValueError -> 400 Bad Request
        PermissionError -> 403 Forbidden
        其他异常 -> 500 Internal Server Error
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HttpError(400, str(e))
        except PermissionError as e:
            raise HttpError(403, str(e))
        except HttpError:
            # 已经是HTTP错误，直接抛出
            raise
        except Exception as e:
            # 记录详细错误信息到日志
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            raise HttpError(500, f"操作失败: {str(e)}")

    return wrapper


def require_auth(func: Callable) -> Callable:
    """
    需要认证的装饰器
    验证JWT令牌并注入当前用户信息到kwargs中

    用法:
        @router.get("/me")
        @require_auth
        async def get_current_user(request, current_user: dict):
            # current_user 已自动注入
            return {"user_id": current_user["user_id"]}

    参数:
        request: Django请求对象

    返回:
        装饰后的函数，kwargs中将包含 current_user

    异常:
        HttpError 401: 未登录或令牌无效
    """

    @wraps(func)
    async def wrapper(request, *args, **kwargs) -> Any:
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            raise HttpError(401, "未登录或令牌无效")

        from src.infrastructure.auth_jwt.token_validator import token_validator

        token = auth_header[7:]
        is_valid, payload = token_validator.is_token_valid(token)
        if not is_valid:
            raise HttpError(401, "未登录或令牌无效")

        # 注入当前用户到kwargs
        kwargs["current_user"] = payload
        return await func(request, *args, **kwargs)

    return wrapper


def require_permissions(*permission_codes: str) -> Callable:
    """
    需要特定权限的装饰器
    验证当前用户是否拥有指定权限

    用法:
        @router.delete("/users/{user_id}")
        @require_auth
        @require_permissions("user:delete")
        async def delete_user(request, user_id: str, current_user: dict):
            # 只有拥有 user:delete 权限的用户才能访问
            pass

    参数:
        permission_codes: 需要的权限代码列表

    返回:
        装饰后的函数

    异常:
        HttpError 401: 未登录
        HttpError 403: 权限不足
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @require_auth
        async def wrapper(request, *args, **kwargs) -> Any:
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HttpError(401, "未登录")

            user_id = current_user.get("user_id")
            if not user_id:
                raise HttpError(401, "无效的用户信息")

            # 检查权限
            from src.application.services.rbac_service import rbac_service

            for perm_code in permission_codes:
                has_perm = await rbac_service.has_permission(user_id, perm_code)
                if not has_perm:
                    raise HttpError(403, f"权限不足: 需要 {perm_code} 权限")

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


def validate_exists(get_entity_func: Callable) -> Callable:
    """
    验证实体存在的装饰器
    在执行操作前验证实体是否存在

    用法:
        async def get_user(user_id: str):
            return await user_service.get_user_by_id(user_id)

        @router.put("/users/{user_id}")
        @validate_exists(get_user)
        async def update_user(request, user_id: str, entity: UserEntity):
            # entity 已自动注入并验证存在
            pass

    参数:
        get_entity_func: 获取实体的异步函数

    返回:
        装饰后的函数，kwargs中将包含 entity

    异常:
        HttpError 404: 实体不存在
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request, *args, **kwargs) -> Any:
            # 从kwargs中提取ID参数（假设第一个参数是ID）
            # 这里需要根据实际情况调整
            entity_id = kwargs.get("user_id") or kwargs.get("role_id") or kwargs.get("permission_id")

            if entity_id:
                entity = await get_entity_func(entity_id)
                if not entity:
                    raise HttpError(404, "资源不存在")
                kwargs["entity"] = entity

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
