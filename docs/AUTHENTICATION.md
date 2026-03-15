# 接口鉴权机制

## 概述

本系统采用 **全局默认鉴权，豁免标记** 的权限控制策略。所有接口默认需要 JWT 身份验证，只有明确标记 `auth=NOT_SET` 的接口才允许匿名访问。

## 鉴权流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        请求到达                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              GlobalAuth.authenticate() 全局认证检查               │
│                                                                 │
│   1. 提取 Authorization Header 中的 Bearer Token                 │
│   2. 验证 Token 有效性（签名、过期时间、黑名单）                    │
│   3. 解析 JWT Payload 并注入到请求对象                            │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────────┐
│   auth=NOT_SET          │     │      默认鉴权                    │
│   (豁免鉴权)             │     │      (需要验证)                  │
│                         │     │                                 │
│   跳过认证直接放行        │     │   Token 有效 → 继续处理          │
│                         │     │   Token 无效 → 返回 401          │
└─────────────────────────┘     └─────────────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     执行业务逻辑                                 │
│                                                                 │
│   可通过 request.user_id 和 request.user_payload 获取用户信息    │
└─────────────────────────────────────────────────────────────────┘
```

## 核心配置

### 全局认证类

```python
# src/infrastructure/auth_jwt/global_auth.py
from ninja.security import HttpBearer
from src.infrastructure.auth_jwt.token_validator import token_validator

class GlobalAuth(HttpBearer):
    """全局认证类 - 基于 JWT Bearer Token"""

    def authenticate(self, request, token: str):
        is_valid, error_msg, payload = token_validator.is_token_valid(token)
        if is_valid and payload:
            # 注入用户信息到请求对象
            request.user_id = payload.get("user_id")
            request.user_payload = payload
            return payload
        return None
```

### API 实例配置

```python
# src/api/app.py
from ninja.constants import NOT_SET
from ninja_extra import NinjaExtraAPI
from src.infrastructure.auth_jwt import GlobalAuth

# 创建 API 实例，配置全局认证
api = NinjaExtraAPI(
    title="Hello-Django-Ninja-Api",
    auth=GlobalAuth(),  # 全局默认鉴权
)

# 豁免鉴权的公开接口
@api.get("/health", auth=NOT_SET)
def health_check(request):
    return {"status": "ok"}
```

## 使用方式

### 默认鉴权（无需额外配置）

所有接口默认需要鉴权，不需要任何额外标记：

```python
from ninja_extra import api_controller, http_get

@api_controller("/v1/users")
class UserController:

    @http_get("/list")
    async def list_users(self):
        # 需要鉴权（默认行为）
        pass

    @http_get("/{user_id}")
    async def get_user(self, user_id: str):
        # 需要鉴权（默认行为）
        pass
```

### 豁免鉴权

只有少数公开接口需要豁免鉴权，使用 `auth=NOT_SET`：

```python
from ninja.constants import NOT_SET
from ninja_extra import api_controller, http_post

@api_controller("/v1/auth")
class AuthController:

    @http_post("/login", auth=NOT_SET)
    async def login(self, login_dto: UserLoginDTO):
        # 豁免鉴权，允许匿名访问
        pass

    @http_post("/refresh", auth=NOT_SET)
    async def refresh_token(self, refresh_dto: RefreshTokenDTO):
        # 豁免鉴权，允许匿名访问
        pass
```

### 获取当前用户信息

鉴权成功后，用户信息会自动注入到请求对象：

```python
from ninja_extra import http_get

@http_get("/me")
async def get_current_user(self, request):
    user_id = request.user_id          # 用户ID
    payload = request.user_payload     # 完整的 JWT Payload
    username = payload.get("username")
    roles = payload.get("roles", [])
    return {"user_id": user_id, "username": username}
```

## 公开接口清单

以下接口无需鉴权即可访问（已标记 `auth=NOT_SET`）：

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | API 根路径 |
| `/health` | GET | 健康检查 |
| `/v1/auth/login` | POST | 用户登录 |
| `/v1/auth/refresh` | POST | 刷新令牌 |
| `/v1/auth/logout` | POST | 用户登出 |
| `/v1/users` | POST | 用户注册 |
| `/v1/system/health` | GET | 系统健康检查 |

## 注意事项

### 1. 新增接口默认需要鉴权

新增接口时，**无需任何额外配置**，默认就需要鉴权：

```python
# 默认需要鉴权，无需额外标记
@http_post("/data")
async def create_data(self, dto: DataDTO):
    pass
```

### 2. 公开接口必须显式豁免

只有公开接口才需要添加 `auth=NOT_SET`：

```python
from ninja.constants import NOT_SET

@http_get("/public-info", auth=NOT_SET)
async def get_public_info(self):
    pass
```

### 3. Token 格式要求

请求需要在 Header 中携带 Bearer Token：

```
Authorization: Bearer <your_jwt_token>
```

### 4. 认证失败响应

Token 无效或缺失时，返回 `401 Unauthorized`：

```json
{
    "detail": "Unauthorized"
}
```

### 5. 控制器级别豁免

如果整个控制器都需要公开访问，可以在每个方法上添加 `auth=NOT_SET`：

```python
from ninja.constants import NOT_SET

@api_controller("/v1/public")
class PublicController:

    @http_get("/info", auth=NOT_SET)
    async def get_info(self):
        pass

    @http_get("/config", auth=NOT_SET)
    async def get_config(self):
        pass
```

### 6. 权限检查（可选）

如果需要额外的权限检查（如特定角色或权限），可以在业务逻辑中实现：

```python
from ninja.errors import HttpError

@http_delete("/users/{user_id}")
async def delete_user(self, request, user_id: str):
    # 检查是否有删除权限
    roles = request.user_payload.get("roles", [])
    if "admin" not in roles:
        raise HttpError(403, "权限不足")

    # 执行删除逻辑
    pass
```

## 相关文件

| 文件 | 说明 |
|------|------|
| `src/infrastructure/auth_jwt/global_auth.py` | 全局认证类 |
| `src/infrastructure/auth_jwt/token_validator.py` | Token 验证器 |
| `src/infrastructure/auth_jwt/jwt_manager.py` | JWT 管理器 |
| `src/api/app.py` | API 实例配置 |
| `src/api/v1/controllers/auth_controller.py` | 认证控制器示例 |
| `src/api/v1/controllers/user_controller.py` | 用户控制器示例 |
