"""
API应用实例
API Application - NinjaAPI实例和路由注册
"""

from ninja import NinjaAPI

from src.api.v1 import auth_api, rbac_api, security_api, user_api

# 创建API实例
api = NinjaAPI(
    title="Hello-Django-Ninja-Api",
    description="基于Django-Ninja的RESTful API服务 - 集成JWT认证和RBAC权限管理",
    version="1.0.0",
)

# 注册路由
api.add_router("/v1/auth", auth_api.router, tags=["认证"])
api.add_router("/v1", user_api.router, tags=["用户"])
api.add_router("/v1", rbac_api.router, tags=["权限管理"])
api.add_router("/v1", security_api.router, tags=["安全"])


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
