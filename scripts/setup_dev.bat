@echo off
REM Windows 开发环境初始化脚本

echo 🚀 开始设置开发环境...

REM 检查 UV 是否安装
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo 📦 安装 UV...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
)

REM 创建虚拟环境
echo 🐍 创建 Python 虚拟环境 (3.10.11)...
uv venv --python 3.10.11

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 安装依赖
echo 📚 安装项目依赖...
uv pip install -e ".[dev]"

REM 代码格式化
echo ✨ 代码格式化 (Ruff)...
ruff format .

REM 代码检查
echo 🔍 代码检查 (Ruff)...
ruff check . --fix

REM 类型检查
echo 📊 类型检查 (MyPy)...
mypy src/

REM 创建初始管理员账号（包含数据库迁移）
echo 👤 创建初始管理员账号...
python scripts\init_admin.py

REM 运行测试
echo 🧪 运行测试...
pytest

echo ✅ 开发环境设置完成！
echo 🎯 启动服务: python manage.py runserver

pause
