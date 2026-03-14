# Hello-Django-Ninja-Api 系统设计文档（基于UV管理 & DDD & RBAC架构）

---

## 1. 项目概述

**项目名称**：Hello-Django-Ninja-Api  
**功能描述**：基于 Django 和 Django-Ninja 框架，结合 JWT 与 RBAC 权限认证机制，采用领域驱动设计（DDD）架构，打造高度模块化与可扩展的 API 服务系统。  
本系统重点支持权限精细化控制、多版本管理（UV管理）、API限流、黑白名单等功能，大幅提升系统可用性和健壮性，最大限度减少代码重复，提升系统可维护性和业务扩展能力。  
系统设计充分考虑AI开发的便利性，采用标准化的模块结构和清晰的依赖关系，便于AI助手进行代码生成和系统构建。

---

## 2. 设计目标

- 基于 **DDD** 架构，清晰划分业务领域与技术实现分层。
- 引入 **RBAC**（基于角色的访问控制）认证授权，增强权限管理灵活度。
- 采用 **UV管理**，单元版本化，支持模块独立演进。
- 目录结构合理规划，避免代码冗余，提高复用率。
- 结合 Django-Ninja 提供高性能、高类型安全的 REST API。
- 支持 JWT 认证，满足现代前后端分离业务需求。
- 实现API限流、黑白名单等安全防护机制。
- 使用Django生态成熟插件，提升系统健壮性。
- 实现高可用性、高性能、可监控的系统架构。
- **AI友好设计**：标准化模块结构，便于AI助手开发和维护。

---

## 3. 技术架构

```mermaid
graph TD
    subgraph "客户端层"
        Client[Web客户端<br/>Mobile App<br/>第三方服务]
    end
    
    subgraph "API网关层"
        Gateway[Nginx负载均衡<br/>API Gateway]
    end
    
    subgraph "应用服务层"
        ApiLayer[API层 - Django-Ninja]
        Application[应用层]
        Domain[领域层]
        Infrastructure[基础设施层]
    end
    
    subgraph "安全防护层"
        RateLimit[DRF-Rate-Limit<br/>API限流]
        BlackWhiteList[IP黑白名单<br/>访问控制]
        Security[Security中间件<br/>防护]
    end
    
    subgraph "数据存储层"
        Database[(PostgreSQL主库)]
        Cache[(Redis缓存)]
        Logs[(日志存储)]
    end
    
    subgraph "认证授权层"
        AuthService[JWT认证服务]
        RBACModule[RBAC权限管理]
    end
    
    Client --> Gateway
    Gateway --> ApiLayer
    ApiLayer --> RateLimit
    RateLimit --> ApiLayer
    ApiLayer --> Application
    Application --> Domain
    Domain --> Infrastructure
    Domain --> Database
    Domain --> Cache
    AuthService --> ApiLayer
    RBACModule --> ApiLayer
    BlackWhiteList --> ApiLayer
    Security --> ApiLayer
    Infrastructure --> Logs
```

### 3.1 技术栈

| 层级       | 技术/工具                             | 说明                              |
|------------|--------------------------------------|-----------------------------------|
| 开发语言   | Python 3.10+                        | 稳定主流Python版本                |
| Web框架    | Django 4.x                         | Web后端基础框架                   |
| API框架    | Django-Ninja                      | 类型安全、高性能API框架            |
| 认证       | djangorestframework-simplejwt + RBAC | JWT认证结合角色权限管理          |
| 限流       | django-ratelimit/drf-rate-limit    | API请求频率限制                   |
| IP管理     | django-ipware                      | IP地址识别与管理                  |
| ORM        | Django ORM                       | 对象关系映射                     |
| 缓存       | Redis                            | 高性能内存缓存                    |
| 数据库     | PostgreSQL                      | 关系型数据库，支持事务与高并发    |
| 版本管理   | UV管理                          | 单元模块版本管理                     |
| 设计模式   | DDD（领域驱动设计）               | 业务复杂系统拆分和设计指导          |
| 日志管理   | Django内置日志系统                | 结构化日志记录与存储               |
| 容器化     | Docker                           | 容器化部署                        |
| 安全防护   | django-cors-headersdjango-defenderdjango-securitydjango-ratelimit | 多层安全防护 |

---

## 4. 领域驱动设计（DDD）架构解析

### 4.1 分层说明

| 层级           | 职责描述                              |
|----------------|-------------------------------------|
| 接口层(API层)  | 提供REST API接口，调用应用层逻辑，处理HTTP请求响应 |
| 应用层         | 负责编排业务流程，协调领域层服务和基础设施 |
| 领域层         | 业务核心，包含实体(Entity)、值对象(Value Object)、聚合根(Aggregate Root)、领域服务 |
| 基础设施层     | 数据库访问、认证、外部服务接口实现、缓存管理 |

### 4.2 业务领域划分（核心领域）

| 领域            | 主要功能                                 |
|-----------------|--------------------------------------|
| 用户管理域(User)| 用户注册、信息维护、JWT登录认证、个人资料管理 |
| 权限管理域(RBAC)| 角色管理、权限分配、访问控制、权限验证 |
| 认证域(Auth)    | JWT 生成、验证与刷新、会话管理、安全控制 |
| 通用服务域(Core)| 通用的工具函数、中间件、异常处理、配置管理 |
| 业务服务域(Business)| 具体业务逻辑处理，如订单、商品、支付等 |
| 安全域(Security)| API限流、IP黑白名单、安全防护、攻击检测 |

### 4.3 领域模型设计原则

- **聚合根**：每个聚合都有唯一的聚合根，负责维护聚合内的一致性
- **值对象**：不可变对象，用于描述实体的属性特征
- **领域服务**：处理跨实体的业务逻辑
- **仓储模式**：抽象数据访问逻辑，实现领域与基础设施解耦

---

## 5. AI友好的目录结构（结合UV & DDD）

```plaintext
Hello-Django-Ninja-Api/
├── docker/
│   ├── Dockerfile                 # 应用容器构建文件
│   └── docker-compose.yml         # 服务编排配置
├── src/
│   ├── api/                      # API接口层（Django-Ninja路由及视图）
│   │   ├── v1/                   # 版本控制 - v1版本
│   │   │   ├── __init__.py       # 包初始化
│   │   │   ├── user_api.py       # 用户相关API - AI可直接实现
│   │   │   ├── auth_api.py       # 认证相关API - AI可直接实现
│   │   │   ├── rbac_api.py       # 权限管理API - AI可直接实现
│   │   │   ├── security_api.py   # 安全相关API - AI可直接实现
│   │   │   └── business_apis/    # 业务API子目录
│   │   │       ├── order_api.py  # 订单API - AI可直接实现
│   │   │       └── product_api.py # 商品API - AI可直接实现
│   │   ├── v2/                   # 版本控制 - v2版本
│   │   │   ├── __init__.py       # 包初始化
│   │   │   └── user_api_v2.py    # 用户相关API v2 - AI可直接实现
│   │   └── common.py             # API公共组件 - AI可直接实现
│   ├── application/              # 应用层
│   │   ├── services/             # 应用服务 - AI可直接实现
│   │   │   ├── user_service.py   # 用户领域服务
│   │   │   ├── auth_service.py   # 认证服务
│   │   │   ├── rbac_service.py   # RBAC服务
│   │   │   ├── security_service.py # 安全服务
│   │   │   └── business_services/ # 业务应用服务
│   │   │       ├── order_service.py
│   │   │       └── product_service.py
│   │   ├── dto/                  # 数据传输对象 - AI可直接实现
│   │   │   ├── user_dto.py       # 用户DTO
│   │   │   ├── auth_dto.py       # 认证DTO
│   │   │   ├── rbac_dto.py       # RBAC DTO
│   │   │   └── security_dto.py   # 安全DTO
│   │   └── interfaces/           # 应用层接口定义 - AI可直接实现
│   │       └── base_service.py
│   ├── domain/                   # 领域层（实体、聚合根、领域服务、仓储接口）
│   │   ├── user/                 # 用户领域 - AI可直接实现
│   │   │   ├── entities/         # 用户实体
│   │   │   │   ├── user_entity.py # 用户实体
│   │   │   │   └── profile_entity.py # 用户档案实体
│   │   │   ├── value_objects/    # 用户相关值对象
│   │   │   │   ├── email.py      # 邮箱值对象
│   │   │   │   └── phone.py      # 电话值对象
│   │   │   ├── repositories/     # 用户仓储接口定义
│   │   │   │   └── user_repository.py
│   │   │   ├── services/         # 用户领域服务
│   │   │   │   └── user_domain_service.py
│   │   │   └── events/           # 用户领域事件
│   │   │       └── user_events.py
│   │   ├── rbac/                 # 权限管理领域 - AI可直接实现
│   │   │   ├── entities/         # 角色、权限实体
│   │   │   │   ├── role_entity.py
│   │   │   │   └── permission_entity.py
│   │   │   ├── value_objects/    # 角色权限值对象
│   │   │   │   └── permission_value_object.py
│   │   │   ├── repositories/     # 权限管理仓储接口
│   │   │   │   └── rbac_repository.py
│   │   │   └── services/         # 权限领域服务
│   │   │       └── rbac_domain_service.py
│   │   ├── auth/                 # 认证领域 - AI可直接实现
│   │   │   ├── entities/         # 认证实体
│   │   │   │   └── token_entity.py
│   │   │   ├── services/         # 认证领域服务
│   │   │   │   └── auth_domain_service.py
│   │   │   └── factories/        # 认证工厂
│   │   │       └── token_factory.py
│   │   ├── security/             # 安全领域 - AI可直接实现
│   │   │   ├── entities/         # 安全实体
│   │   │   │   ├── rate_limit_entity.py # 限流实体
│   │   │   │   ├── ip_blacklist_entity.py # IP黑名单实体
│   │   │   │   └── ip_whitelist_entity.py # IP白名单实体
│   │   │   ├── services/         # 安全领域服务
│   │   │   │   ├── rate_limit_service.py
│   │   │   │   ├── ip_filter_service.py
│   │   │   │   └── security_domain_service.py
│   │   │   └── factories/        # 安全工厂
│   │   │       └── security_factory.py
│   │   └── business/             # 业务领域 - AI可直接实现
│   │       ├── order/            # 订单领域
│   │       └── product/          # 商品领域
│   ├── infrastructure/           # 基础设施层
│   │   ├── repositories/         # 仓储实现 - AI可直接实现
│   │   │   ├── user_repo_impl.py # 用户数据持久化实现
│   │   │   ├── rbac_repo_impl.py # 权限持久化实现
│   │   │   ├── security_repo_impl.py # 安全数据持久化实现
│   │   │   └── base_repository.py # 基础仓储
│   │   ├── persistence/          # 持久化层
│   │   │   ├── models/           # Django模型 - AI可直接实现
│   │   │   │   ├── user_models.py
│   │   │   │   ├── auth_models.py
│   │   │   │   ├── rbac_models.py
│   │   │   │   └── security_models.py
│   │   │   └── migrations/       # 数据库迁移
│   │   ├── auth_jwt/             # JWT工具库 - AI可直接实现
│   │   │   ├── jwt_manager.py    # JWT管理器
│   │   │   └── token_validator.py # Token验证器
│   │   ├── cache/                # 缓存实现 - AI可直接实现
│   │   │   ├── redis_cache.py    # Redis缓存实现
│   │   │   └── cache_manager.py  # 缓存管理器
│   │   ├── rate_limit/           # 限流实现 - AI可直接实现
│   │   │   ├── drf_rate_limit.py # DRF限流实现
│   │   │   └── rate_limit_manager.py # 限流管理器
│   │   ├── ip_management/        # IP管理 - AI可直接实现
│   │   │   ├── ip_filter.py      # IP过滤器
│   │   │   └── ip_manager.py     # IP管理器
│   │   ├── external/             # 外部服务接口 - AI可直接实现
│   │   │   └── third_party_api.py # 第三方API接口
│   │   ├── config/               # 配置管理 - AI可直接实现
│   │   │   └── database_config.py
│   │   └── monitoring/           # 监控组件 - AI可直接实现
│   │       └── metrics_collector.py
│   ├── core/                     # 通用功能模块 - AI可直接实现
│   │   ├── exceptions.py         # 自定义异常
│   │   ├── middlewares.py        # 中间件
│   │   ├── decorators.py         # 装饰器
│   │   ├── validators.py         # 验证器
│   │   ├── utils.py              # 工具函数
│   │   ├── constants.py          # 常量定义
│   │   └── logger.py             # 日志配置
│   └── tests/                    # 测试代码 - AI可直接实现
│       ├── unit/                 # 单元测试
│       ├── integration/          # 集成测试
│       └── fixtures/             # 测试数据
├── config/                       # 配置文件 - AI可直接实现
│   ├── settings/                 # 配置文件
│   │   ├── base.py               # 基础配置
│   │   ├── development.py        # 开发环境配置
│   │   ├── production.py         # 生产环境配置
│   │   └── testing.py            # 测试环境配置
│   ├── urls.py                   # 路由汇总 - AI可直接实现
│   ├── asgi.py
│   └── wsgi.py
├── scripts/                      # 脚本文件 - AI可直接实现
│   ├── migrate.sh                # 数据库迁移脚本
│   ├── deploy.sh                 # 部署脚本
│   └── backup.sh                 # 备份脚本
├── logs/                         # 日志文件目录
│   ├── app.log                   # 应用日志
│   ├── error.log                 # 错误日志
│   └── access.log                # 访问日志
├── docs/                         # 文档
│   ├── api_docs/                 # API文档
│   └── design_docs/              # 设计文档
├── .env.example                  # 环境变量示例
├── .gitignore
├── requirements.txt              # 依赖包列表 - AI可直接实现
├── requirements-dev.txt          # 开发依赖 - AI可直接实现
├── manage.py                     # Django管理脚本 - AI可直接实现
└── README.md                     # 项目说明 - AI可直接实现
```

---

## 6. 开发规范

### 6.1 代码规范
- **代码风格**: 符合 PEP 8 规范，使用 Ruff 自动格式化
- **类型提示**: 所有公共接口使用类型提示，使用 MyPy 检查
- **文档字符串**: 使用 Google 风格 docstring
- **代码质量**: Ruff 0 错误，MyPy 宽松模式通过

### 6.2 测试规范
- **测试框架**: pytest + pytest-django
- **测试覆盖**: 核心业务逻辑覆盖率 ≥ 80%
- **测试类型**: 单元测试、集成测试
- **测试配置**: `pyproject.toml`

### 6.3 Git 工作流
- **分支模型**: Git Flow
  - `main`: 生产环境分支
  - `develop`: 开发主分支
  - `feature/*`: 功能开发分支
  - `bugfix/*`: 缺陷修复分支
  - `hotfix/*`: 紧急修复分支
- **提交信息**: 语义化提交（feat/fix/docs/refactor/test/chore）

---

## 7. RBAC认证设计

### 7.1 核心概念
- **用户(User)**：访问系统的主体
- **角色(Role)**：一组权限的集合
- **权限(Permission)**：系统操作的访问许可
- **资源(Resource)**：受权限控制的对象

### 7.2 权限控制流程
1. 用户登录获取包含角色和权限的 JWT Token
2. 访问接口时解析 Token 获取身份和权限
3. RBAC 模块验证接口和数据访问权限
4. 记录操作日志

### 7.3 JWT认证
- Token 包含用户ID、角色、权限、组织信息
- 支持刷新和黑名单机制
- 支持多设备登录和强制登出

---

## 8. 安全设计

### 8.1 安全特性
- **认证**: bcrypt 密码加密，JWT Token
- **授权**: RBAC 细粒度权限控制
- **防护**: API 限流、IP 黑白名单、XSS/CSRF 防护
- **审计**: 操作日志记录

### 8.2 安全组件
- django-cors-headers: CORS 跨域控制
- django-ratelimit: 请求频率限制
- django-defender: 登录失败封禁
- django-security: 安全头设置

---

---

## 9. 性能优化

### 9.1 数据库优化
- 索引优化、避免 N+1 查询
- 连接池管理
- 支持读写分离

### 9.2 缓存策略
- Redis 缓存热点数据
- 本地缓存频繁访问数据
- 缓存穿透防护

### 9.3 异步处理
- 支持异步 API（Django-Ninja）
- 可集成 Celery 任务队列
- 事件驱动机制

---

## 10. 日志管理

### 10.1 日志分类
- 应用日志、错误日志、访问日志、安全日志

### 10.2 日志特性
- 结构化日志（JSON 格式）
- 分级记录（DEBUG/INFO/WARNING/ERROR）
- 自动归档和清理

---

---

## 11. 关键设计优势

- **分层清晰**: DDD 架构，职责单一，易于维护
- **权限完善**: RBAC 细粒度权限控制
- **类型安全**: Django-Ninja + Pydantic 类型提示
- **安全防护**: 多层安全机制（限流、黑白名单、认证授权）
- **性能优化**: 缓存、异步、数据库优化
- **易于测试**: 分层设计便于单元测试和集成测试
- **AI 友好**: 标准化模块结构

---

## 12. 部署架构

支持多种部署方式：
- **开发环境**: Docker Compose 一键启动
- **生产环境**: Gunicorn + Nginx + PostgreSQL + Redis
- **容器化**: Docker + Kubernetes

---

---

## 19. 快速开始

### 19.1 环境要求

- Python >= 3.10.11
- UV（Python包管理工具）
- SQLite（开发环境）或 PostgreSQL（生产环境）
- Redis（缓存，可选）

### 19.2 本地环境搭建

#### 方式一：自动化安装脚本（推荐）

**Linux/Mac:**
```bash
# 运行安装脚本
bash scripts/setup_dev.sh
```

**Windows:**
```cmd
# 运行安装脚本
scripts\setup_dev.bat
```

脚本将自动完成以下操作：
1. 检查并安装 UV
2. 创建 Python 虚拟环境（Python 3.10.11）
3. 安装项目依赖
4. 代码格式化和检查
5. 创建数据库表
6. 创建初始管理员账号
7. 运行单元测试

#### 方式二：手动安装

```bash
# 1. 安装 UV（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# 或 PowerShell（Windows）
# irm https://astral.sh/uv/install.ps1 | iex

# 2. 创建虚拟环境
uv venv --python 3.10.11

# 3. 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate.bat  # Windows

# 4. 安装项目依赖（包含开发依赖）
uv pip install -e ".[dev]"

# 5. 数据库迁移
python manage.py makemigrations
python manage.py migrate --run-syncdb

# 6. 创建初始管理员账号
python scripts/init_admin.py

# 7. 启动开发服务器
python manage.py runserver
```

### 19.3 服务启动

```bash
# 激活虚拟环境后启动服务
python manage.py runserver

# 指定端口
python manage.py runserver 0.0.0.0:8000
```

服务启动后，访问：
- API根路径: http://localhost:8000/
- API文档: http://localhost:8000/api/docs
- ReDoc文档: http://localhost:8000/api/redoc

### 19.4 初始账号

默认初始管理员账号：
- **用户名**: `admin`
- **密码**: `admin123`
- **邮箱**: `admin@example.com`

⚠️ **重要提示**：生产环境部署后请立即修改默认密码！

可通过环境变量自定义初始账号：
```bash
export ADMIN_USERNAME=myadmin
export ADMIN_EMAIL=myadmin@example.com
export ADMIN_PASSWORD=mypassword123
python scripts/init_admin.py
```

### 19.5 代码规范检查

#### Ruff 代码检查

```bash
# 检查代码
ruff check .

# 自动修复问题
ruff check . --fix

# 代码格式化
ruff format .
```

#### MyPy 类型检查

```bash
# 运行类型检查
mypy src/

# MyPy 配置在宽松模式下运行
# 138个类型错误是Django ORM的已知限制，不影响项目运行
```

#### 一键检查脚本

```bash
# 运行所有检查
bash scripts/lint.sh
```

### 19.6 单元测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models/test_user_models.py

# 运行特定测试
pytest tests/test_models/test_user_models.py::TestUserModel::test_create_user

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 仅运行单元测试
pytest -m unit

# 仅运行集成测试
pytest -m integration
```

测试配置：
- 使用 `pytest` + `pytest-django` 测试框架
- 配置文件：`pyproject.toml`
- 测试路径：`tests/`
- 期望覆盖率：> 80%

### 19.7 服务部署

#### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 生产环境部署

1. **环境变量配置**

创建 `.env` 文件：
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://host:port/0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **数据库迁移**

```bash
python manage.py migrate --settings=config.settings.production
```

3. **收集静态文件**

```bash
python manage.py collectstatic --settings=config.settings.production
```

4. **使用 Gunicorn + Nginx 部署**

```bash
# 安装 gunicorn
pip install gunicorn

# 启动服务
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

5. **使用 Supervisor 管理进程**

```ini
[program:django-ninja-api]
directory=/path/to/Hello-Django-Ninja-Api
command=/path/to/.venv/bin/gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django-ninja-api.log
```

### 19.8 数据库管理

```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations

# 回滚迁移
python manage.py migrate app_name migration_name

# Django Shell
python manage.py shell
```

### 19.9 常用命令

```bash
# 创建超级用户
python manage.py createsuperuser

# Django 管理命令
python manage.py shell
python manage.py dbshell

# 清除缓存（如使用Redis）
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## 20. 开发工作流

### 20.1 代码提交前检查

```bash
# 1. 运行代码检查
ruff check . --fix
ruff format .

# 2. 运行类型检查
mypy src/

# 3. 运行测试
pytest

# 4. 提交代码
git add .
git commit -m "feat: your message"
```

### 20.2 分支策略

- `main`: 生产环境分支
- `develop`: 开发主分支
- `feature/*`: 功能开发分支
- `bugfix/*`: 缺陷修复分支
- `hotfix/*`: 紧急修复分支

### 20.3 代码质量标准

- **代码风格**: 符合 PEP 8 规范
- **类型提示**: 所有公共接口使用类型提示
- **文档字符串**: 使用 Google 风格 docstring
- **测试覆盖**: 核心业务逻辑覆盖率 ≥ 80%
- **代码检查**: 通过 Ruff 检查（0 错误）
- **类型检查**: MyPy 类型检查通过（宽松模式）

---

## 21. 故障排查

### 21.1 常见问题

**问题1: 模块导入错误**
```bash
# 解决方案：确保在虚拟环境中操作
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat  # Windows
```

**问题2: 数据库迁移失败**
```bash
# 解决方案：删除迁移文件重新创建
rm -rf src/infrastructure/persistence/migrations/*.py
python manage.py makemigrations
python manage.py migrate
```

**问题3: Redis 连接失败**
```bash
# 解决方案：启动 Redis 服务
redis-server
# 或使用 Docker
docker run -d -p 6379:6379 redis:latest
```

**问题4: 端口被占用**
```bash
# 解决方案：使用其他端口
python manage.py runserver 0.0.0.0:8001
```

### 21.2 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log

# 查看访问日志
tail -f logs/access.log
```

---

## 13. 后续扩展

- 事件驱动机制（Domain Events）
- 微服务架构
- OAuth 2.0 认证
- API 网关统一鉴权
- Kubernetes 编排部署
- DevOps 自动化流水线

---

## 14. 总结

本系统采用 **DDD 架构**，结合 **RBAC 权限控制** 和 **JWT 认证**，构建了结构清晰、职责明确、模块独立的现代化后端 API 服务。系统集成了 **API 限流、IP 黑白名单、多层安全防护** 等功能，具备高可用性、高性能、易扩展、强安全的特点，适合作为企业级应用的技术蓝本。

---

*更新日期：2026年3月7日*