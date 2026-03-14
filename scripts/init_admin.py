"""
初始化脚本 - 创建初始管理员账号
使用 Django shell 执行，避免导入链问题
"""
import os
import subprocess
import sys


def run_command(cmd, check=True):
    """运行命令并返回结果"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    return result


def main():
    """主函数"""
    # 获取环境变量或使用默认值
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')

    project_root = os.path.dirname(os.path.dirname(__file__))
    python_exe = sys.executable
    manage_py = os.path.join(project_root, 'manage.py')

    # 1. 先运行迁移
    print("=" * 60)
    print("Step 1: Running database migrations...")
    print("=" * 60)
    try:
        run_command([python_exe, manage_py, 'migrate', '--noinput'])
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Migration failed: {e}")
        return

    # 2. 创建管理员账号
    print("\n" + "=" * 60)
    print("Step 2: Creating initial admin account...")
    print("=" * 60)

    # 使用 Django shell 执行
    script = f'''
from src.infrastructure.persistence.models.user_models import User

username = "{username}"
email = "{email}"
password = "{password}"

# 检查用户是否已存在
if User.objects.filter(username=username).exists():
    print(f"WARNING: User '{{username}}' already exists, skipping creation")
else:
    # 创建超级用户
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"SUCCESS: Initial admin account created successfully!")
    print(f"  Username: {{username}}")
    print(f"  Email: {{email}}")
    print(f"  Password: {{password}}")
    print(f"\\nWARNING: Please change the default password in production environment!")
'''

    # 执行 Django shell
    try:
        run_command([python_exe, manage_py, 'shell', '-c', script])
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create admin account: {e}")
        return

    print("\n" + "=" * 60)
    print("Initialization completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
