#!/usr/bin/env python
"""执行数据库迁移、创建管理员、启动服务和测试"""
import subprocess
import time
import sys
import os

def run_command(cmd, description, wait=True):
    """执行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"执行命令: {cmd}\n")

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"[✓] {description} 完成")
        return True
    else:
        print(f"[✗] {description} 失败 (返回码: {result.returncode})")
        return False

def main():
    os.chdir("e:/GitHub/Hello-Django-Ninja-Api")

    print("\n" + "="*60)
    print("开始执行项目部署流程")
    print("="*60)

    # 步骤1: 创建迁移文件
    success = run_command(
        "python manage.py makemigrations",
        "步骤1: 创建迁移文件"
    )

    # 步骤2: 应用迁移
    success = run_command(
        "python manage.py migrate --run-syncdb",
        "步骤2: 应用迁移",
        wait=True
    ) and success

    # 步骤3: 创建管理员
    success = run_command(
        "python scripts/init_admin.py",
        "步骤3: 创建管理员用户"
    ) and success

    # 步骤4: 启动服务(后台运行)
    print("\n" + "="*60)
    print("步骤4: 启动Django服务")
    print("="*60)

    # 使用start命令在后台启动服务
    subprocess.Popen(
        ["python", "manage.py", "runserver", "8000"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("[✓] 服务正在启动...")
    print("等待服务就绪...")
    time.sleep(5)  # 等待服务启动

    # 检查服务是否启动
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/api/health", timeout=5)
        if response.status_code == 200:
            print(f"[✓] 服务启动成功,健康检查通过")
        else:
            print(f"[!] 服务已启动,但健康检查返回: {response.status_code}")
    except Exception as e:
        print(f"[!] 服务启动检查失败: {e}")

    # 步骤5: 测试API
    api_test_success = run_command(
        "python test_api.py",
        "步骤5: API功能测试"
    )

    # 步骤6: 运行单元测试
    test_success = run_command(
        "pytest tests/ -v",
        "步骤6: 单元测试"
    )

    print("\n" + "="*60)
    print("执行完成!")
    print("="*60)
    print("\n服务信息:")
    print("- 服务地址: http://127.0.0.1:8000")
    print("- API文档: http://127.0.0.1:8000/api/docs")
    print("- 交互文档: http://127.0.0.1:8000/api")
    print("\n提示: 服务在单独的窗口中运行,请手动关闭该窗口以停止服务")

if __name__ == "__main__":
    main()
