# 开发指南

## 环境要求

- Python >= 3.10.11
- Docker (可选)
- Redis (可选)

## 快速开始

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

### 2. 激活虚拟环境

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

或使用 UV:
```bash
uv pip install -e ".[dev]"
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件配置相关参数
```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户

```bash
python manage.py createsuperuser
```

### 7. 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 http://127.0.0.1:8000/ 启动

## 开发工具

### 代码格式化 (Ruff)

```bash
# 格式化代码
ruff format .

# 检查代码
ruff check .

# 自动修复问题
ruff check . --fix
```

### 类型检查 (MyPy)

```bash
# 类型检查
mypy src/
```

### 运行测试 (Pytest)

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models/test_user_models.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 运行所有检查

```bash
# Linux/Mac
bash scripts/lint.sh
bash scripts/test.sh

# Windows
scripts\lint.bat
scripts\test.bat
```

## 项目结构

```
Hello-Django-Ninja-Api/
├── docker/                    # Docker 配置
├── src/
│   ├── api/                   # API 层
│   │   ├── common.py         # API 通用配置
│   │   └── v1/               # API v1 版本
│   ├── application/           # 应用层
│   │   ├── dto/              # 数据传输对象
│   │   └── services/         # 应用服务
│   ├── domain/               # 领域层
│   │   ├── user/            # 用户领域
│   │   ├── rbac/            # RBAC 权限领域
│   │   ├── auth/            # 认证领域
│   │   └── security/        # 安全领域
│   ├── infrastructure/       # 基础设施层
│   │   ├── persistence/     # 数据库持久化
│   │   ├── repositories/    # 仓储实现
│   │   ├── auth_jwt/       # JWT 认证
│   │   ├── cache/          # 缓存实现
│   │   ├── rate_limit/     # 限流
│   │   └── ip_management/  # IP 管理
│   └── core/                # 核心模块
│       ├── exceptions.py    # 异常处理
│       ├── middlewares.py   # 中间件
│       ├── utils.py        # 工具函数
│       ├── constants.py    # 常量
│       └── logger.py       # 日志
├── config/                  # 配置
│   ├── settings/           # Django 设置
│   ├── urls.py             # URL 路由
│   ├── wsgi.py             # WSGI 配置
│   └── asgi.py             # ASGI 配置
├── tests/                   # 测试
│   ├── test_models/        # 模型测试
│   ├── test_api/           # API 测试
│   ├── test_services/      # 服务测试
│   └── test_middlewares/   # 中间件测试
├── scripts/                # 脚本
├── logs/                   # 日志文件
├── manage.py              # Django 管理脚本
├── pyproject.toml         # 项目配置 (UV)
├── ruff.toml              # Ruff 配置
├── .mypy.ini              # MyPy 配置
├── requirements.txt       # 依赖列表
└── .env.example           # 环境变量示例
```

## API 文档

启动服务器后，访问以下地址查看 API 文档：

- Swagger UI: http://127.0.0.1:8000/api/docs
- ReDoc: http://127.0.0.1:8000/api/redoc

## Docker 部署

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

## 常见问题

### 1. 数据库迁移失败

```bash
# 清理迁移文件
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# 重新生成迁移
python manage.py makemigrations
python manage.py migrate
```

### 2. Redis 连接失败

确保 Redis 服务正在运行：

```bash
# Windows
redis-server

# Linux/Mac
sudo systemctl start redis
```

### 3. 端口被占用

更改端口：

```bash
python manage.py runserver 8080
```

## 贡献指南

1. 遵循 PEP 8 编码规范
2. 运行代码检查和测试
3. 提交前格式化代码
4. 编写清晰的提交信息
