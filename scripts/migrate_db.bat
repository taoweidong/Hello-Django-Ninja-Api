@echo off
chcp 65001 >nul
echo ============================================================
echo 数据库迁移脚本 - 将数据库移动到 sql 目录
echo ============================================================

echo.
echo 步骤 1: 停止运行的服务...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo 发现运行中的Python进程，尝试停止...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] 已停止Python进程
) else (
    echo [OK] 没有运行中的Python进程
)

echo.
echo 步骤 2: 移动数据库文件...
if exist db.sqlite3 (
    move db.sqlite3 sql\db.sqlite3 >nul 2>&1
    if exist sql\db.sqlite3 (
        echo [OK] 数据库已移动到 sql\db.sqlite3
    ) else (
        echo [错误] 无法移动数据库文件
        pause
        exit /b 1
    )
) else (
    echo [OK] 根目录没有数据库文件，将在 sql 目录创建新数据库
)

echo.
echo 步骤 3: 创建迁移文件...
python manage.py makemigrations
if %ERRORLEVEL% EQU 0 (
    echo [OK] 迁移文件创建成功
) else (
    echo [警告] 创建迁移文件时出现问题，继续执行...
)

echo.
echo 步骤 4: 应用数据库迁移...
python manage.py migrate
if %ERRORLEVEL% EQU 0 (
    echo [OK] 数据库迁移成功
) else (
    echo [错误] 数据库迁移失败
    pause
    exit /b 1
)

echo.
echo 步骤 5: 创建超级管理员...
python scripts\init_admin.py
if %ERRORLEVEL% EQU 0 (
    echo [OK] 管理员创建成功
) else (
    echo [警告] 管理员创建脚本执行完成
)

echo.
echo 步骤 6: 清理临时文件...
if exist .coverage del /f /q .coverage >nul 2>&1
if exist htmlcov rmdir /s /q htmlcov >nul 2>&1
if exist .pytest_cache rmdir /s /q .pytest_cache >nul 2>&1
if exist .mypy_cache rmdir /s /q .mypy_cache >nul 2>&1
if exist .ruff_cache rmdir /s /q .ruff_cache >nul 2>&1
if exist test_api.py del /f /q test_api.py >nul 2>&1
if exist check_db.py del /f /q check_db.py >nul 2>&1
echo [OK] 临时文件清理完成

echo.
echo ============================================================
echo [完成] 数据库迁移和初始化完成!
echo ============================================================
echo.
echo 数据库位置: sql\db.sqlite3
echo 管理后台: http://127.0.0.1:8000/admin/
echo API文档: http://127.0.0.1:8000/api/docs
echo.
echo 启动服务: python manage.py runserver
echo.
pause
