# IP 管理

<cite>
**本文档引用的文件**
- [src/core/middlewares/ip_limit_middleware.py](file://src/core/middlewares/ip_limit_middleware.py)
- [src/domain/security/entities/ip_blacklist_entity.py](file://src/domain/security/entities/ip_blacklist_entity.py)
- [src/domain/security/entities/ip_whitelist_entity.py](file://src/domain/security/entities/ip_whitelist_entity.py)
- [src/application/services/security_service.py](file://src/application/services/security_service.py)
- [src/infrastructure/repositories/security_repo_impl.py](file://src/infrastructure/repositories/security_repo_impl.py)
- [src/infrastructure/persistence/models/security_models.py](file://src/infrastructure/persistence/models/security_models.py)
- [src/domain/security/entities/rate_limit_entity.py](file://src/domain/security/entities/rate_limit_entity.py)
- [src/api/v1/controllers/security_controller.py](file://src/api/v1/controllers/security_controller.py)
- [src/api/v1/security_api.py](file://src/api/v1/security_api.py)
- [config/settings/base.py](file://config/settings/base.py)
- [src/application/dto/security/ip_blacklist_dto.py](file://src/application/dto/security/ip_blacklist_dto.py)
- [src/application/dto/security/ip_whitelist_dto.py](file://src/application/dto/security/ip_whitelist_dto.py)
- [src/core/exceptions/ip_blocked_error.py](file://src/core/exceptions/ip_blocked_error.py)
- [src/domain/security/repositories/security_repository.py](file://src/domain/security/repositories/security_repository.py)
</cite>

## 目录
1. [引言](#引言)
2. [项目结构](#项目结构)
3. [核心组件](#核心组件)
4. [架构总览](#架构总览)
5. [详细组件分析](#详细组件分析)
6. [依赖分析](#依赖分析)
7. [性能考量](#性能考量)
8. [故障排查指南](#故障排查指南)
9. [结论](#结论)
10. [附录](#附录)

## 引言
本文件面向“IP 管理”子系统，系统性阐述基于 Django + Django Ninja 的 IP 黑名单与白名单中间件设计、实体模型、仓储实现、API 控制器、配置策略、安全考量、监控与审计以及常见攻击防护策略。文档同时覆盖限流规则与记录的实体与仓储，便于统一理解安全防护体系。

## 项目结构
IP 管理相关代码分布在以下层次：
- 中介层：IPLimitMiddleware 负责请求阶段的 IP 白名单/黑名单判定
- 应用层：SecurityService 提供业务编排与 DTO 转换
- 领域层：IP 黑名单/白名单实体与限流实体定义业务规则
- 基础设施层：ORM 模型与仓储实现负责持久化与查询
- 接口层：Ninja 控制器与路由暴露管理 API
- 配置层：settings 中的黑白名单开关与限流开关

```mermaid
graph TB
subgraph "接口层"
C1["SecurityController<br/>src/api/v1/controllers/security_controller.py"]
C2["security_api.py<br/>Ninja 路由"]
end
subgraph "应用层"
S["SecurityService<br/>src/application/services/security_service.py"]
end
subgraph "领域层"
E1["IPBlacklistEntity<br/>src/domain/security/entities/ip_blacklist_entity.py"]
E2["IPWhitelistEntity<br/>src/domain/security/entities/ip_whitelist_entity.py"]
E3["RateLimitEntity<br/>src/domain/security/entities/rate_limit_entity.py"]
end
subgraph "基础设施层"
R["SecurityRepositoryImpl<br/>src/infrastructure/repositories/security_repo_impl.py"]
M["ORM 模型<br/>src/infrastructure/persistence/models/security_models.py"]
end
subgraph "中介层"
MW["IPLimitMiddleware<br/>src/core/middlewares/ip_limit_middleware.py"]
end
subgraph "配置层"
CFG["settings/base.py"]
end
C1 --> S
C2 --> S
S --> R
R --> M
MW --> M
CFG --> MW
CFG --> S
```

**图表来源**
- [src/api/v1/controllers/security_controller.py:21-302](file://src/api/v1/controllers/security_controller.py#L21-L302)
- [src/api/v1/security_api.py:1-285](file://src/api/v1/security_api.py#L1-L285)
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)
- [src/core/middlewares/ip_limit_middleware.py:15-130](file://src/core/middlewares/ip_limit_middleware.py#L15-L130)
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:15-130](file://src/core/middlewares/ip_limit_middleware.py#L15-L130)
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)
- [src/api/v1/controllers/security_controller.py:21-302](file://src/api/v1/controllers/security_controller.py#L21-L302)
- [src/api/v1/security_api.py:1-285](file://src/api/v1/security_api.py#L1-L285)
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)

## 核心组件
- IP 限制中间件：在请求进入阶段根据配置与数据库中的黑白名单进行拦截或放行
- 安全服务：封装业务逻辑，协调 DTO、实体与仓储
- 仓储实现：提供异步 CRUD 与查询能力，屏蔽 ORM 细节
- ORM 模型：定义 IP 黑名单、白名单与限流规则/记录的表结构与索引
- 实体模型：定义 IP 黑名单/白名单与限流规则的业务行为与校验
- 控制器与路由：对外暴露管理接口，支持新增、删除、查询与状态查看

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:15-130](file://src/core/middlewares/ip_limit_middleware.py#L15-L130)
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)
- [src/domain/security/entities/ip_blacklist_entity.py:11-53](file://src/domain/security/entities/ip_blacklist_entity.py#L11-L53)
- [src/domain/security/entities/ip_whitelist_entity.py:11-47](file://src/domain/security/entities/ip_whitelist_entity.py#L11-L47)
- [src/domain/security/entities/rate_limit_entity.py:11-106](file://src/domain/security/entities/rate_limit_entity.py#L11-L106)
- [src/api/v1/controllers/security_controller.py:21-302](file://src/api/v1/controllers/security_controller.py#L21-L302)
- [src/api/v1/security_api.py:1-285](file://src/api/v1/security_api.py#L1-L285)

## 架构总览
IP 管理采用分层架构，请求经由中间件与限流中间件后进入控制器，控制器调用应用服务，应用服务通过仓储访问 ORM 模型完成持久化与查询；同时，中间件在请求生命周期内执行 IP 白名单/黑名单判定。

```mermaid
sequenceDiagram
participant Client as "客户端"
participant MW as "IPLimitMiddleware"
participant Ctrl as "SecurityController"
participant Svc as "SecurityService"
participant Repo as "SecurityRepositoryImpl"
participant Model as "ORM 模型"
Client->>MW : "HTTP 请求"
MW->>MW : "_get_client_ip()"
MW->>Repo : "查询白名单/黑名单"
Repo->>Model : "ORM 查询"
Model-->>Repo : "实体/布尔结果"
Repo-->>MW : "判定结果"
MW-->>Client : "403 或放行"
Client->>Ctrl : "管理 API 请求"
Ctrl->>Svc : "业务方法"
Svc->>Repo : "CRUD/查询"
Repo->>Model : "ORM 操作"
Model-->>Repo : "持久化结果"
Repo-->>Svc : "实体/列表"
Svc-->>Ctrl : "DTO/响应"
Ctrl-->>Client : "JSON 响应"
```

**图表来源**
- [src/core/middlewares/ip_limit_middleware.py:41-76](file://src/core/middlewares/ip_limit_middleware.py#L41-L76)
- [src/infrastructure/repositories/security_repo_impl.py:46-108](file://src/infrastructure/repositories/security_repo_impl.py#L46-L108)
- [src/infrastructure/persistence/models/security_models.py:13-80](file://src/infrastructure/persistence/models/security_models.py#L13-L80)
- [src/api/v1/controllers/security_controller.py:49-185](file://src/api/v1/controllers/security_controller.py#L49-L185)
- [src/application/services/security_service.py:35-100](file://src/application/services/security_service.py#L35-L100)

## 详细组件分析

### IP 限制中间件（IPLimitMiddleware）
- 职责：在请求进入阶段根据配置决定是否启用白名单/黑名单模式，并据此放行或返回 403
- IP 解析：优先读取代理头，回退至 REMOTE_ADDR
- 白名单模式：仅允许白名单内的 IP 访问
- 黑名单模式：对黑名单内的 IP（含永久与临时）直接拒绝
- 配置项：IP_BLACKLIST_ENABLED、IP_WHITELIST_ENABLED

```mermaid
flowchart TD
Start(["进入中间件"]) --> GetIP["_get_client_ip()"]
GetIP --> Mode{"是否启用白名单/黑名单模式"}
Mode --> |白名单| CheckWL["_is_whitelisted(ip)"]
Mode --> |黑名单| CheckBL["_is_blacklisted(ip)"]
CheckWL --> WLRes{"是否在白名单"}
WLRes --> |否| DenyWL["返回 403不在白名单"]
WLRes --> |是| Next1["放行"]
CheckBL --> BLRes{"是否在黑名单"}
BLRes --> |是| DenyBL["返回 403在黑名单"]
BLRes --> |否| Next2["放行"]
DenyWL --> End(["结束"])
DenyBL --> End
Next1 --> End
Next2 --> End
```

**图表来源**
- [src/core/middlewares/ip_limit_middleware.py:41-76](file://src/core/middlewares/ip_limit_middleware.py#L41-L76)
- [src/core/middlewares/ip_limit_middleware.py:78-130](file://src/core/middlewares/ip_limit_middleware.py#L78-L130)

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:15-130](file://src/core/middlewares/ip_limit_middleware.py#L15-L130)
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)

### IP 黑名单实体（IPBlacklistEntity）
- 字段：标识、IP 地址、原因、是否永久、过期时间、创建时间、创建人
- 行为：校验必填、判断封禁是否生效、解除封禁、序列化
- 业务规则：永久封禁优先于过期时间；未过期即生效

```mermaid
classDiagram
class IPBlacklistEntity {
+string blacklist_id
+string ip_address
+string reason
+bool is_permanent
+datetime expires_at
+datetime created_at
+string created_by
+is_active() bool
+unban() void
+to_dict() dict
}
```

**图表来源**
- [src/domain/security/entities/ip_blacklist_entity.py:11-53](file://src/domain/security/entities/ip_blacklist_entity.py#L11-L53)

**章节来源**
- [src/domain/security/entities/ip_blacklist_entity.py:11-53](file://src/domain/security/entities/ip_blacklist_entity.py#L11-L53)

### IP 白名单实体（IPWhitelistEntity）
- 字段：标识、IP 地址、描述、是否激活、创建时间、创建人
- 行为：停用/激活、序列化
- 业务规则：仅激活状态有效

```mermaid
classDiagram
class IPWhitelistEntity {
+string whitelist_id
+string ip_address
+string description
+bool is_active
+datetime created_at
+string created_by
+deactivate() void
+activate() void
+to_dict() dict
}
```

**图表来源**
- [src/domain/security/entities/ip_whitelist_entity.py:11-47](file://src/domain/security/entities/ip_whitelist_entity.py#L11-L47)

**章节来源**
- [src/domain/security/entities/ip_whitelist_entity.py:11-47](file://src/domain/security/entities/ip_whitelist_entity.py#L11-L47)

### 安全服务（SecurityService）
- 职责：封装业务逻辑，协调 DTO、实体与仓储
- 黑名单：新增前检查重复、保存后转换响应 DTO
- 白名单：新增前检查重复、保存后转换响应 DTO
- 限流：创建规则前检查唯一性、切换状态、删除、查询列表、计算剩余配额
- 安全状态：统计黑白名单与活跃限流规则数量

```mermaid
classDiagram
class SecurityService {
+add_to_blacklist(dto, created_by) IPBlacklistResponseDTO
+remove_from_blacklist(ip_address) bool
+get_blacklist_entry(ip_address) IPBlacklistResponseDTO?
+list_blacklist() IPBlacklistResponseDTO[]
+add_to_whitelist(dto, created_by) IPWhitelistResponseDTO
+remove_from_whitelist(ip_address) bool
+list_whitelist() IPWhitelistResponseDTO[]
+create_rate_limit_rule(dto) RateLimitRuleResponseDTO
+toggle_rate_limit_rule(limit_id) RateLimitRuleResponseDTO
+delete_rate_limit_rule(limit_id) bool
+list_rate_limit_rules() RateLimitRuleResponseDTO[]
+get_rate_limit_status(key, endpoint, method) RateLimitStatusDTO
+get_security_status() dict
}
SecurityService --> SecurityRepository : "依赖"
```

**图表来源**
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/domain/security/repositories/security_repository.py:13-118](file://src/domain/security/repositories/security_repository.py#L13-L118)

**章节来源**
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/domain/security/repositories/security_repository.py:13-118](file://src/domain/security/repositories/security_repository.py#L13-L118)

### 仓储实现（SecurityRepositoryImpl）
- 职责：实现 SecurityRepository 接口，提供异步 CRUD 与查询
- 黑名单：新增、删除、按 IP 查询、判断是否封禁、列出（可排除过期）
- 白名单：新增、删除、按 IP 查询、判断是否在白名单、列出（可包含未激活）
- 限流：创建规则、按端点+方法查询、更新、删除、列出、获取或创建记录、递增计数、重置记录

```mermaid
classDiagram
class SecurityRepositoryImpl {
+add_to_blacklist(entity) IPBlacklistEntity
+remove_from_blacklist(ip_address) bool
+get_blacklist_entry(ip_address) IPBlacklistEntity?
+is_blacklisted(ip_address) bool
+list_blacklist(include_expired) IPBlacklistEntity[]
+add_to_whitelist(entity) IPWhitelistEntity
+remove_from_whitelist(ip_address) bool
+get_whitelist_entry(ip_address) IPWhitelistEntity?
+is_whitelisted(ip_address) bool
+list_whitelist(include_inactive) IPWhitelistEntity[]
+create_rate_limit_rule(entity) RateLimitEntity
+get_rate_limit_rule(endpoint, method) RateLimitEntity?
+update_rate_limit_rule(entity) RateLimitEntity
+delete_rate_limit_rule(limit_id) bool
+list_rate_limit_rules(is_active?) RateLimitEntity[]
+get_or_create_rate_limit_record(key, endpoint, method, window_seconds) RateLimitRecordEntity
+increment_rate_limit_count(record_id) int
+reset_rate_limit_record(record_id) void
}
SecurityRepositoryImpl ..|> SecurityRepository : "实现"
```

**图表来源**
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/domain/security/repositories/security_repository.py:13-118](file://src/domain/security/repositories/security_repository.py#L13-L118)

**章节来源**
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/domain/security/repositories/security_repository.py:13-118](file://src/domain/security/repositories/security_repository.py#L13-L118)

### ORM 模型（IPBlacklist/IPWhitelist/RateLimitRule/RateLimitRecord）
- IPBlacklist：UUID 主键、唯一 IP、原因、是否永久、过期时间、创建者外键
- IPWhitelist：UUID 主键、唯一 IP、描述、是否激活、创建者外键
- RateLimitRule：端点+方法唯一、速率、周期、作用域、是否激活
- RateLimitRecord：限流键+端点+方法复合索引、计数、窗口起始与过期时间

```mermaid
erDiagram
IP_BLACKLIST {
uuid id PK
genericipaddress ip_address UK
text reason
boolean is_permanent
datetime expires_at
datetime created_at
uuid created_by FK
}
IP_WHITELIST {
uuid id PK
genericipaddress ip_address UK
varchar description
boolean is_active
datetime created_at
uuid created_by FK
}
RATE_LIMIT_RULE {
uuid id PK
varchar name
varchar endpoint
varchar method
positiveint rate
positiveint period
varchar scope
boolean is_active
text description
datetime created_at
datetime updated_at
}
RATE_LIMIT_RECORD {
uuid id PK
varchar key
varchar endpoint
varchar method
positiveint count
datetime window_start
datetime expires_at
}
IP_BLACKLIST }o--|| USER : "created_by"
IP_WHITELIST }o--|| USER : "created_by"
```

**图表来源**
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)

**章节来源**
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)

### 限流实体（RateLimitEntity/RateLimitRecordEntity）
- RateLimitEntity：规则名称、端点、方法、速率、周期、作用域、是否激活、描述、时间戳
- RateLimitRecordEntity：限流键、端点、方法、计数、窗口起始、过期时间
- 行为：生成限流字符串、检查是否超限、激活/停用、序列化、递增计数、判断过期、重置

```mermaid
classDiagram
class RateLimitEntity {
+string limit_id
+string name
+string endpoint
+string method
+int rate
+int period
+string scope
+bool is_active
+string description
+datetime created_at
+datetime updated_at
+get_rate_string() string
+check_limit(current_count) bool
+activate() void
+deactivate() void
+to_dict() dict
}
class RateLimitRecordEntity {
+string record_id
+string key
+string endpoint
+string method
+int count
+datetime window_start
+datetime expires_at
+increment() int
+is_expired() bool
+reset() void
}
```

**图表来源**
- [src/domain/security/entities/rate_limit_entity.py:11-106](file://src/domain/security/entities/rate_limit_entity.py#L11-L106)

**章节来源**
- [src/domain/security/entities/rate_limit_entity.py:11-106](file://src/domain/security/entities/rate_limit_entity.py#L11-L106)

### 控制器与 API（SecurityController/security_api）
- 黑名单：新增、删除、列表查询
- 白名单：新增、删除、列表查询
- 限流：创建、切换状态、删除、列表查询
- 安全状态：统计黑白名单与活跃限流规则数量

```mermaid
sequenceDiagram
participant Client as "客户端"
participant Ctrl as "SecurityController"
participant Svc as "SecurityService"
participant Repo as "SecurityRepositoryImpl"
participant Model as "ORM 模型"
Client->>Ctrl : "POST /v1/security/blacklist"
Ctrl->>Svc : "add_to_blacklist(IPBlacklistDTO)"
Svc->>Repo : "get_blacklist_entry(ip)"
Repo->>Model : "查询是否存在"
Model-->>Repo : "存在/不存在"
Repo-->>Svc : "返回实体"
Svc->>Repo : "add_to_blacklist(entity)"
Repo->>Model : "持久化"
Model-->>Repo : "保存成功"
Repo-->>Svc : "返回实体"
Svc-->>Ctrl : "IPBlacklistResponseDTO"
Ctrl-->>Client : "JSON 响应"
```

**图表来源**
- [src/api/v1/controllers/security_controller.py:43-68](file://src/api/v1/controllers/security_controller.py#L43-L68)
- [src/application/services/security_service.py:35-54](file://src/application/services/security_service.py#L35-L54)
- [src/infrastructure/repositories/security_repo_impl.py:29-39](file://src/infrastructure/repositories/security_repo_impl.py#L29-L39)
- [src/infrastructure/persistence/models/security_models.py:13-50](file://src/infrastructure/persistence/models/security_models.py#L13-L50)

**章节来源**
- [src/api/v1/controllers/security_controller.py:21-302](file://src/api/v1/controllers/security_controller.py#L21-L302)
- [src/api/v1/security_api.py:1-285](file://src/api/v1/security_api.py#L1-L285)

## 依赖分析
- 中介层依赖配置项与仓储/模型
- 应用服务依赖 DTO、实体与仓储接口
- 仓储实现依赖 ORM 模型
- 控制器依赖应用服务
- 领域实体与 DTO 之间通过服务层转换

```mermaid
graph LR
MW["IPLimitMiddleware"] --> CFG["settings/base.py"]
MW --> Repo["SecurityRepositoryImpl"]
Ctrl["SecurityController"] --> Svc["SecurityService"]
Svc --> Repo
Repo --> Model["ORM 模型"]
Svc --> DTO["DTO 层"]
Svc --> Entity["领域实体"]
```

**图表来源**
- [src/core/middlewares/ip_limit_middleware.py:30-39](file://src/core/middlewares/ip_limit_middleware.py#L30-L39)
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)
- [src/application/services/security_service.py:24-32](file://src/application/services/security_service.py#L24-L32)
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:15-130](file://src/core/middlewares/ip_limit_middleware.py#L15-L130)
- [src/application/services/security_service.py:24-225](file://src/application/services/security_service.py#L24-L225)
- [src/infrastructure/repositories/security_repo_impl.py:21-260](file://src/infrastructure/repositories/security_repo_impl.py#L21-L260)
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)

## 性能考量
- 查询优化：IP 黑名单与白名单均使用唯一索引与数据库索引，降低查找成本
- 异步访问：仓储方法采用异步 ORM 接口，提升高并发下的吞吐
- 限流窗口：限流记录按键+端点+方法建立复合索引，减少锁竞争
- 缓存建议：结合 Redis 缓存热点 IP 的黑白名单状态，减少数据库压力（需在仓储层扩展）

[本节为通用性能建议，不直接分析具体文件]

## 故障排查指南
- IP 被封禁异常：当 IP 在黑名单中且未过期时触发
- 中间件未生效：确认配置项 IP_BLACKLIST_ENABLED / IP_WHITELIST_ENABLED 是否正确设置
- 白名单/黑名单重复：服务层在新增前会检查重复，避免重复条目
- 限流规则冲突：端点+方法唯一约束，创建前需确保唯一性
- 日志定位：中间件与应用层使用日志记录关键事件，便于审计与排错

**章节来源**
- [src/core/exceptions/ip_blocked_error.py:9-26](file://src/core/exceptions/ip_blocked_error.py#L9-L26)
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)
- [src/application/services/security_service.py:39-42](file://src/application/services/security_service.py#L39-L42)
- [src/infrastructure/persistence/models/security_models.py:126-126](file://src/infrastructure/persistence/models/security_models.py#L126-L126)

## 结论
本 IP 管理子系统通过中间件与应用服务协同，结合实体与仓储实现，提供了完善的 IP 黑名单/白名单与限流能力。配置灵活、扩展性强，适合在生产环境中部署。建议配合缓存与更细粒度的审计日志进一步增强性能与可观测性。

## 附录

### 配置策略
- 黑名单/白名单开关：通过环境变量控制
- 限流开关与默认值：通过环境变量控制
- 示例键名：
  - IP_BLACKLIST_ENABLED
  - IP_WHITELIST_ENABLED
  - RATE_LIMIT_ENABLED
  - RATE_LIMIT_DEFAULT

**章节来源**
- [config/settings/base.py:232-235](file://config/settings/base.py#L232-L235)

### 数据模型字段定义（摘要）
- IPBlacklist：ip_address（唯一）、is_permanent、expires_at、created_by
- IPWhitelist：ip_address（唯一）、is_active、description、created_by
- RateLimitRule：endpoint、method（唯一组合）、rate、period、scope、is_active
- RateLimitRecord：key、endpoint、method、count、window_start、expires_at

**章节来源**
- [src/infrastructure/persistence/models/security_models.py:13-162](file://src/infrastructure/persistence/models/security_models.py#L13-L162)

### 安全考虑与最佳实践
- IP 欺骗防护：中间件优先读取代理头并截断逗号分隔列表的第一个值，避免伪造
- CIDR 网段处理：当前模型为单 IP，若需网段匹配，可在服务层扩展为 CIDR 检查并在仓储层增加范围查询
- IPv6 支持：模型使用 GenericIPAddressField，天然支持 IPv4/IPv6
- 限流策略：按 IP/用户/全局三种作用域灵活配置，结合 Redis 缓存提升性能

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:78-93](file://src/core/middlewares/ip_limit_middleware.py#L78-L93)
- [src/infrastructure/persistence/models/security_models.py:20-20](file://src/infrastructure/persistence/models/security_models.py#L20-L20)
- [src/domain/security/entities/rate_limit_entity.py:11-106](file://src/domain/security/entities/rate_limit_entity.py#L11-L106)

### 监控与审计
- 中间件日志：对命中白名单/黑名单的 IP 记录警告日志
- 安全状态接口：提供黑名单/白名单/限流规则数量等状态信息
- 建议扩展：在仓储层增加审计记录表，记录每次变更的时间、操作人与上下文

**章节来源**
- [src/core/middlewares/ip_limit_middleware.py:56-56](file://src/core/middlewares/ip_limit_middleware.py#L56-L56)
- [src/api/v1/controllers/security_controller.py:286-302](file://src/api/v1/controllers/security_controller.py#L286-L302)