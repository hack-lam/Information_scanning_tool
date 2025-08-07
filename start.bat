@echo off
chcp 65001 >nul
title 信息收集工具 v2.0 - 启动器

echo.
echo ================================================================
echo                     信息收集工具 v2.0
echo                   基于Python + Flask开发
echo ================================================================
echo.

echo 🔍 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python环境
    echo 请先安装Python 3.6或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

echo.
echo 📦 正在检查依赖包...
python -c "import flask, requests, dns.resolver, whois" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  检测到缺少依赖包，正在自动安装...
    echo.
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖包安装失败
        echo 请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装完成
) else (
    echo ✅ 依赖包检查通过
)

echo.
echo 🚀 正在启动信息收集工具...
echo.
echo ================================================================
echo  应用信息:
echo    - 访问地址: http://localhost:5000
echo    - 停止服务: 按 Ctrl+C
echo ================================================================
echo.
echo ⚠️  免责声明: 本工具仅供网络安全测试和学习使用
echo              请在授权范围内使用，不得用于非法用途
echo.

python run.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 应用启动失败
    echo.
    echo 🔧 故障排除建议:
    echo    1. 检查端口5000是否被占用
    echo    2. 确认防火墙设置
    echo    3. 重新安装依赖: pip install -r requirements.txt
    echo    4. 检查Python版本是否兼容
    echo.
)

pause
