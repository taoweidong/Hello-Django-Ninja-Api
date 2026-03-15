"""
常量定义
Constants - 项目常量定义
"""

# ========== 用户相关常量 ==========

# 用户名规则
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 50
USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"

# 密码规则
PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 100

# 手机号
PHONE_PATTERN = r"^1[3-9]\d{9}$"

# 邮箱
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


# ========== RBAC相关常量 ==========

# 系统角色代码
ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_GUEST = "guest"
ROLE_MODERATOR = "moderator"

# 系统角色名称
ROLE_NAMES = {ROLE_ADMIN: "管理员", ROLE_USER: "普通用户", ROLE_GUEST: "访客", ROLE_MODERATOR: "版主"}

# 资源类型
RESOURCE_USER = "user"
RESOURCE_ROLE = "role"
RESOURCE_PERMISSION = "permission"
RESOURCE_SYSTEM = "system"
RESOURCE_API = "api"

# 操作类型
ACTION_READ = "read"
ACTION_CREATE = "create"
ACTION_UPDATE = "update"
ACTION_DELETE = "delete"
ACTION_MANAGE = "manage"


# ========== API相关常量 ==========

# HTTP方法
METHOD_GET = "GET"
METHOD_POST = "POST"
METHOD_PUT = "PUT"
METHOD_PATCH = "PATCH"
METHOD_DELETE = "DELETE"

# 限流范围
SCOPE_IP = "ip"
SCOPE_USER = "user"
SCOPE_GLOBAL = "global"

# 默认限流配置
DEFAULT_RATE_LIMIT = "100/minute"
DEFAULT_RATE_LIMIT_PERIOD = 60


# ========== Token相关常量 ==========

# Token类型
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# Token过期时间（秒）
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1小时
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7天


# ========== 分页相关常量 ==========

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1


# ========== 缓存相关常量 ==========

# 缓存过期时间（秒）
CACHE_USER_EXPIRE = 1800  # 30分钟
CACHE_PERMISSION_EXPIRE = 600  # 10分钟
CACHE_ROLE_EXPIRE = 600  # 10分钟


# ========== 状态码 ==========

# 成功
SUCCESS_CODE = 0
SUCCESS_MESSAGE = "操作成功"

# 错误
ERROR_CODE = 1
ERROR_MESSAGE = "操作失败"

# 认证错误
AUTH_ERROR_CODE = 401
AUTH_ERROR_MESSAGE = "认证失败"

# 权限错误
PERMISSION_ERROR_CODE = 403
PERMISSION_ERROR_MESSAGE = "权限不足"

# 资源不存在
NOT_FOUND_ERROR_CODE = 404
NOT_FOUND_ERROR_MESSAGE = "资源不存在"

# 验证错误
VALIDATION_ERROR_CODE = 422
VALIDATION_ERROR_MESSAGE = "数据验证失败"

# 限流错误
RATE_LIMIT_ERROR_CODE = 429
RATE_LIMIT_ERROR_MESSAGE = "请求过于频繁"

# 服务器错误
SERVER_ERROR_CODE = 500
SERVER_ERROR_MESSAGE = "服务器错误"


# ========== 日志相关常量 ==========

# 日志级别
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
