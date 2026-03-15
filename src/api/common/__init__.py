"""
API公共模块
API Common - 公共组件和工具
"""

from src.api.common.decorators import handle_errors, require_auth
from src.api.common.permissions import AllowAny, HasAnyPermission, HasPermission, IsAdminUser, IsAuthenticated
from src.api.common.responses import MessageResponse, PaginatedResponse, ResponseFactory

__all__ = [
    # 装饰器
    "handle_errors",
    "require_auth",
    # 权限类
    "IsAuthenticated",
    "HasPermission",
    "HasAnyPermission",
    "IsAdminUser",
    "AllowAny",
    # 响应对象
    "MessageResponse",
    "PaginatedResponse",
    "ResponseFactory",
]
