"""
工具函数
Utilities - 常用工具函数
"""

import hashlib
import json
import re
import uuid
from datetime import datetime
from typing import Any


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


def generate_short_uuid() -> str:
    """生成短UUID"""
    return uuid.uuid4().hex[:8]


def hash_password(password: str, salt: str = "") -> str:
    """密码哈希"""
    combined = f"{password}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()


def verify_password(password: str, hashed: str, salt: str = "") -> bool:
    """验证密码"""
    return hash_password(password, salt) == hashed


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证手机号格式"""
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_username(username: str) -> bool:
    """验证用户名格式"""
    pattern = r"^[a-zA-Z0-9_]{3,50}$"
    return bool(re.match(pattern, username))


def mask_email(email: str) -> str:
    """邮箱脱敏"""
    if "@" not in email:
        return email
    local, domain = email.split("@")
    masked_local = local[0] + "*" if len(local) <= 2 else local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"


def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if len(phone) != 11:
        return phone
    return phone[:3] + "****" + phone[7:]


def get_client_ip(request) -> str:
    """获取客户端IP"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR", "127.0.0.1")
    return ip


def get_user_agent(request) -> str:
    """获取用户代理"""
    return request.META.get("HTTP_USER_AGENT", "")


def parse_user_agent(user_agent: str) -> dict[str, str]:
    """解析用户代理"""
    result = {"browser": "Unknown", "os": "Unknown", "device": "Unknown"}

    # 简单解析
    if "Chrome" in user_agent:
        result["browser"] = "Chrome"
    elif "Firefox" in user_agent:
        result["browser"] = "Firefox"
    elif "Safari" in user_agent:
        result["browser"] = "Safari"
    elif "Edge" in user_agent:
        result["browser"] = "Edge"

    if "Windows" in user_agent:
        result["os"] = "Windows"
    elif "Mac" in user_agent:
        result["os"] = "Mac"
    elif "Linux" in user_agent:
        result["os"] = "Linux"
    elif "Android" in user_agent:
        result["os"] = "Android"
    elif "iOS" in user_agent:
        result["os"] = "iOS"

    return result


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime | None:
    """解析日期时间"""
    try:
        return datetime.strptime(dt_str, fmt)
    except ValueError:
        return None


def get_time_ago(dt: datetime) -> str:
    """获取相对时间"""
    now = datetime.now()
    diff = now - dt

    if diff.days > 365:
        return f"{diff.days // 365}年前"
    elif diff.days > 30:
        return f"{diff.days // 30}个月前"
    elif diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}小时前"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}分钟前"
    else:
        return "刚刚"


def to_json(data: Any) -> str:
    """转换为JSON"""
    return json.dumps(data, default=str, ensure_ascii=False)


def from_json(json_str: str) -> Any:
    """从JSON解析"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def paginate(items: list, page: int = 1, page_size: int = 10) -> dict[str, Any]:
    """分页"""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return {"items": items[start:end], "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size - 1) // page_size}


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= length:
        return text
    return text[: length - len(suffix)] + suffix
