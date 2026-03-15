"""
自定义权限类
Custom Permissions - 适配现有 RBAC 系统的权限控制
"""

from typing import Any

from ninja_extra.permissions import BasePermission

from src.infrastructure.auth_jwt.token_validator import token_validator


class IsAuthenticated(BasePermission):
    """
    认证权限类
    验证用户是否已登录
    """

    def has_permission(self, request: Any, controller: Any) -> bool:
        """
        检查用户是否已认证

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否已认证
        """
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return False

        token = auth_header[7:]
        is_valid, error_msg, payload = token_validator.is_token_valid(token)

        if is_valid and payload:
            # 将用户信息注入请求对象
            request.user_id = payload.get("user_id")
            request.user_payload = payload
            return True

        return False


class HasPermission(BasePermission):
    """
    权限检查类
    验证用户是否拥有指定权限

    用法:
        @api_controller("/users", permissions=[IsAuthenticated, HasPermission("user:read")])
        class UserController:
            pass
    """

    def __init__(self, permission_code: str):
        """
        初始化权限检查

        Args:
            permission_code: 权限代码，如 "user:read", "role:delete"
        """
        self.permission_code = permission_code

    def has_permission(self, request: Any, controller: Any) -> bool:
        """
        检查用户是否拥有指定权限

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否拥有权限
        """
        # 首先确保用户已认证
        if not hasattr(request, "user_id"):
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if not auth_header.startswith("Bearer "):
                return False

            token = auth_header[7:]
            is_valid, _, payload = token_validator.is_token_valid(token)

            if not is_valid or not payload:
                return False

            request.user_id = payload.get("user_id")
            request.user_payload = payload

        # 检查权限
        user_id = getattr(request, "user_id", None)
        if not user_id:
            return False

        # 异步权限检查需要在视图层面处理
        # 这里先返回 True，实际检查在 async_has_permission 中进行
        request._required_permission = self.permission_code
        return True

    async def async_has_permission(self, request: Any, controller: Any) -> bool:
        """
        异步权限检查

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否拥有权限
        """
        user_id = getattr(request, "user_id", None)
        if not user_id:
            return False

        from src.application.services.rbac_service import rbac_service

        return await rbac_service.check_user_permission(user_id, self.permission_code)


class HasAnyPermission(BasePermission):
    """
    任一权限检查类
    验证用户是否拥有指定权限中的任意一个

    用法:
        @api_controller("/users", permissions=[IsAuthenticated, HasAnyPermission("user:read", "user:write")])
        class UserController:
            pass
    """

    def __init__(self, *permission_codes: str):
        """
        初始化权限检查

        Args:
            permission_codes: 权限代码列表
        """
        self.permission_codes = permission_codes

    def has_permission(self, request: Any, controller: Any) -> bool:
        """
        检查用户是否拥有任一权限

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否拥有任一权限
        """
        # 首先确保用户已认证
        if not hasattr(request, "user_id"):
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if not auth_header.startswith("Bearer "):
                return False

            token = auth_header[7:]
            is_valid, _, payload = token_validator.is_token_valid(token)

            if not is_valid or not payload:
                return False

            request.user_id = payload.get("user_id")
            request.user_payload = payload

        # 保存需要的权限列表
        request._required_permissions = self.permission_codes
        return True

    async def async_has_permission(self, request: Any, controller: Any) -> bool:
        """
        异步权限检查

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否拥有任一权限
        """
        user_id = getattr(request, "user_id", None)
        if not user_id:
            return False

        from src.application.services.rbac_service import rbac_service

        for perm_code in self.permission_codes:
            has_perm = await rbac_service.check_user_permission(user_id, perm_code)
            if has_perm:
                return True

        return False


class IsAdminUser(BasePermission):
    """
    管理员权限类
    验证用户是否为管理员（拥有 admin 角色）
    """

    def has_permission(self, request: Any, controller: Any) -> bool:
        """
        检查用户是否为管理员

        Args:
            request: HTTP 请求对象
            controller: 控制器对象

        Returns:
            bool: 是否为管理员
        """
        # 首先确保用户已认证
        if not hasattr(request, "user_payload"):
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if not auth_header.startswith("Bearer "):
                return False

            token = auth_header[7:]
            is_valid, _, payload = token_validator.is_token_valid(token)

            if not is_valid or not payload:
                return False

            request.user_id = payload.get("user_id")
            request.user_payload = payload

        payload = getattr(request, "user_payload", {})
        roles = payload.get("roles", [])

        return "admin" in roles


class AllowAny(BasePermission):
    """
    允许所有用户访问
    用于公开接口
    """

    def has_permission(self, request: Any, controller: Any) -> bool:
        """允许所有请求"""
        return True
