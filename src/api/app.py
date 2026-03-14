"""
API应用实例
API Application - NinjaExtraAPI实例和路由注册
"""

from ninja_extra import NinjaExtraAPI

from src.api.v1.controllers import (
    AuthController,
    RBACController,
    SecurityController,
    SystemController,
    UserController,
)

# 创建API实例
api = NinjaExtraAPI(
    title="Hello-Django-Ninja-Api",
    description="基于Django-Ninja-Extra的RESTful API服务 - 集成JWT认证和RBAC权限管理",
    version="1.0.0",
)

# 注册控制器
api.register_controllers(
    AuthController,
    UserController,
    RBACController,
    SecurityController,
    SystemController,
)


@api.get("/health", tags=["系统"])
def health_check(request):
    """健康检查"""
    return {"status": "ok", "message": "服务运行正常"}


@api.get("/", tags=["系统"])
def root(request):
    """API根路径"""
    return {
        "message": "Welcome to Hello-Django-Ninja-Api",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
    }
