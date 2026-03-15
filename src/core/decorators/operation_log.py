"""
操作日志装饰器
Operation Log Decorator - 自动记录API操作日志
"""

import contextlib
import json
from collections.abc import Callable
from functools import wraps

from django.http import HttpRequest

from src.infrastructure.repositories.system_repo_impl import SystemRepository


def operation_log(module: str, description: str | None = None):
    """
    操作日志装饰器

    用法:
        @operation_log(module="用户管理", description="创建用户")
        async def create_user(request, dto):
            ...

    Args:
        module: 模块名称
        description: 操作描述（可选）
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取request对象
            request = None
            for arg in args:
                if isinstance(arg, HttpRequest):
                    request = arg
                    break

            # 执行原函数
            response = None
            error = None
            status_code = 200
            response_result = None

            try:
                response = await func(*args, **kwargs)
                status_code = getattr(response, "status_code", 200)
                response_result = json.dumps(response, ensure_ascii=False) if response else None
            except Exception as e:
                error = e
                status_code = getattr(e, "status_code", 500)
                response_result = str(e)

            # 记录操作日志（异步）
            if request:
                with contextlib.suppress(Exception):
                    await _log_operation(request, module, description, status_code, response_result)

            # 如果有错误，重新抛出
            if error:
                raise error

            return response

        return wrapper

    return decorator


async def _log_operation(
    request: HttpRequest, module: str, description: str | None, status_code: int, response_result: str | None
) -> None:
    """记录操作日志"""
    repo = SystemRepository()

    # 获取用户信息
    user_id = None
    if hasattr(request, "user") and request.user.is_authenticated:
        user_id = request.user.id

    # 获取请求信息
    path = request.path
    method = request.method

    # 获取请求体
    body = None
    if request.body:
        try:
            body = request.body.decode("utf-8")
            # 限制请求体长度
            if len(body) > 10000:
                body = body[:10000] + "..."
        except Exception:
            body = None

    # 获取IP地址
    ipaddress = _get_client_ip(request)

    # 获取浏览器和系统信息
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    browser, system = _parse_user_agent(user_agent)

    # 创建日志记录
    await repo.create_operation_log(
        user_id=user_id,
        module=module,
        path=path,
        method=method,
        body=body,
        ipaddress=ipaddress,
        browser=browser,
        system=system,
        response_code=status_code,
        response_result=response_result,
        status_code=status_code,
        description=description or f"{method} {path}",
    )


def _get_client_ip(request: HttpRequest) -> str:
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR", "")
    return ip[:39] if ip else ""


def _parse_user_agent(user_agent: str) -> tuple[str, str]:
    """
    解析User-Agent字符串
    返回: (浏览器, 操作系统)
    """
    browser = "Unknown"
    system = "Unknown"

    # 解析浏览器
    if "Chrome" in user_agent:
        browser = "Chrome"
    elif "Firefox" in user_agent:
        browser = "Firefox"
    elif "Safari" in user_agent:
        browser = "Safari"
    elif "Edge" in user_agent:
        browser = "Edge"
    elif "Opera" in user_agent or "OPR" in user_agent:
        browser = "Opera"
    elif "MSIE" in user_agent or "Trident" in user_agent:
        browser = "Internet Explorer"

    # 解析操作系统
    if "Windows" in user_agent:
        system = "Windows"
    elif "Mac" in user_agent:
        system = "MacOS"
    elif "Linux" in user_agent:
        system = "Linux"
    elif "Android" in user_agent:
        system = "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        system = "iOS"

    return browser[:64], system[:64]
