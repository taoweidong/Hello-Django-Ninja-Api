# 认证 API

<cite>
**本文引用的文件**
- [src/api/app.py](file://src/api/app.py)
- [src/api/v1/auth_api.py](file://src/api/v1/auth_api.py)
- [src/api/v1/controllers/auth_controller.py](file://src/api/v1/controllers/auth_controller.py)
- [src/application/services/auth_service.py](file://src/application/services/auth_service.py)
- [src/application/dto/auth/token_response_dto.py](file://src/application/dto/auth/token_response_dto.py)
- [src/application/dto/auth/refresh_token_dto.py](file://src/application/dto/auth/refresh_token_dto.py)
- [src/application/dto/user/user_login_dto.py](file://src/application/dto/user/user_login_dto.py)
- [src/infrastructure/auth_jwt/jwt_manager.py](file://src/infrastructure/auth_jwt/jwt_manager.py)
- [src/infrastructure/auth_jwt/token_validator.py](file://src/infrastructure/auth_jwt/token_validator.py)
- [src/infrastructure/persistence/models/auth_models.py](file://src/infrastructure/persistence/models/auth_models.py)
- [config/settings/base.py](file://config/settings/base.py)
- [tests/test_api/test_auth_api.py](file://tests/test_api/test_auth_api.py)
- [src/core/middlewares/security_middleware.py](file://src/core/middlewares/security_middleware.py)
- [src/core/exceptions/authentication_error.py](file://src/core/exceptions/authentication_error.py)
</cite>

## 目录
1. [简介](#简介)
2. [项目结构](#项目结构)
3. [核心组件](#核心组件)
4. [架构总览](#架构总览)
5. [详细组件分析](#详细组件分析)
6. [依赖分析](#依赖分析)
7. [性能考虑](#性能考虑)
8. [故障排查指南](#故障排查指南)
9. [结论](#结论)
10. [附录](#附录)

## 简介
本文件为认证 API 的权威技术文档，覆盖用户登录、令牌刷新、用户登出等认证相关接口的完整规范。内容包括：
- 接口定义：HTTP 方法、URL 路径、请求参数、响应格式与状态码
- 完整请求/响应示例：成功登录获取 JWT 令牌、使用刷新令牌获取新访问令牌、用户登出撤销令牌
- 认证机制实现原理：JWT 令牌生成、验证与刷新流程
- 登录日志记录：IP 地址、用户代理、设备信息的采集与持久化
- 错误处理与常见问题：认证失败的错误分类与解决方案
- 安全考虑与最佳实践：生产环境安全头、令牌撤销、速率限制与 IP 黑白名单

## 项目结构
认证相关模块采用分层架构设计，遵循关注点分离与依赖倒置原则：
- 表现层：Ninja/NinjaExtra 控制器负责接收请求、解析 DTO、返回响应
- 应用层：AuthService 封装业务逻辑，协调 JWT 管理器、令牌验证器、缓存与持久化
- 基础设施层：JWT 管理器与令牌验证器负责编码/解码与黑名单校验；ORM 模型持久化登录日志与刷新令牌
- 配置层：Django/REST Framework SIMPLE_JWT 配置控制令牌生命周期与算法

```mermaid
graph TB
subgraph "表现层"
C1["AuthController<br/>src/api/v1/controllers/auth_controller.py"]
R1["Router<br/>src/api/v1/auth_api.py"]
end
subgraph "应用层"
S1["AuthService<br/>src/application/services/auth_service.py"]
end
subgraph "基础设施层"
J1["JWTManager<br/>src/infrastructure/auth_jwt/jwt_manager.py"]
V1["TokenValidator<br/>src/infrastructure/auth_jwt/token_validator.py"]
M1["Models<br/>src/infrastructure/persistence/models/auth_models.py"]
end
subgraph "配置层"
G1["SIMPLE_JWT 配置<br/>config/settings/base.py"]
end
C1 --> S1
R1 --> C1
S1 --> J1
S1 --> V1
S1 --> M1
G1 --> J1
G1 --> V1
```

图表来源
- [src/api/v1/controllers/auth_controller.py:16-133](file://src/api/v1/controllers/auth_controller.py#L16-L133)
- [src/api/v1/auth_api.py:13-74](file://src/api/v1/auth_api.py#L13-L74)
- [src/application/services/auth_service.py:20-233](file://src/application/services/auth_service.py#L20-L233)
- [src/infrastructure/auth_jwt/jwt_manager.py:13-147](file://src/infrastructure/auth_jwt/jwt_manager.py#L13-L147)
- [src/infrastructure/auth_jwt/token_validator.py:11-108](file://src/infrastructure/auth_jwt/token_validator.py#L11-L108)
- [src/infrastructure/persistence/models/auth_models.py:12-114](file://src/infrastructure/persistence/models/auth_models.py#L12-L114)
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)

章节来源
- [src/api/app.py:24-30](file://src/api/app.py#L24-L30)
- [src/api/v1/controllers/auth_controller.py:16-133](file://src/api/v1/controllers/auth_controller.py#L16-L133)
- [src/api/v1/auth_api.py:13-74](file://src/api/v1/auth_api.py#L13-L74)
- [src/application/services/auth_service.py:20-233](file://src/application/services/auth_service.py#L20-L233)
- [src/infrastructure/auth_jwt/jwt_manager.py:13-147](file://src/infrastructure/auth_jwt/jwt_manager.py#L13-L147)
- [src/infrastructure/auth_jwt/token_validator.py:11-108](file://src/infrastructure/auth_jwt/token_validator.py#L11-L108)
- [src/infrastructure/persistence/models/auth_models.py:12-114](file://src/infrastructure/persistence/models/auth_models.py#L12-L114)
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)

## 核心组件
- 认证控制器：提供 /v1/auth/login、/v1/auth/refresh、/v1/auth/logout 三个接口，负责参数解析与响应封装
- 认证服务：实现登录、刷新、登出、令牌验证等核心业务逻辑，协调 JWT 管理器与令牌验证器
- JWT 管理器：负责访问令牌与刷新令牌的生成、解码、验证与过期判断
- 令牌验证器：负责访问令牌有效性校验、刷新令牌校验与黑名单检查
- 持久化模型：RefreshToken、TokenBlacklist、LoginLog 三类模型分别支持刷新令牌持久化、令牌撤销黑名单与登录日志
- 配置：SIMPLE_JWT 控制令牌生命周期、算法与头部类型

章节来源
- [src/api/v1/controllers/auth_controller.py:16-133](file://src/api/v1/controllers/auth_controller.py#L16-L133)
- [src/application/services/auth_service.py:20-233](file://src/application/services/auth_service.py#L20-L233)
- [src/infrastructure/auth_jwt/jwt_manager.py:13-147](file://src/infrastructure/auth_jwt/jwt_manager.py#L13-L147)
- [src/infrastructure/auth_jwt/token_validator.py:11-108](file://src/infrastructure/auth_jwt/token_validator.py#L11-L108)
- [src/infrastructure/persistence/models/auth_models.py:12-114](file://src/infrastructure/persistence/models/auth_models.py#L12-L114)
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)

## 架构总览
认证流程由“控制器 → 应用服务 → JWT/验证器 → 持久化/缓存”构成，形成清晰的职责边界。

```mermaid
sequenceDiagram
participant Client as "客户端"
participant Ctrl as "AuthController"
participant Svc as "AuthService"
participant JWT as "JWTManager"
participant Val as "TokenValidator"
participant DB as "ORM模型"
Client->>Ctrl : "POST /v1/auth/login"
Ctrl->>Svc : "login(login_dto, ip, ua, device)"
Svc->>DB : "查询用户并校验密码"
Svc->>JWT : "create_access_token / create_refresh_token"
Svc->>DB : "保存刷新令牌"
Svc->>DB : "创建登录日志"
Svc-->>Ctrl : "TokenResponseDTO"
Ctrl-->>Client : "200 OK + 访问/刷新令牌"
Client->>Ctrl : "POST /v1/auth/refresh"
Ctrl->>Svc : "refresh_access_token(refresh_dto)"
Svc->>Val : "validate_refresh_token"
Svc->>JWT : "create_access_token"
Svc-->>Ctrl : "TokenResponseDTO"
Ctrl-->>Client : "200 OK + 新访问令牌"
Client->>Ctrl : "POST /v1/auth/logout"
Ctrl->>Svc : "logout(access_token)"
Svc->>Val : "revoke_token"
Svc-->>Ctrl : "成功"
Ctrl-->>Client : "200 OK + 登出成功"
```

图表来源
- [src/api/v1/controllers/auth_controller.py:36-133](file://src/api/v1/controllers/auth_controller.py#L36-L133)
- [src/application/services/auth_service.py:26-180](file://src/application/services/auth_service.py#L26-L180)
- [src/infrastructure/auth_jwt/jwt_manager.py:25-80](file://src/infrastructure/auth_jwt/jwt_manager.py#L25-L80)
- [src/infrastructure/auth_jwt/token_validator.py:21-103](file://src/infrastructure/auth_jwt/token_validator.py#L21-L103)
- [src/infrastructure/persistence/models/auth_models.py:12-44](file://src/infrastructure/persistence/models/auth_models.py#L12-L44)

## 详细组件分析

### 接口规范与示例

- 登录接口
  - 方法与路径：POST /v1/auth/login
  - 请求体 DTO：UserLoginDTO（字段：username、password、device_info）
  - 响应 DTO：TokenResponseDTO（字段：access_token、refresh_token、token_type、expires_in、user）
  - 状态码：200 成功；400/500 失败（如凭据错误、用户未激活）
  - 示例请求体（JSON）：参见 DTO 示例字段
  - 示例响应（JSON）：参见 DTO 示例字段
  - 说明：接口会采集客户端 IP 与 User-Agent，并记录登录日志

- 刷新令牌接口
  - 方法与路径：POST /v1/auth/refresh
  - 请求体 DTO：RefreshTokenDTO（字段：refresh_token）
  - 响应 DTO：TokenResponseDTO（仅返回新的 access_token 与 expires_in）
  - 状态码：200 成功；400/500 失败（如刷新令牌无效或已过期）
  - 示例请求体（JSON）：参见 DTO 示例字段
  - 示例响应（JSON）：参见 DTO 示例字段

- 登出接口
  - 方法与路径：POST /v1/auth/logout
  - 请求头：Authorization: Bearer <access_token>
  - 响应 DTO：MessageResponse（字段：message）
  - 状态码：200 成功；无 Authorization 头时仍返回成功
  - 示例请求头：Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  - 示例响应（JSON）：{"message": "登出成功"}

章节来源
- [src/api/v1/controllers/auth_controller.py:36-133](file://src/api/v1/controllers/auth_controller.py#L36-L133)
- [src/api/v1/auth_api.py:22-74](file://src/api/v1/auth_api.py#L22-L74)
- [src/application/dto/user/user_login_dto.py:9-28](file://src/application/dto/user/user_login_dto.py#L9-L28)
- [src/application/dto/auth/refresh_token_dto.py:9-22](file://src/application/dto/auth/refresh_token_dto.py#L9-L22)
- [src/application/dto/auth/token_response_dto.py:9-32](file://src/application/dto/auth/token_response_dto.py#L9-L32)
- [tests/test_api/test_auth_api.py:23-87](file://tests/test_api/test_auth_api.py#L23-L87)

### 认证机制与流程

- 令牌生成
  - 访问令牌：包含 user_id、username、roles、permissions、iat/exp/jti 等声明
  - 刷新令牌：包含 user_id、username、iat/exp/jti 等声明
  - 生命周期：由 SIMPLE_JWT 配置决定（分钟级）

- 令牌验证
  - 访问令牌：验证签名、类型为 access、不在黑名单、未过期
  - 刷新令牌：验证签名、类型为 refresh、不在黑名单、未过期

- 刷新流程
  - 使用 refresh_token 向 /v1/auth/refresh 发起请求
  - 服务端验证刷新令牌后，签发新的访问令牌

- 登出流程
  - 客户端携带 Bearer Token 调用 /v1/auth/logout
  - 服务端撤销该访问令牌（加入黑名单），并清理用户相关缓存

```mermaid
flowchart TD
Start(["开始"]) --> ValidateCreds["校验用户名/密码"]
ValidateCreds --> CredsOK{"凭据有效？"}
CredsOK -- "否" --> LogFail["记录登录失败日志"] --> End(["结束"])
CredsOK -- "是" --> GenTokens["生成访问/刷新令牌"]
GenTokens --> SaveRT["保存刷新令牌到数据库"]
SaveRT --> UpdateLastLogin["更新用户最后登录时间"]
UpdateLastLogin --> LogSuccess["记录登录成功日志"]
LogSuccess --> ReturnResp["返回TokenResponseDTO"]
ReturnResp --> End
```

图表来源
- [src/application/services/auth_service.py:26-112](file://src/application/services/auth_service.py#L26-L112)
- [src/infrastructure/auth_jwt/jwt_manager.py:25-80](file://src/infrastructure/auth_jwt/jwt_manager.py#L25-L80)
- [src/infrastructure/persistence/models/auth_models.py:12-44](file://src/infrastructure/persistence/models/auth_models.py#L12-L44)

章节来源
- [src/infrastructure/auth_jwt/jwt_manager.py:25-143](file://src/infrastructure/auth_jwt/jwt_manager.py#L25-L143)
- [src/infrastructure/auth_jwt/token_validator.py:21-103](file://src/infrastructure/auth_jwt/token_validator.py#L21-L103)
- [src/application/services/auth_service.py:113-180](file://src/application/services/auth_service.py#L113-L180)

### 数据模型与日志记录

- RefreshToken 模型
  - 字段：user、token、jti、device_info、ip_address、is_revoked、expires_at、created_at
  - 用途：持久化刷新令牌，支持按 jti 建索引

- TokenBlacklist 模型
  - 字段：jti、user、token_type、revoked_at、expires_at
  - 用途：记录已撤销令牌，配合缓存实现黑名单

- LoginLog 模型
  - 字段：user、username、ip_address、user_agent、device_info、browser、os、login_status、fail_reason、login_time
  - 用途：记录登录事件，便于审计与风控

```mermaid
erDiagram
USER ||--o{ REFRESH_TOKEN : "拥有多个"
USER ||--o{ LOGIN_LOG : "拥有多个"
USER ||--o{ TOKEN_BLACKLIST : "拥有多个"
REFRESH_TOKEN {
uuid id PK
uuid user_id FK
string token UK
string jti UK
string device_info
ip_address ip_address
boolean is_revoked
datetime expires_at
datetime created_at
}
TOKEN_BLACKLIST {
uuid id PK
string jti UK
uuid user_id FK
enum token_type
datetime revoked_at
datetime expires_at
}
LOGIN_LOG {
uuid id PK
uuid user_id FK
string username
ip_address ip_address
text user_agent
string device_info
string browser
string os
boolean login_status
string fail_reason
datetime login_time
}
```

图表来源
- [src/infrastructure/persistence/models/auth_models.py:12-114](file://src/infrastructure/persistence/models/auth_models.py#L12-L114)

章节来源
- [src/infrastructure/persistence/models/auth_models.py:12-114](file://src/infrastructure/persistence/models/auth_models.py#L12-L114)

### 类与依赖关系

```mermaid
classDiagram
class AuthController {
+login(request, login_dto) TokenResponseDTO
+refresh_token(refresh_dto) TokenResponseDTO
+logout(authorization) MessageResponse
}
class AuthService {
+login(login_dto, ip_address, user_agent, device_info) TokenResponseDTO
+refresh_access_token(refresh_dto) TokenResponseDTO
+logout(access_token) bool
+verify_token(token) (bool, dict|None)
}
class JWTManager {
+create_access_token(...)
+create_refresh_token(...)
+verify_token(token) (bool, dict|None)
+decode_token(token) dict|None
+is_token_expired(token) bool
}
class TokenValidator {
+is_token_valid(token) (bool, str|None, dict|None)
+validate_refresh_token(token) (bool, str|None, dict|None)
+revoke_token(token) bool
+is_blacklisted(jti) bool
}
AuthController --> AuthService : "依赖"
AuthService --> JWTManager : "使用"
AuthService --> TokenValidator : "使用"
AuthService --> RefreshToken : "持久化"
AuthService --> LoginLog : "持久化"
```

图表来源
- [src/api/v1/controllers/auth_controller.py:16-133](file://src/api/v1/controllers/auth_controller.py#L16-L133)
- [src/application/services/auth_service.py:20-233](file://src/application/services/auth_service.py#L20-L233)
- [src/infrastructure/auth_jwt/jwt_manager.py:13-147](file://src/infrastructure/auth_jwt/jwt_manager.py#L13-L147)
- [src/infrastructure/auth_jwt/token_validator.py:11-108](file://src/infrastructure/auth_jwt/token_validator.py#L11-L108)
- [src/infrastructure/persistence/models/auth_models.py:12-44](file://src/infrastructure/persistence/models/auth_models.py#L12-L44)

## 依赖分析
- 控制器依赖应用服务，应用服务依赖 JWT 管理器与令牌验证器，以及 ORM 模型与缓存
- SIMPLE_JWT 配置影响令牌生命周期与算法，从而影响登录、刷新与验证行为
- 安全中间件在生产环境添加安全响应头，提升传输层安全性

```mermaid
graph LR
Ctrl["AuthController"] --> Svc["AuthService"]
Svc --> JWT["JWTManager"]
Svc --> TV["TokenValidator"]
Svc --> Models["ORM Models"]
Cfg["SIMPLE_JWT 配置"] --> JWT
Cfg --> TV
Sec["SecurityMiddleware"] --> Resp["HTTP 响应"]
```

图表来源
- [src/api/v1/controllers/auth_controller.py:16-133](file://src/api/v1/controllers/auth_controller.py#L16-L133)
- [src/application/services/auth_service.py:20-233](file://src/application/services/auth_service.py#L20-L233)
- [src/infrastructure/auth_jwt/jwt_manager.py:13-147](file://src/infrastructure/auth_jwt/jwt_manager.py#L13-L147)
- [src/infrastructure/auth_jwt/token_validator.py:11-108](file://src/infrastructure/auth_jwt/token_validator.py#L11-L108)
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)
- [src/core/middlewares/security_middleware.py:46-52](file://src/core/middlewares/security_middleware.py#L46-L52)

章节来源
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)
- [src/core/middlewares/security_middleware.py:46-52](file://src/core/middlewares/security_middleware.py#L46-L52)

## 性能考虑
- 缓存与黑名单：令牌撤销通过 Redis 缓存实现，避免频繁数据库查询
- 过期时间：访问令牌短周期（分钟级），刷新令牌长周期（默认 24 小时），降低刷新频率
- 异步操作：登录、刷新、登出均采用异步实现，减少阻塞
- 数据库索引：RefreshToken 模型对 user 与 jti 建立索引，提升查询效率

## 故障排查指南
- 常见错误与处理
  - 用户名或密码错误：登录失败并记录失败日志，返回 500
  - 用户未激活：登录失败并记录失败日志，返回 500
  - 刷新令牌无效或已过期：返回 400/500
  - 令牌类型不正确：访问令牌校验失败，返回 400/500
  - 令牌已失效/已撤销：访问令牌校验失败，返回 400/500
  - 令牌过期：访问令牌校验失败，返回 400/500
- 建议排查步骤
  - 确认 SIMPLE_JWT 配置（算法、生命周期、头部类型）
  - 检查 Redis 是否可用，确认黑名单键空间
  - 核对请求头 Authorization 是否为 Bearer Token
  - 查看 LoginLog 与 TokenBlacklist 表，定位失败原因
- 相关异常类
  - AuthenticationError：认证失败统一异常基类

章节来源
- [src/application/services/auth_service.py:36-112](file://src/application/services/auth_service.py#L36-L112)
- [src/infrastructure/auth_jwt/token_validator.py:21-103](file://src/infrastructure/auth_jwt/token_validator.py#L21-L103)
- [src/core/exceptions/authentication_error.py:9-26](file://src/core/exceptions/authentication_error.py#L9-L26)

## 结论
本认证 API 采用清晰的分层架构与完善的令牌生命周期管理，结合登录日志与黑名单机制，提供了高可用、可观测且安全的认证能力。建议在生产环境中启用安全响应头、合理配置令牌生命周期，并结合速率限制与 IP 黑白名单进一步强化安全防护。

## 附录

### 接口一览表
- 登录
  - 方法：POST
  - 路径：/v1/auth/login
  - 请求体：UserLoginDTO
  - 响应：TokenResponseDTO
  - 状态码：200、400、500
- 刷新令牌
  - 方法：POST
  - 路径：/v1/auth/refresh
  - 请求体：RefreshTokenDTO
  - 响应：TokenResponseDTO
  - 状态码：200、400、500
- 登出
  - 方法：POST
  - 路径：/v1/auth/logout
  - 请求头：Authorization: Bearer <access_token>
  - 响应：MessageResponse
  - 状态码：200

### 配置要点
- SIMPLE_JWT 关键项
  - ACCESS_TOKEN_LIFETIME：访问令牌生命周期（分钟）
  - REFRESH_TOKEN_LIFETIME：刷新令牌生命周期（分钟）
  - ALGORITHM：签名算法（默认 HS256）
  - AUTH_HEADER_TYPES：授权头部类型（默认 Bearer）
- 安全响应头（生产环境）
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security: max-age=31536000; includeSubDomains

章节来源
- [config/settings/base.py:137-151](file://config/settings/base.py#L137-L151)
- [src/core/middlewares/security_middleware.py:46-52](file://src/core/middlewares/security_middleware.py#L46-L52)