# 信息收集工具 v2.0

一款现代化的信息收集工具，提供命令行和Web界面两种使用方式，集成了多种信息收集功能，适用于网络安全测试和渗透测试。

## 🌟 主要特性

### 🖥️ 双界面支持
- **Web界面**: 现代化的图形界面，直观易用
- **命令行界面**: 适合自动化和批量处理

### 🔍 基础信息收集
- **Whois信息查询**: 获取域名注册信息、注册商、注册时间等
- **CDN识别**: 检测目标是否使用CDN服务，支持主流CDN识别
- **ICP备案查询**: 查询域名备案信息
- **DNS解析**: 获取域名的DNS解析记录

### 🌐 子域名爆破
- **子域名枚举**: 基于字典的子域名爆破
- **IP解析**: 获取子域名对应的IP地址
- **IP归属地查询**: 查询IP地址的地理位置信息
- **Web指纹识别**: 识别Web服务器和框架类型

### 📁 目录扫描
- **敏感目录扫描**: 扫描常见的管理后台、配置目录等
- **敏感文件扫描**: 检测配置文件、备份文件等敏感文件
- **状态码检测**: 识别不同HTTP状态码的响应
- **网页标题提取**: 提取网页标题信息

### 🔗 API接口集成
- **FOFA搜索**: 集成FOFA网络空间搜索引擎
- **Quake搜索**: 集成360 Quake网络空间搜索引擎
- **批量查询**: 支持批量搜索和结果导出

## 🚀 快速开始

### 环境要求
- Python 3.6+
- Windows/Linux/MacOS

### 方式一：一键启动（推荐）

#### Windows用户
```bash
# 双击运行 start.bat 文件
start.bat
```

#### 所有平台
```bash
# 使用Python启动脚本
python run.py
```

### 方式二：手动安装
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动Web界面
python app.py

# 3. 访问Web界面
# 打开浏览器访问: http://localhost:5000
```

## 📱 使用说明

### Web界面使用

1. **启动应用**
   ```bash
   python run.py
   # 或者双击 start.bat (Windows)
   ```

2. **访问界面**
   - 自动打开浏览器，或手动访问 `http://localhost:5000`

3. **功能模块**
   - **首页**: 工具概览和快速入口
   - **基础信息收集**: Whois、CDN、ICP备案查询
   - **子域名爆破**: 发现子域名和指纹识别
   - **目录扫描**: 敏感目录和文件发现
   - **FOFA搜索**: 网络空间资产搜索
   - **Quake搜索**: 360网络空间搜索
   - **综合扫描**: 一键执行所有扫描功能
   - **扫描结果**: 查看和管理扫描历史

### 命令行界面使用

```bash
# 完整扫描（使用内置字典）
python info_collector.py -t example.com

# 使用大字典进行扫描
python info_collector.py -t example.com --dict large

# 使用自定义字典
python info_collector.py -t example.com --dict-path my_dict.txt

# 仅进行基础信息收集
python info_collector.py -t example.com --no-subdomain --no-directory

# 自定义参数扫描
python info_collector.py -t example.com --threads 100 -o results.json --dict large
```

### 参数说明
- `-t, --target`: 目标域名（必须）
- `--no-subdomain`: 禁用子域名爆破
- `--no-directory`: 禁用目录扫描  
- `--no-fofa`: 禁用FOFA搜索
- `--no-quake`: 禁用Quake搜索
- `-o, --output`: 指定输出文件名
- `--threads`: 设置线程数（默认50）
- `--dict`: 子域名字典类型，可选值：builtin（内置）、large（大字典）
- `--dict-path`: 自定义字典文件路径

## ⚙️ 配置说明

### API配置
工具内置了以下API配置：
- **FOFA**: 
  - 邮箱: xxx@.com
  - API Key: xxxxxxxx
- **Quake**: 
  - API Key: xxxxxxxxx

如需修改API配置，请编辑 `info_collector.py` 文件中的相应部分。

### 字典配置
- **子域名字典**: 
  - 内置字典：约70个常用子域名，适合快速扫描
  - 大字典：9.5万个子域名（subnames-9.5w.txt），更全面但耗时较长
  - 自定义字典：支持指定自定义字典文件
- **目录字典**: 内置敏感目录和文件列表，可在源码中扩展

## 📊 输出结果

### Web界面
- 实时显示扫描进度
- 分类展示扫描结果
- 支持结果导出和下载
- 提供历史记录管理

### 命令行界面
扫描结果将保存为JSON格式，包含：
- 基础信息（Whois、CDN、ICP备案）
- 发现的子域名及其IP地址
- 检测到的目录和文件
- FOFA和Quake搜索结果

## 🛠️ 技术架构

### 后端技术栈
- **Python 3.6+**: 核心开发语言
- **Flask**: Web框架
- **dnspython**: DNS解析
- **requests**: HTTP请求处理
- **python-whois**: Whois查询

### 前端技术栈
- **Bootstrap 5**: UI框架
- **jQuery**: JavaScript库
- **Font Awesome**: 图标库
- **Chart.js**: 图表展示（可扩展）

### 核心功能模块
```
├── app.py              # Flask Web应用主程序
├── info_collector.py   # 核心扫描功能模块
├── run.py             # 启动脚本
├── start.bat          # Windows批处理启动脚本
├── requirements.txt   # Python依赖配置
├── templates/         # HTML模板文件
├── static/           # 静态资源文件
│   ├── css/         # 样式文件
│   └── js/          # JavaScript文件
└── downloads/        # 结果下载目录
```

## 📷 界面截图

### 主界面
- 现代化的响应式设计
- 清晰的功能分类
- 实时扫描进度显示

### 功能特色
- 🎨 美观的用户界面
- 📱 响应式设计，支持移动设备
- 🌙 深色/浅色主题切换
- 📊 实时扫描进度和统计
- 💾 结果导出和历史管理
- 🔍 高级搜索和过滤功能

## 🐛 故障排除

### 常见问题

1. **端口占用问题**
   ```bash
   # 修改端口号（在app.py中）
   app.run(host='0.0.0.0', port=5001)
   ```

2. **依赖安装失败**
   ```bash
   # 使用镜像源安装
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

3. **API调用失败**
   - 检查网络连接
   - 确认API密钥是否有效
   - 注意API调用频率限制

### 运行环境检查
```bash
# 检查Python版本
python --version

# 检查依赖安装
python run.py --check

# 安装/更新依赖
python run.py --install
```

## ⚠️ 免责声明与使用条款

### 免责声明
- 本工具仅供网络安全测试和学习使用
- 请在授权范围内使用，不得用于非法用途
- 使用者应遵守相关法律法规
- 作者不承担任何使用本工具造成的法律责任

### 使用建议
- 建议在测试环境或已获得授权的目标上使用
- 合理设置线程数，避免对目标服务器造成压力
- 定期更新字典文件以提高扫描效果
- 注意API调用频率限制

### 法律合规
在任何情况下进行网络安全测试之前，请确保您有明确的书面授权。未经授权的网络扫描和渗透测试可能违反法律。

## 📝 更新日志

### v2.0 (2024-01-01)
- 🎉 新增Web图形界面
- 🔧 重构核心扫描引擎
- 📊 添加实时进度显示
- 💾 增强结果导出功能
- 🎨 现代化UI设计
- 📱 响应式移动端支持
- 🌙 深色主题支持
- 📈 扫描统计和可视化

### v1.0 (2023-12-01)
- 初始版本发布
- 实现基础信息收集功能
- 实现子域名爆破功能
- 实现目录扫描功能
- 集成FOFA和Quake API
- 支持多线程扫描
- 支持结果导出

## 🤝 贡献指南

欢迎提交问题和改进建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 技术支持

如有问题或建议，请通过以下方式联系：
- 项目地址: [GitHub Repository]
- 技术支持: support@example.com
- 意见反馈: feedback@example.com

## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

---

**Made with ❤️ for Security Researchers**

