"""
速率限制中间件测试
"""

from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from src.core.middlewares import RateLimitMiddleware


@pytest.fixture
def request_factory():
    """请求工厂 fixture"""
    return RequestFactory()


@pytest.fixture
def rate_limit_middleware():
    """速率限制中间件 fixture"""
    mock_cache = Mock()
    get_response = Mock()
    middleware = RateLimitMiddleware(get_response)
    middleware.cache = mock_cache
    return middleware


@pytest.mark.unit
class TestRateLimitMiddleware:
    """速率限制中间件测试"""

    def test_request_within_limit(self, request_factory, rate_limit_middleware):
        """测试请求在限制内"""
        mock_cache = Mock()
        mock_cache.get.return_value = 5  # 5次请求，未超过100次
        rate_limit_middleware.cache = mock_cache

        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        response = rate_limit_middleware(request)

        assert response is not None

    def test_request_exceeds_limit(self, request_factory, rate_limit_middleware):
        """测试请求超过限制"""
        mock_cache = Mock()
        mock_cache.get.return_value = 101  # 超过100次限制
        rate_limit_middleware.cache = mock_cache

        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        response = rate_limit_middleware(request)

        assert response.status_code == 429
        assert "rate limit exceeded" in response.content.decode().lower()

    def test_whitelisted_ip(self, request_factory, rate_limit_middleware):
        """测试白名单 IP"""
        mock_cache = Mock()
        rate_limit_middleware.cache = mock_cache

        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "192.168.1.1"

        # 模拟白名单检查
        mock_cache.get.return_value = True
        rate_limit_middleware.is_whitelisted = lambda ip: mock_cache.get(f"whitelist:{ip}")

        response = rate_limit_middleware(request)

        assert response is not None
        mock_cache.get.assert_called()
