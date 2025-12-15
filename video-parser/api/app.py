# -*- coding: utf-8 -*-
"""
视频解析API服务
"""

from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入核心解析器
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.parser import parse_video_url

app = Flask(__name__)

@app.route('/api/parse', methods=['POST'])
def parse_video():
    """解析视频API接口"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required parameter: url'
            }), 400

        url = data['url']
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL cannot be empty'
            }), 400

        # 解析视频
        logger.info(f"解析视频URL: {url}")
        result = parse_video_url(url)

        # 添加免责声明
        if result.get('success') and result.get('downloadable'):
            result['disclaimer'] = "本工具仅解析平台允许下载的公开视频内容，请遵守原平台版权与使用协议"

        return jsonify(result)

    except Exception as e:
        logger.error(f"解析视频时发生错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/platforms', methods=['GET'])
def get_supported_platforms():
    """获取支持的平台列表"""
    platforms = [
        {
            'id': 'bilibili',
            'name': '哔哩哔哩',
            'enabled': True
        },
        {
            'id': 'douyin',
            'name': '抖音',
            'enabled': True
        },
        {
            'id': 'kuaishou',
            'name': '快手',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'xiaohongshu',
            'name': '小红书',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'tencent_video',
            'name': '腾讯视频',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'iqiyi',
            'name': '爱奇艺',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'twitter',
            'name': 'Twitter/X',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'youtube',
            'name': 'YouTube',
            'enabled': True
        },
        {
            'id': 'vimeo',
            'name': 'Vimeo',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'dailymotion',
            'name': 'Dailymotion',
            'enabled': False  # 示例中未实现
        }
    ]

    return jsonify({
        'success': True,
        'platforms': platforms
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'Video Parser API is running'
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': 'API endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
