"""
集成测试脚本
使用 requests 库对每个接口进行真实测试
"""

import json
import time
import requests
from typing import Optional

# 配置
BASE_URL = "http://127.0.0.1:8000/api"
TIMEOUT = 10

# 测试结果
test_results = []


def log_test(name: str, success: bool, message: str = ""):
    """记录测试结果"""
    status = "✓ PASS" if success else "✗ FAIL"
    result = f"{status} - {name}"
    if message:
        result += f" | {message}"
    print(result)
    test_results.append({"name": name, "success": success, "message": message})


def make_request(
    method: str,
    endpoint: str,
    data: dict = None,
    token: str = None,
    expect_status: int = 200,
) -> tuple[bool, dict | None]:
    """发送HTTP请求"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=TIMEOUT)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=TIMEOUT)
        else:
            return False, None

        if response.status_code == expect_status:
            try:
                return True, response.json()
            except:
                return True, {}
        else:
            return False, {"status": response.status_code, "body": response.text[:200]}
    except Exception as e:
        return False, {"error": str(e)}


class IntegrationTest:
    """集成测试类"""

    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.role_id: Optional[str] = None

    def run_all(self):
        """运行所有测试"""
        print("=" * 60)
        print("开始集成测试")
        print("=" * 60)

        # 1. 健康检查
        self.test_health_check()

        # 2. 认证测试
        self.test_auth_flow()

        # 3. 用户管理测试
        self.test_user_flow()

        # 4. RBAC测试
        self.test_rbac_flow()

        # 5. 安全管理测试
        self.test_security_flow()

        # 6. 系统管理测试
        self.test_system_flow()

        # 打印结果
        self.print_results()

    def test_health_check(self):
        """测试健康检查"""
        print("\n--- 健康检查 ---")
        success, data = make_request("GET", "/health")
        log_test("健康检查", success, str(data) if not success else "")

    def test_auth_flow(self):
        """测试认证流程"""
        print("\n--- 认证测试 ---")

        # 1. 注册用户
        user_data = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "TestPass123!",
            "phone": "13800138000",
        }
        success, data = make_request("POST", "/v1/users", user_data)
        if success and data:
            self.user_id = data.get("user_id")
        log_test("注册用户", success, f"user_id: {self.user_id}")

        # 2. 登录
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        success, data = make_request("POST", "/v1/auth/login", login_data)
        if success and data:
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
        log_test("用户登录", success, "token获取成功" if self.access_token else "token获取失败")

        # 3. 刷新Token
        if self.refresh_token:
            success, data = make_request(
                "POST", "/v1/auth/refresh", {"refresh_token": self.refresh_token}
            )
            log_test("刷新Token", success)

        # 4. 登出
        if self.access_token:
            success, _ = make_request("POST", "/v1/auth/logout", token=self.access_token)
            log_test("用户登出", success)

            # 重新登录获取token
            success, data = make_request("POST", "/v1/auth/login", login_data)
            if success and data:
                self.access_token = data.get("access_token")

    def test_user_flow(self):
        """测试用户管理"""
        print("\n--- 用户管理测试 ---")

        # 1. 获取用户列表
        success, data = make_request("GET", "/v1/users")
        log_test("获取用户列表", success)

        # 2. 获取当前用户信息
        if self.access_token:
            success, data = make_request("GET", "/v1/me", token=self.access_token)
            log_test("获取当前用户", success)

    def test_rbac_flow(self):
        """测试RBAC"""
        print("\n--- RBAC测试 ---")

        # 1. 创建角色
        role_data = {
            "name": f"测试角色_{int(time.time())}",
            "code": f"test_role_{int(time.time())}",
            "description": "测试角色描述",
        }
        success, data = make_request("POST", "/v1/rbac/roles", role_data)
        if success and data:
            self.role_id = data.get("role_id")
        log_test("创建角色", success, f"role_id: {self.role_id}")

        # 2. 获取角色列表
        success, data = make_request("GET", "/v1/rbac/roles")
        log_test("获取角色列表", success)

        # 3. 获取权限列表
        success, data = make_request("GET", "/v1/rbac/permissions")
        log_test("获取权限列表", success)

        # 4. 初始化系统权限
        success, data = make_request("POST", "/v1/rbac/permissions/init")
        log_test("初始化系统权限", success)

    def test_security_flow(self):
        """测试安全管理"""
        print("\n--- 安全管理测试 ---")

        # 1. 获取黑名单列表
        success, data = make_request("GET", "/v1/security/blacklist")
        log_test("获取黑名单列表", success)

        # 2. 获取白名单列表
        success, data = make_request("GET", "/v1/security/whitelist")
        log_test("获取白名单列表", success)

        # 3. 获取限流规则列表
        success, data = make_request("GET", "/v1/security/rate-limit")
        log_test("获取限流规则列表", success)

        # 4. 获取安全状态
        success, data = make_request("GET", "/v1/security/status")
        log_test("获取安全状态", success)

    def test_system_flow(self):
        """测试系统管理"""
        print("\n--- 系统管理测试 ---")

        # 1. 健康检查
        success, data = make_request("GET", "/v1/system/health")
        log_test("系统健康检查", success)

        # 2. 获取部门列表
        success, data = make_request("GET", "/v1/system/depts")
        log_test("获取部门列表", success)

        # 3. 获取菜单列表
        success, data = make_request("GET", "/v1/system/menus")
        log_test("获取菜单列表", success)

        # 4. 获取角色列表
        success, data = make_request("GET", "/v1/system/roles")
        log_test("获取系统角色列表", success)

        # 5. 获取操作日志列表
        success, data = make_request("GET", "/v1/system/operation-logs")
        log_test("获取操作日志列表", success)

    def print_results(self):
        """打印测试结果"""
        output = []
        output.append("\n" + "=" * 60)
        output.append("测试结果汇总")
        output.append("=" * 60)

        passed = sum(1 for r in test_results if r["success"])
        failed = len(test_results) - passed

        output.append(f"总计: {len(test_results)} 个测试")
        output.append(f"通过: {passed} 个")
        output.append(f"失败: {failed} 个")

        if failed > 0:
            output.append("\n失败的测试:")
            for r in test_results:
                if not r["success"]:
                    output.append(f"  - {r['name']}: {r['message']}")

        output.append("=" * 60)
        result_str = "\n".join(output)
        print(result_str)

        # 同时写入文件
        with open("integration_test_results.txt", "w", encoding="utf-8") as f:
            f.write(result_str)


if __name__ == "__main__":
    test = IntegrationTest()
    test.run_all()
