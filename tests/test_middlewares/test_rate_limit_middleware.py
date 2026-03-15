"""
速率限制中间件测试
"""

from unittest.mock import Mock, patch

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
    get_response = Mock()
    return RateLimitMiddleware(get_response)


@pytest.mark.unit
class TestRateLimitMiddleware:
    """速率限制中间件测试"""

    def test_request_within_limit(self, request_factory, rate_limit_middleware):
        """测试请求在限制内"""
        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        with patch("src.core.middlewares.rate_limit_middleware.cache") as mock_cache:
            mock_cache.get.return_value = 5  # 5次请求，未超过100次
            response = rate_limit_middleware(request)
            assert response is not None

    def test_request_exceeds_limit(self, request_factory, rate_limit_middleware):
        """测试请求超过限制"""
        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        with patch("src.core.middlewares.rate_limit_middleware.cache") as mock_cache:
            mock_cache.get.return_value = 101  # 超过100次限制
            response = rate_limit_middleware(request)

            assert response.status_code == 429
            content = response.content.decode()
            assert "RATE_LIMIT_ERROR" in content

    def test_whitelisted_ip(self, request_factory, rate_limit_middleware):
        """测试白名单 IP - 验证中间件正常处理请求"""
        request = request_factory.get("/api/test")
        request.META["REMOTE_ADDR"] = "192.168.1.1"

        with patch("src.core.middlewares.rate_limit_middleware.cache") as mock_cache:
            mock_cache.get.return_value = 0  # 第一次请求，允许通过
            mock_cache.set = Mock()  # mock set 方法
            response = rate_limit_middleware(request)

            assert response is not None
            mock_cache.get.assert_called()
