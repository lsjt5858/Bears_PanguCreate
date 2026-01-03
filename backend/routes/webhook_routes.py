"""
Webhook 路由
处理 Webhook 相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.webhook_service import webhook_service

webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhooks')


@webhook_bp.route('/events', methods=['GET'])
@login_required
def get_supported_events():
    """获取支持的事件类型
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    responses:
      200:
        description: 事件类型列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    events = webhook_service.get_supported_events()
    return jsonify({
        'data': events
    })


@webhook_bp.route('', methods=['GET'])
@login_required
def list_webhooks():
    """获取 Webhook 列表
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: 页码
      - name: page_size
        in: query
        type: integer
        required: false
        default: 20
        description: 每页数量
    responses:
      200:
        description: Webhook 列表
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
            pagination:
              type: object
    """
    user_id = g.current_user.id
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    webhooks, total = webhook_service.get_webhooks(
        user_id=user_id,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'data': [w.to_dict() for w in webhooks],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@webhook_bp.route('', methods=['POST'])
@login_required
def create_webhook():
    """创建 Webhook
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - url
            - events
          properties:
            name:
              type: string
              description: Webhook 名称
            url:
              type: string
              description: 回调 URL
            events:
              type: array
              items:
                type: string
              description: 订阅的事件类型
            description:
              type: string
              description: 描述
            method:
              type: string
              description: 请求方法 (POST/GET)
            headers:
              type: object
              description: 自定义请求头
            secret:
              type: string
              description: 签名密钥
    responses:
      201:
        description: 创建成功
      400:
        description: 请求参数错误
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    required_fields = ['name', 'url', 'events']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    webhook, error = webhook_service.create_webhook(
        user_id=user_id,
        name=data['name'],
        url=data['url'],
        events=data['events'],
        description=data.get('description'),
        method=data.get('method', 'POST'),
        headers=data.get('headers'),
        secret=data.get('secret')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Webhook 创建成功',
        'data': webhook.to_dict()
    }), 201


@webhook_bp.route('/<webhook_id>', methods=['GET'])
@login_required
def get_webhook(webhook_id):
    """获取 Webhook 详情
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: webhook_id
        in: path
        type: string
        required: true
        description: Webhook ID
    responses:
      200:
        description: Webhook 详情
      404:
        description: Webhook 不存在
    """
    user_id = g.current_user.id
    
    webhook = webhook_service.get_webhook(webhook_id, user_id)
    if not webhook:
        return jsonify({'error': 'Webhook 不存在'}), 404
    
    return jsonify({
        'data': webhook.to_dict()
    })


@webhook_bp.route('/<webhook_id>', methods=['PUT'])
@login_required
def update_webhook(webhook_id):
    """更新 Webhook
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: webhook_id
        in: path
        type: string
        required: true
        description: Webhook ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            url:
              type: string
            events:
              type: array
              items:
                type: string
            description:
              type: string
            method:
              type: string
            headers:
              type: object
            secret:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: 更新成功
      400:
        description: 请求参数错误
      404:
        description: Webhook 不存在
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    webhook, error = webhook_service.update_webhook(
        webhook_id=webhook_id,
        user_id=user_id,
        **data
    )
    
    if error:
        status_code = 404 if 'not found' in error.lower() or '不存在' in error else 400
        return jsonify({'error': error}), status_code
    
    return jsonify({
        'message': 'Webhook 更新成功',
        'data': webhook.to_dict()
    })


@webhook_bp.route('/<webhook_id>', methods=['DELETE'])
@login_required
def delete_webhook(webhook_id):
    """删除 Webhook
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: webhook_id
        in: path
        type: string
        required: true
        description: Webhook ID
    responses:
      200:
        description: 删除成功
      404:
        description: Webhook 不存在
    """
    user_id = g.current_user.id
    
    success, message = webhook_service.delete_webhook(webhook_id, user_id)
    
    if not success:
        return jsonify({'error': message}), 404
    
    return jsonify({
        'message': message
    })


@webhook_bp.route('/<webhook_id>/toggle', methods=['POST'])
@login_required
def toggle_webhook(webhook_id):
    """切换 Webhook 状态
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: webhook_id
        in: path
        type: string
        required: true
        description: Webhook ID
    responses:
      200:
        description: 切换成功
      404:
        description: Webhook 不存在
    """
    user_id = g.current_user.id
    
    webhook, error = webhook_service.toggle_webhook(webhook_id, user_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'message': f'Webhook 已{"启用" if webhook.is_active else "禁用"}',
        'data': webhook.to_dict()
    })


@webhook_bp.route('/<webhook_id>/test', methods=['POST'])
@login_required
def test_webhook(webhook_id):
    """测试 Webhook
    ---
    tags:
      - Webhook
    security:
      - BearerAuth: []
    parameters:
      - name: webhook_id
        in: path
        type: string
        required: true
        description: Webhook ID
    responses:
      200:
        description: 测试结果
      404:
        description: Webhook 不存在
    """
    user_id = g.current_user.id
    
    success, message = webhook_service.test_webhook(webhook_id, user_id)
    
    return jsonify({
        'success': success,
        'message': message
    })
