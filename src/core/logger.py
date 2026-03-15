"""
日志配置
Logger - 日志配置和日志器
"""

import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings


def get_logger(name: str = None) -> logging.Logger:
    """
    获取日志器
    """
    logger = logging.getLogger(name) if name else logging.getLogger("src")

    # 避免重复配置
    if logger.handlers:
        return logger

    # 设置日志级别
    log_level = getattr(settings, "LOG_LEVEL", "INFO")
    logger.setLevel(getattr(logging, log_level.upper()))

    # 创建日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    if settings.DEBUG:
        # 开发环境只输出到控制台
        return logger

    # 生产环境输出到文件
    log_dir = settings.BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    # 应用日志
    app_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding="utf-8",
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)
    logger.addHandler(app_handler)

    # 错误日志
    error_handler = RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding="utf-8",
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    # 访问日志
    access_handler = RotatingFileHandler(
        log_dir / "access.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding="utf-8",
    )
    access_handler.setFormatter(formatter)
    access_handler.setLevel(logging.INFO)

    # 访问日志器
    access_logger = logging.getLogger("access")
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)

    return logger


# 预定义的日志器
logger = get_logger("src")
auth_logger = get_logger("src.auth")
security_logger = get_logger("src.security")
api_logger = get_logger("src.api")


def log_request(request, response=None, error=None):
    """记录请求日志"""
    log_data = {
        "method": request.method,
        "path": request.path,
        "ip": request.META.get("REMOTE_ADDR"),
        "user": str(request.user) if request.user.is_authenticated else "anonymous",
    }

    if response:
        log_data["status"] = response.status_code

    if error:
        log_data["error"] = str(error)
        api_logger.error(f"API Error: {log_data}", exc_info=True)
    else:
        api_logger.info(f"API Request: {log_data}")


def log_auth_event(event_type: str, user_id: str = None, ip: str = None, success: bool = True, message: str = None):
    """记录认证事件"""
    log_data = {"event_type": event_type, "success": success, "user_id": user_id, "ip": ip, "message": message}

    if success:
        auth_logger.info(f"Auth Event: {log_data}")
    else:
        auth_logger.warning(f"Auth Event: {log_data}")


def log_security_event(event_type: str, ip: str = None, details: str = None):
    """记录安全事件"""
    log_data = {"event_type": event_type, "ip": ip, "details": details}

    security_logger.warning(f"Security Event: {log_data}")
