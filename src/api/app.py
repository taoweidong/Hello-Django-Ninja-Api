"""
API应用实例
API Application - NinjaExtraAPI实例和路由配置

权限控制策略：
- 控制器级别鉴权：在 @api_controller 中配置 auth=GlobalAuth()
- 豁免标记：公开接口使用 auth=None
"""

from ninja_extra import NinjaExtraAPI

from src.api.v1.controllers import AuthController, RBACController, SecurityController, SystemController, UserController

# 创建API实例
api = NinjaExtraAPI(
    title="Hello-Django-Ninja-Api",
    description="基于Django-Ninja-Extra的RESTful API服务 - 集成JWT认证和RBAC权限管理",
    version="1.0.0",
)

# 注册控制器（每个控制器单独配置 auth）
api.register_controllers(AuthController, UserController, RBACController, SecurityController, SystemController)


@api.get("/health", tags=["系统"], auth=None)
def health_check(request):
    """健康检查（公开访问）"""
    return {"status": "ok", "message": "服务运行正常"}


@api.get("/", tags=["系统"], auth=None)
def root(request):
    """API根路径（公开访问）"""
    return {"message": "Welcome to Hello-Django-Ninja-Api", "version": "1.0.0", "docs": "/api/docs", "redoc": "/api/redoc"}
