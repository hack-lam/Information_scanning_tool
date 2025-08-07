#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息收集工具 Web版本
基于Flask的Web界面应用
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import threading
import time
from datetime import datetime
import os
from info_collector import InfoCollector

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 全局变量存储扫描任务
scan_tasks = {}
task_counter = 0

def generate_task_id():
    """生成任务ID"""
    global task_counter
    task_counter += 1
    return f"task_{task_counter}_{int(time.time())}"

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/info_collect')
def info_collect():
    """信息收集页面"""
    return render_template('info_collect.html')

@app.route('/subdomain')
def subdomain():
    """子域名爆破页面"""
    return render_template('subdomain.html')

@app.route('/directory')
def directory():
    """目录扫描页面"""
    return render_template('directory.html')

@app.route('/fofa_search')
def fofa_search():
    """FOFA搜索页面"""
    return render_template('fofa_search.html')

@app.route('/quake_search')
def quake_search():
    """Quake搜索页面"""
    return render_template('quake_search.html')

@app.route('/comprehensive')
def comprehensive():
    """综合扫描页面"""
    return render_template('comprehensive.html')

@app.route('/results')
def results():
    """结果查看页面"""
    return render_template('results.html')

@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

# API接口
@app.route('/api/scan/start', methods=['POST'])
def start_scan():
    """启动扫描任务"""
    try:
        data = request.get_json()
        target = data.get('target', '').strip()
        scan_type = data.get('scan_type', 'comprehensive')
        
        if not target:
            return jsonify({'success': False, 'message': '请输入目标域名'})
        
        task_id = generate_task_id()
        
        # 创建任务记录
        scan_tasks[task_id] = {
            'task_id': task_id,
            'target': target,
            'scan_type': scan_type,
            'status': 'running',
            'progress': 0,
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': None,
            'results': None,
            'error': None
        }
        
        # 启动后台扫描任务
        thread = threading.Thread(target=run_scan_task, args=(task_id, target, scan_type, data))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '扫描任务已启动'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'启动扫描失败: {str(e)}'})

def run_scan_task(task_id, target, scan_type, options):
    """运行扫描任务"""
    try:
        collector = InfoCollector()
        
        # 更新任务状态
        scan_tasks[task_id]['progress'] = 10
        
        if scan_type == 'whois':
            results = collector.get_whois_info(target)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'cdn':
            results = collector.check_cdn(target)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'subdomain':
            results = collector.subdomain_brute(target)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'directory':
            target_url = f"http://{target}"
            results = collector.scan_directory(target_url, collector.directory_dict)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'fofa':
            query = options.get('query', f'domain="{target}"')
            results = collector.fofa_search(query)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'quake':
            query = options.get('query', f'domain: "{target}"')
            results = collector.quake_search(query)
            scan_tasks[task_id]['progress'] = 100
            
        elif scan_type == 'comprehensive':
            # 综合扫描，分步骤更新进度
            scan_tasks[task_id]['progress'] = 20
            
            enable_subdomain = options.get('enable_subdomain', True)
            enable_directory = options.get('enable_directory', True)
            enable_fofa = options.get('enable_fofa', True)
            enable_quake = options.get('enable_quake', True)
            
            results = collector.comprehensive_scan(
                target=target,
                enable_subdomain=enable_subdomain,
                enable_directory=enable_directory,
                enable_fofa=enable_fofa,
                enable_quake=enable_quake
            )
            scan_tasks[task_id]['progress'] = 100
        
        else:
            raise ValueError(f'不支持的扫描类型: {scan_type}')
        
        # 更新任务结果
        scan_tasks[task_id]['status'] = 'completed'
        scan_tasks[task_id]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        scan_tasks[task_id]['results'] = results
        
    except Exception as e:
        scan_tasks[task_id]['status'] = 'failed'
        scan_tasks[task_id]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        scan_tasks[task_id]['error'] = str(e)

@app.route('/api/scan/status/<task_id>')
def get_scan_status(task_id):
    """获取扫描任务状态"""
    if task_id in scan_tasks:
        return jsonify(scan_tasks[task_id])
    else:
        return jsonify({'success': False, 'message': '任务不存在'})

@app.route('/api/scan/list')
def list_scan_tasks():
    """获取所有扫描任务列表"""
    tasks = []
    for task_id, task_info in scan_tasks.items():
        tasks.append({
            'task_id': task_id,
            'target': task_info['target'],
            'scan_type': task_info['scan_type'],
            'status': task_info['status'],
            'start_time': task_info['start_time'],
            'end_time': task_info['end_time']
        })
    
    # 按开始时间倒序排列
    tasks.sort(key=lambda x: x['start_time'], reverse=True)
    return jsonify({'tasks': tasks})

@app.route('/api/scan/result/<task_id>')
def get_scan_result(task_id):
    """获取扫描结果详情"""
    if task_id in scan_tasks:
        task = scan_tasks[task_id]
        if task['status'] == 'completed':
            return jsonify({
                'success': True,
                'task_info': task,
                'results': task['results']
            })
        else:
            return jsonify({
                'success': False,
                'message': f'任务状态: {task["status"]}',
                'task_info': task
            })
    else:
        return jsonify({'success': False, 'message': '任务不存在'})

@app.route('/api/scan/download/<task_id>')
def download_scan_result(task_id):
    """下载扫描结果"""
    if task_id in scan_tasks:
        task = scan_tasks[task_id]
        if task['status'] == 'completed' and task['results']:
            filename = f"scan_result_{task['target']}_{task_id}.json"
            filepath = os.path.join('downloads', filename)
            
            # 创建下载目录
            os.makedirs('downloads', exist_ok=True)
            
            # 保存结果到文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(task['results'], f, ensure_ascii=False, indent=2)
            
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'success': False, 'message': '任务未完成或无结果'})
    else:
        return jsonify({'success': False, 'message': '任务不存在'})

@app.route('/api/scan/delete/<task_id>', methods=['DELETE'])
def delete_scan_task(task_id):
    """删除扫描任务"""
    if task_id in scan_tasks:
        del scan_tasks[task_id]
        return jsonify({'success': True, 'message': '任务已删除'})
    else:
        return jsonify({'success': False, 'message': '任务不存在'})

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    
    print("=" * 60)
    print("信息收集工具 Web版本启动中...")
    print("访问地址: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
