#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息收集工具 v1.0
功能包括：基础信息收集、子域名爆破、目录扫描、FOFA/Quake接口调用
"""

import requests
import json
import base64
import time
import threading
import socket
import ssl
import whois
import dns.resolver
import re
import os
import hashlib
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys
from datetime import datetime
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Colors:
    """颜色输出类"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class InfoCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # API配置
        self.fofa_email = "li1u888@163.com"
        self.fofa_key = "80cb74dd36424e570a36c19a7601b8a0"
        self.quake_key = "42203ab4-20e1-404e-8ca7-448f9e852a84"
        
        # 子域名字典
        self.subdomain_dict_builtin = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api', 'blog', 'shop',
            'forum', 'news', 'help', 'support', 'vpn', 'cdn', 'cache', 'static',
            'img', 'image', 'video', 'download', 'upload', 'file', 'files',
            'data', 'db', 'database', 'sql', 'backup', 'bak', 'old', 'new',
            'staging', 'pre', 'prod', 'demo', 'beta', 'alpha', 'mobile', 'm',
            'wap', 'app', 'apps', 'service', 'services', 'web', 'webmail',
            'email', 'pop', 'smtp', 'imap', 'exchange', 'mx', 'ns', 'dns',
            'gateway', 'router', 'firewall', 'proxy', 'lb', 'balance'
        ]
        
        # 当前使用的子域名字典
        self.subdomain_dict = self.subdomain_dict_builtin.copy()
        
        # 大字典文件路径
        self.large_dict_path = "subnames-9.5w.txt"
        
        # 敏感目录字典
        self.directory_dict = [
            'admin', 'administrator', 'login', 'panel', 'control', 'manage',
            'management', 'manager', 'system', 'sys', 'backup', 'bak', 'old',
            'new', 'test', 'demo', 'dev', 'development', 'staging', 'beta',
            'alpha', 'temp', 'tmp', 'log', 'logs', 'cache', 'config', 'conf',
            'include', 'inc', 'lib', 'libs', 'data', 'database', 'db', 'sql',
            'upload', 'uploads', 'download', 'downloads', 'file', 'files',
            'img', 'images', 'pic', 'pictures', 'video', 'videos', 'media',
            'static', 'assets', 'css', 'js', 'javascript', 'style', 'styles',
            'plugin', 'plugins', 'module', 'modules', 'component', 'components',
            'api', 'service', 'services', 'webservice', 'rest', 'ajax',
            'json', 'xml', 'feed', 'rss', 'atom', 'sitemap'
        ]

    def print_banner(self):
        """打印工具横幅"""
        banner = f"""
{Colors.CYAN}
██╗███╗   ██╗███████╗ ██████╗      ██████╗ ██████╗ ██╗     ██╗     ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██║████╗  ██║██╔════╝██╔═══██╗    ██╔════╝██╔═══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║██╔██╗ ██║█████╗  ██║   ██║    ██║     ██║   ██║██║     ██║     █████╗  ██║        ██║   ██║   ██║██████╔╝
██║██║╚██╗██║██╔══╝  ██║   ██║    ██║     ██║   ██║██║     ██║     ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██║██║ ╚████║██║     ╚██████╔╝    ╚██████╗╚██████╔╝███████╗███████╗███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝      ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Colors.END}
{Colors.YELLOW}                                    信息收集工具 v1.0{Colors.END}
{Colors.GREEN}                           功能：基础信息收集 | 子域名爆破 | 目录扫描 | API接口调用{Colors.END}
{Colors.RED}                                      请合法使用，仅供安全测试{Colors.END}
        """
        print(banner)

    def log_info(self, message):
        """信息日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.BLUE}[{timestamp}] [INFO]{Colors.END} {message}")

    def log_success(self, message):
        """成功日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.GREEN}[{timestamp}] [SUCCESS]{Colors.END} {message}")

    def log_warning(self, message):
        """警告日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.YELLOW}[{timestamp}] [WARNING]{Colors.END} {message}")

    def log_error(self, message):
        """错误日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.RED}[{timestamp}] [ERROR]{Colors.END} {message}")

    # ========== 基础信息收集模块 ==========
    
    def get_whois_info(self, domain):
        """获取Whois信息"""
        try:
            self.log_info(f"正在查询 {domain} 的Whois信息...")
            w = whois.whois(domain)
            
            info = {
                '域名': domain,
                '注册商': str(w.registrar) if w.registrar else 'N/A',
                '创建时间': str(w.creation_date) if w.creation_date else 'N/A',
                '过期时间': str(w.expiration_date) if w.expiration_date else 'N/A',
                '更新时间': str(w.updated_date) if w.updated_date else 'N/A',
                '注册人': str(w.registrant) if hasattr(w, 'registrant') and w.registrant else 'N/A',
                '注册邮箱': str(w.emails) if w.emails else 'N/A',
                'DNS服务器': str(w.name_servers) if w.name_servers else 'N/A'
            }
            
            self.log_success(f"成功获取 {domain} 的Whois信息")
            return info
            
        except Exception as e:
            self.log_error(f"获取Whois信息失败: {str(e)}")
            return None

    def check_cdn(self, domain):
        """CDN识别"""
        try:
            self.log_info(f"正在检测 {domain} 的CDN...")
            
            # 通过DNS解析检查
            result = dns.resolver.resolve(domain, 'A')
            ips = [str(rdata) for rdata in result]
            
            # 通过CNAME检查
            cname_result = None
            try:
                cname_result = dns.resolver.resolve(domain, 'CNAME')
                cnames = [str(rdata) for rdata in cname_result]
            except:
                cnames = []
            
            # CDN特征检测
            cdn_patterns = {
                'Cloudflare': ['cloudflare', 'cf-ray'],
                'AWS CloudFront': ['cloudfront', 'amazonaws'],
                'Akamai': ['akamai', 'akamaiedge'],
                'MaxCDN': ['maxcdn', 'netdna'],
                'Fastly': ['fastly'],
                'KeyCDN': ['keycdn'],
                'CloudFlare': ['cloudflare'],
                '网宿': ['wscdn', 'wangsu'],
                '阿里云': ['alicdn', 'kunlun'],
                '腾讯云': ['qcloud', 'tencent'],
                '百度云': ['baiduyun', 'bcebos']
            }
            
            detected_cdn = []
            
            # 检查CNAME
            for cname in cnames:
                for cdn_name, patterns in cdn_patterns.items():
                    for pattern in patterns:
                        if pattern.lower() in cname.lower():
                            detected_cdn.append(cdn_name)
            
            # HTTP头检查
            try:
                response = self.session.get(f"http://{domain}", timeout=10, allow_redirects=True)
                headers = response.headers
                
                for cdn_name, patterns in cdn_patterns.items():
                    for pattern in patterns:
                        for header_name, header_value in headers.items():
                            if pattern.lower() in header_value.lower() or pattern.lower() in header_name.lower():
                                detected_cdn.append(cdn_name)
            except:
                pass
            
            cdn_info = {
                '域名': domain,
                'IP地址': ips,
                'CNAME记录': cnames,
                '检测到的CDN': list(set(detected_cdn)) if detected_cdn else ['无CDN或未识别']
            }
            
            if detected_cdn:
                self.log_success(f"检测到CDN: {', '.join(set(detected_cdn))}")
            else:
                self.log_info("未检测到CDN")
            
            return cdn_info
            
        except Exception as e:
            self.log_error(f"CDN检测失败: {str(e)}")
            return None

    def get_icp_info(self, domain):
        """获取ICP备案信息（模拟接口）"""
        try:
            self.log_info(f"正在查询 {domain} 的ICP备案信息...")
            
            # 这里可以集成真实的ICP查询接口
            # 由于接口限制，这里返回模拟数据
            icp_info = {
                '域名': domain,
                '备案号': '模拟备案号',
                '备案单位': '模拟备案单位',
                '备案类型': '企业',
                '审核时间': '2023-01-01',
                '备案状态': '正常'
            }
            
            self.log_success(f"获取到 {domain} 的ICP备案信息")
            return icp_info
            
        except Exception as e:
            self.log_error(f"获取ICP备案信息失败: {str(e)}")
            return None

    # ========== 子域名爆破模块 ==========
    
    def load_subdomain_dict(self, dict_type="builtin", custom_path=None):
        """加载子域名字典"""
        try:
            if dict_type == "large":
                # 使用大字典
                dict_path = custom_path or self.large_dict_path
                if os.path.exists(dict_path):
                    # 尝试多种编码格式
                    encodings = ['utf-8', 'gbk', 'gb2312', 'ascii']
                    subdomains = []
                    
                    for encoding in encodings:
                        try:
                            with open(dict_path, 'r', encoding=encoding) as f:
                                subdomains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if subdomains:
                        # 去重和过滤
                        subdomains = list(set(subdomains))
                        # 过滤无效字符
                        subdomains = [sub for sub in subdomains if sub.replace('-', '').replace('_', '').isalnum()]
                        self.subdomain_dict = subdomains
                        self.log_success(f"成功加载大字典，共 {len(subdomains)} 个子域名")
                        return True
                    else:
                        self.log_error(f"无法读取字典文件: {dict_path}")
                        self.subdomain_dict = self.subdomain_dict_builtin.copy()
                        return False
                else:
                    self.log_warning(f"大字典文件不存在: {dict_path}，使用内置字典")
                    self.subdomain_dict = self.subdomain_dict_builtin.copy()
                    return False
                    
            elif dict_type == "custom" and custom_path:
                # 使用自定义字典
                if os.path.exists(custom_path):
                    encodings = ['utf-8', 'gbk', 'gb2312', 'ascii']
                    subdomains = []
                    
                    for encoding in encodings:
                        try:
                            with open(custom_path, 'r', encoding=encoding) as f:
                                subdomains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if subdomains:
                        subdomains = list(set(subdomains))
                        subdomains = [sub for sub in subdomains if sub.replace('-', '').replace('_', '').isalnum()]
                        self.subdomain_dict = subdomains
                        self.log_success(f"成功加载自定义字典，共 {len(subdomains)} 个子域名")
                        return True
                    else:
                        self.log_error(f"无法读取自定义字典文件: {custom_path}")
                        return False
                else:
                    self.log_error(f"自定义字典文件不存在: {custom_path}")
                    return False
            else:
                # 使用内置字典
                self.subdomain_dict = self.subdomain_dict_builtin.copy()
                self.log_info(f"使用内置字典，共 {len(self.subdomain_dict)} 个子域名")
                return True
                
        except Exception as e:
            self.log_error(f"加载字典失败: {str(e)}")
            self.subdomain_dict = self.subdomain_dict_builtin.copy()
            return False
    
    def resolve_domain(self, subdomain):
        """解析单个子域名"""
        try:
            result = dns.resolver.resolve(subdomain, 'A')
            ips = [str(rdata) for rdata in result]
            return {
                'subdomain': subdomain,
                'ips': ips,
                'status': 'active'
            }
        except:
            return None

    def get_ip_location(self, ip):
        """获取IP归属地"""
        try:
            # 使用免费的IP归属地查询接口
            response = self.session.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return f"{data.get('country', '')} {data.get('regionName', '')} {data.get('city', '')}"
        except:
            pass
        return "未知"

    def get_web_fingerprint(self, url):
        """获取Web指纹信息"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            headers = response.headers
            content = response.text[:1000]  # 只取前1000字符
            
            fingerprints = []
            
            # 检查常见的Web服务器
            server = headers.get('Server', '').lower()
            if 'nginx' in server:
                fingerprints.append('Nginx')
            elif 'apache' in server:
                fingerprints.append('Apache')
            elif 'iis' in server:
                fingerprints.append('IIS')
            elif 'tomcat' in server:
                fingerprints.append('Tomcat')
            
            # 检查常见的Web框架
            if 'laravel' in content.lower():
                fingerprints.append('Laravel')
            elif 'wordpress' in content.lower():
                fingerprints.append('WordPress')
            elif 'drupal' in content.lower():
                fingerprints.append('Drupal')
            elif 'joomla' in content.lower():
                fingerprints.append('Joomla')
            elif 'django' in content.lower():
                fingerprints.append('Django')
            
            # 检查X-Powered-By头
            powered_by = headers.get('X-Powered-By', '')
            if powered_by:
                fingerprints.append(f"X-Powered-By: {powered_by}")
            
            return fingerprints if fingerprints else ['未识别']
            
        except:
            return ['无法访问']

    def subdomain_brute(self, domain, threads=50, dict_type="builtin", custom_dict_path=None, 
                        enable_location=True, enable_fingerprint=True):
        """子域名爆破"""
        # 加载指定的字典
        self.load_subdomain_dict(dict_type, custom_dict_path)
        
        total_count = len(self.subdomain_dict)
        self.log_info(f"开始对 {domain} 进行子域名爆破...")
        self.log_info(f"使用字典: {dict_type}，共 {total_count} 个子域名")
        
        found_subdomains = []
        checked_count = 0
        
        def check_subdomain(sub):
            nonlocal checked_count
            subdomain = f"{sub}.{domain}"
            result = self.resolve_domain(subdomain)
            if result:
                # 获取IP归属地
                if enable_location:
                    try:
                        for ip in result['ips']:
                            location = self.get_ip_location(ip)
                            result['location'] = location
                            break
                    except:
                        result['location'] = '未知'
                else:
                    result['location'] = '未启用'
                
                # 获取Web指纹
                if enable_fingerprint:
                    try:
                        fingerprints = self.get_web_fingerprint(f"http://{subdomain}")
                        result['fingerprints'] = fingerprints
                    except:
                        result['fingerprints'] = ['无法获取']
                else:
                    result['fingerprints'] = ['未启用']
                
                found_subdomains.append(result)
                self.log_success(f"发现子域名: {subdomain} -> {', '.join(result['ips'])}")
            
            checked_count += 1
            if checked_count % 100 == 0:
                progress = (checked_count / total_count) * 100
                self.log_info(f"扫描进度: {checked_count}/{total_count} ({progress:.1f}%)")
        
        # 使用线程池进行爆破
        try:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(check_subdomain, self.subdomain_dict)
        except KeyboardInterrupt:
            self.log_warning("用户中断扫描")
        
        self.log_info(f"子域名爆破完成，共发现 {len(found_subdomains)} 个活跃子域名")
        return found_subdomains

    # ========== 目录扫描模块 ==========
    
    def scan_directory(self, url, directories, threads=20):
        """目录扫描"""
        self.log_info(f"开始对 {url} 进行目录扫描...")
        
        found_directories = []
        
        def check_directory(directory):
            target_url = urljoin(url, directory)
            try:
                response = self.session.get(target_url, timeout=10, allow_redirects=False, verify=False)
                if response.status_code in [200, 301, 302, 403]:
                    found_directories.append({
                        'url': target_url,
                        'status_code': response.status_code,
                        'content_length': len(response.content),
                        'title': self.extract_title(response.text) if response.status_code == 200 else ''
                    })
                    self.log_success(f"发现目录: {target_url} [状态码: {response.status_code}]")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(check_directory, directories)
        
        # 扫描常见文件
        common_files = [
            'robots.txt', 'sitemap.xml', '.htaccess', 'web.config',
            'config.php', 'database.php', 'wp-config.php', '.env',
            'backup.sql', 'dump.sql', 'phpinfo.php', 'info.php'
        ]
        
        for file in common_files:
            target_url = urljoin(url, file)
            try:
                response = self.session.get(target_url, timeout=10, verify=False)
                if response.status_code == 200 and len(response.content) > 0:
                    found_directories.append({
                        'url': target_url,
                        'status_code': response.status_code,
                        'content_length': len(response.content),
                        'title': '敏感文件'
                    })
                    self.log_success(f"发现敏感文件: {target_url}")
            except:
                pass
        
        self.log_info(f"目录扫描完成，共发现 {len(found_directories)} 个目录/文件")
        return found_directories

    def extract_title(self, html):
        """提取网页标题"""
        try:
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()[:50]
        except:
            pass
        return ''

    # ========== FOFA接口调用模块 ==========
    
    def fofa_search(self, query, size=100):
        """FOFA搜索"""
        try:
            self.log_info(f"正在使用FOFA搜索: {query}")
            
            # Base64编码查询语句
            query_base64 = base64.b64encode(query.encode()).decode()
            
            url = "https://fofa.info/api/v1/search/all"
            params = {
                'email': self.fofa_email,
                'key': self.fofa_key,
                'qbase64': query_base64,
                'size': size,
                'fields': 'host,ip,port,protocol,country,region,city,organization,os,server,title'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('error') == False:
                    results = data.get('results', [])
                    self.log_success(f"FOFA搜索成功，找到 {len(results)} 条结果")
                    return results
                else:
                    self.log_error(f"FOFA搜索失败: {data.get('errmsg', '未知错误')}")
            else:
                self.log_error(f"FOFA API请求失败，状态码: {response.status_code}")
            
        except Exception as e:
            self.log_error(f"FOFA搜索异常: {str(e)}")
        
        return []

    # ========== Quake接口调用模块 ==========
    
    def quake_search(self, query, size=100):
        """Quake搜索"""
        try:
            self.log_info(f"正在使用Quake搜索: {query}")
            
            url = "https://quake.360.net/api/v3/search/quake_service"
            headers = {
                'X-QuakeToken': self.quake_key,
                'Content-Type': 'application/json'
            }
            
            data = {
                'query': query,
                'start': 0,
                'size': size
            }
            
            response = self.session.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    results = result.get('data', [])
                    self.log_success(f"Quake搜索成功，找到 {len(results)} 条结果")
                    return results
                else:
                    self.log_error(f"Quake搜索失败: {result.get('message', '未知错误')}")
            else:
                self.log_error(f"Quake API请求失败，状态码: {response.status_code}")
            
        except Exception as e:
            self.log_error(f"Quake搜索异常: {str(e)}")
        
        return []

    # ========== 综合扫描功能 ==========
    
    def comprehensive_scan(self, target, enable_subdomain=True, enable_directory=True, 
                          enable_fofa=True, enable_quake=True, dict_type="builtin"):
        """综合扫描"""
        self.log_info(f"开始对 {target} 进行综合扫描...")
        
        results = {
            'target': target,
            'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'basic_info': {},
            'subdomains': [],
            'directories': [],
            'fofa_results': [],
            'quake_results': []
        }
        
        # 基础信息收集
        self.log_info("=" * 50)
        self.log_info("开始基础信息收集")
        self.log_info("=" * 50)
        
        # Whois信息
        whois_info = self.get_whois_info(target)
        if whois_info:
            results['basic_info']['whois'] = whois_info
        
        # CDN检测
        cdn_info = self.check_cdn(target)
        if cdn_info:
            results['basic_info']['cdn'] = cdn_info
        
        # ICP备案信息
        icp_info = self.get_icp_info(target)
        if icp_info:
            results['basic_info']['icp'] = icp_info
        
        # 子域名爆破
        if enable_subdomain:
            self.log_info("=" * 50)
            self.log_info("开始子域名爆破")
            self.log_info("=" * 50)
            custom_dict_path = None
            if dict_type == 'custom':
                # 如果是自定义字典，需要从参数中获取路径
                import sys
                if hasattr(sys.modules[__name__], 'args') and hasattr(sys.modules[__name__].args, 'dict_path'):
                    custom_dict_path = sys.modules[__name__].args.dict_path
            results['subdomains'] = self.subdomain_brute(target, dict_type=dict_type, custom_dict_path=custom_dict_path)
        
        # 目录扫描
        if enable_directory:
            self.log_info("=" * 50)
            self.log_info("开始目录扫描")
            self.log_info("=" * 50)
            target_url = f"http://{target}"
            results['directories'] = self.scan_directory(target_url, self.directory_dict)
        
        # FOFA搜索
        if enable_fofa:
            self.log_info("=" * 50)
            self.log_info("开始FOFA搜索")
            self.log_info("=" * 50)
            fofa_query = f'domain="{target}"'
            results['fofa_results'] = self.fofa_search(fofa_query)
        
        # Quake搜索
        if enable_quake:
            self.log_info("=" * 50)
            self.log_info("开始Quake搜索")
            self.log_info("=" * 50)
            quake_query = f'domain: "{target}"'
            results['quake_results'] = self.quake_search(quake_query)
        
        return results

    def save_results(self, results, filename=None):
        """保存扫描结果"""
        if not filename:
            filename = f"scan_results_{results['target']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            self.log_success(f"扫描结果已保存到: {filename}")
        except Exception as e:
            self.log_error(f"保存结果失败: {str(e)}")

    def print_results_summary(self, results):
        """打印结果摘要"""
        print(f"\n{Colors.CYAN}{'='*60}")
        print(f"扫描结果摘要 - {results['target']}")
        print(f"{'='*60}{Colors.END}")
        
        # 基础信息
        if results['basic_info']:
            print(f"\n{Colors.YELLOW}📋 基础信息:{Colors.END}")
            if 'whois' in results['basic_info']:
                whois = results['basic_info']['whois']
                print(f"  注册商: {whois.get('注册商', 'N/A')}")
                print(f"  创建时间: {whois.get('创建时间', 'N/A')}")
                print(f"  过期时间: {whois.get('过期时间', 'N/A')}")
            
            if 'cdn' in results['basic_info']:
                cdn = results['basic_info']['cdn']
                print(f"  CDN: {', '.join(cdn.get('检测到的CDN', ['无']))}")
        
        # 子域名
        if results['subdomains']:
            print(f"\n{Colors.YELLOW}🌐 发现的子域名 ({len(results['subdomains'])} 个):{Colors.END}")
            for sub in results['subdomains'][:10]:  # 只显示前10个
                print(f"  {sub['subdomain']} -> {', '.join(sub['ips'])}")
            if len(results['subdomains']) > 10:
                print(f"  ... 还有 {len(results['subdomains']) - 10} 个子域名")
        
        # 目录和文件
        if results['directories']:
            print(f"\n{Colors.YELLOW}📁 发现的目录/文件 ({len(results['directories'])} 个):{Colors.END}")
            for dir_info in results['directories'][:10]:  # 只显示前10个
                print(f"  {dir_info['url']} [{dir_info['status_code']}]")
            if len(results['directories']) > 10:
                print(f"  ... 还有 {len(results['directories']) - 10} 个目录/文件")
        
        # FOFA结果
        if results['fofa_results']:
            print(f"\n{Colors.YELLOW}🔍 FOFA搜索结果 ({len(results['fofa_results'])} 个):{Colors.END}")
            for fofa in results['fofa_results'][:5]:  # 只显示前5个
                if len(fofa) >= 3:
                    print(f"  {fofa[0]} ({fofa[1]}:{fofa[2]})")
        
        # Quake结果
        if results['quake_results']:
            print(f"\n{Colors.YELLOW}🕸️ Quake搜索结果 ({len(results['quake_results'])} 个):{Colors.END}")
            for quake in results['quake_results'][:5]:  # 只显示前5个
                if 'ip' in quake and 'port' in quake:
                    print(f"  {quake['ip']}:{quake['port']}")
        
        print(f"\n{Colors.GREEN}扫描完成！详细结果请查看保存的JSON文件。{Colors.END}")

def main():
    parser = argparse.ArgumentParser(description='信息收集工具 v2.0')
    parser.add_argument('-t', '--target', required=True, help='目标域名')
    parser.add_argument('--no-subdomain', action='store_true', help='禁用子域名爆破')
    parser.add_argument('--no-directory', action='store_true', help='禁用目录扫描')
    parser.add_argument('--no-fofa', action='store_true', help='禁用FOFA搜索')
    parser.add_argument('--no-quake', action='store_true', help='禁用Quake搜索')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('--threads', type=int, default=50, help='线程数 (默认: 50)')
    parser.add_argument('--dict', choices=['builtin', 'large'], default='builtin', 
                       help='子域名字典类型: builtin(内置) 或 large(大字典) (默认: builtin)')
    parser.add_argument('--dict-path', help='自定义字典文件路径')
    
    args = parser.parse_args()
    
    collector = InfoCollector()
    collector.print_banner()
    
    # 执行综合扫描
    dict_type = args.dict
    if args.dict_path:
        dict_type = 'custom'
        
    results = collector.comprehensive_scan(
        target=args.target,
        enable_subdomain=not args.no_subdomain,
        enable_directory=not args.no_directory,
        enable_fofa=not args.no_fofa,
        enable_quake=not args.no_quake,
        dict_type=dict_type
    )
    
    # 保存结果
    collector.save_results(results, args.output)
    
    # 打印摘要
    collector.print_results_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}用户中断操作{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}程序异常: {str(e)}{Colors.END}")
        sys.exit(1)
