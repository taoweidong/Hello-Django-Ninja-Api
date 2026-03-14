"""
代码检查和修复脚本
"""
import os
import subprocess
import sys
from pathlib import Path

# 设置 UTF-8 编码
if sys.platform == 'win32':
    os.system('chcp 65001')

def run_command(cmd, description):
    """运行命令"""
    print(f"\n{'='*60}")
    print(f"[Ruff] {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    """主函数"""
    base_dir = Path(__file__).parent.parent

    print("[Start] 开始代码检查和修复...")

    # 1. Ruff 格式化
    run_command(
        f"cd {base_dir} && .venv\\Scripts\\python.exe -m ruff format src/ tests/ config/",
        "Ruff 代码格式化"
    )

    # 2. Ruff 代码检查和修复
    run_command(
        f"cd {base_dir} && .venv\\Scripts\\python.exe -m ruff check src/ tests/ config/ --fix",
        "Ruff 代码检查和自动修复"
    )

    # 3. Ruff 检查剩余问题
    result = run_command(
        f"cd {base_dir} && .venv\\Scripts\\python.exe -m ruff check src/ tests/ config/",
        "Ruff 代码检查（显示剩余问题）"
    )

    print(f"\n{'='*60}")
    if result:
        print("[Success] 所有代码检查通过！")
    else:
        print("[Warning] 仍有代码问题需要手动修复")
    print(f"{'='*60}")

    # 4. MyPy 类型检查
    print(f"\n{'='*60}")
    print("[MyPy] 运行 MyPy 类型检查...")
    print(f"{'='*60}")
    run_command(
        f"cd {base_dir} && .venv\\Scripts\\python.exe -m mypy src/",
        "MyPy 类型检查"
    )

if __name__ == "__main__":
    main()
