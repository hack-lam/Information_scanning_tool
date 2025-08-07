#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息收集工具启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 6):
        print("❌ 错误: 需要Python 3.6或更高版本")
        print(f"当前版本: Python {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python版本检查通过: {sys.version.split()[0]}")

def check_dependencies():
    """检查并安装依赖"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ 错误: requirements.txt文件不存在")
        sys.exit(1)
    
    print("📦 检查依赖包...")
    
    try:
        # 尝试导入主要依赖
        import flask
        import requests
        import dns.resolver
        import whois
        print("✅ 主要依赖包已安装")
        return True
    except ImportError as e:
        print(f"⚠️  缺少依赖包: {e}")
        print("正在安装依赖包...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✅ 依赖包安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖包安装失败")
            print("请手动运行: pip install -r requirements.txt")
            return False

def create_directories():
    """创建必要的目录"""
    directories = [
        "downloads",
        "logs",
        "static/css",
        "static/js",
        "static/img",
        "templates"
    ]
    
    base_path = Path(__file__).parent
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构检查完成")

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "app.py",
        "info_collector.py", 
        "templates/base.html",
        "templates/index.html",
        "static/css/style.css",
        "static/js/main.js"
    ]
    
    base_path = Path(__file__).parent
    missing_files = []
    
    for file_path in required_files:
        if not (base_path / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ 必要文件检查完成")
    return True

def start_application():
    """启动应用"""
    print("\n" + "="*60)
    print("🚀 启动信息收集工具...")
    print("="*60)
    
    # 设置环境变量
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'production'
    
    try:
        # 导入并启动Flask应用
        from app import app
        
        print("✅ 应用初始化成功")
        print("\n📋 应用信息:")
        print(f"   - 应用名称: 信息收集工具 v2.0")
        print(f"   - 访问地址: http://localhost:5000")
        print(f"   - 管理界面: http://localhost:5000/admin (开发中)")
        print(f"   - API文档: http://localhost:5000/api/docs (开发中)")
        
        print("\n🔧 功能模块:")
        print(f"   - 基础信息收集: ✅")
        print(f"   - 子域名爆破: ✅") 
        print(f"   - 目录扫描: ✅")
        print(f"   - FOFA搜索: ✅")
        print(f"   - Quake搜索: ✅")
        print(f"   - 综合扫描: ✅")
        
        print("\n⚠️  免责声明:")
        print(f"   本工具仅供网络安全测试和学习使用")
        print(f"   请在授权范围内使用，不得用于非法用途")
        
        print("\n" + "="*60)
        print("🌐 正在启动Web服务器...")
        print("="*60)
        
        # 延迟3秒后自动打开浏览器
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:5000')
                print("🌍 已在默认浏览器中打开应用")
            except:
                print("ℹ️  请手动在浏览器中访问: http://localhost:5000")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 启动Flask应用
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断，正在关闭服务器...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")
        print("\n🔧 故障排除建议:")
        print("   1. 检查端口5000是否被占用")
        print("   2. 确认防火墙设置")
        print("   3. 重新安装依赖: pip install -r requirements.txt")
        print("   4. 检查Python版本是否兼容")
        sys.exit(1)

def show_help():
    """显示帮助信息"""
    help_text = """
信息收集工具 v2.0 - 启动脚本

用法:
    python run.py [选项]

选项:
    -h, --help      显示此帮助信息
    --check         仅检查环境，不启动应用
    --install       安装/更新依赖包
    --version       显示版本信息

示例:
    python run.py                # 启动应用
    python run.py --check        # 检查环境
    python run.py --install      # 安装依赖

更多信息请访问: https://github.com/yourname/info-collector
    """
    print(help_text)

def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg in ['-h', '--help']:
            show_help()
            return
        elif arg == '--check':
            print("🔍 环境检查模式\n")
            check_python_version()
            check_dependencies()
            create_directories()
            check_files()
            print("\n✅ 环境检查完成")
            return
        elif arg == '--install':
            print("📦 依赖安装模式\n")
            check_dependencies()
            print("\n✅ 依赖安装完成")
            return
        elif arg == '--version':
            print("信息收集工具 v2.0")
            print("基于Python + Flask开发")
            return
        else:
            print(f"❌ 未知参数: {arg}")
            print("使用 --help 查看帮助信息")
            return
    
    # 标准启动流程
    print("🔍 信息收集工具 v2.0 - 启动检查")
    print("="*50)
    
    # 环境检查
    check_python_version()
    
    if not check_dependencies():
        sys.exit(1)
    
    create_directories()
    
    if not check_files():
        sys.exit(1)
    
    # 启动应用
    start_application()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 程序异常: {str(e)}")
        sys.exit(1)
