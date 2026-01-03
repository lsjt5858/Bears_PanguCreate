"""
通知路由
处理通知相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.notification_service import notification_service

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')


@notification_bp.route('', methods=['GET'])
@login_required
def list_notifications():
    """获取通知列表
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    parameters:
      - name: unread_only
        in: query
        type: boolean
        required: false
        description: 是否只返回未读通知
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
        description: 通知列表
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
            pagination:
              type: object
            unread_count:
              type: integer
    """
    user_id = g.current_user.id
    
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    notifications, total = notification_service.get_notifications(
        user_id=user_id,
        unread_only=unread_only,
        page=page,
        page_size=page_size
    )
    
    unread_count = notification_service.get_unread_count(user_id)
    
    return jsonify({
        'data': [n.to_dict() for n in notifications],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        },
        'unread_count': unread_count
    })


@notification_bp.route('/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    """获取未读通知数量
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    responses:
      200:
        description: 未读数量
        schema:
          type: object
          properties:
            count:
              type: integer
    """
    user_id = g.current_user.id
    count = notification_service.get_unread_count(user_id)
    
    return jsonify({
        'count': count
    })


@notification_bp.route('/<notification_id>/read', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    """标记通知为已读
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    parameters:
      - name: notification_id
        in: path
        type: string
        required: true
        description: 通知ID
    responses:
      200:
        description: 标记成功
      404:
        description: 通知不存在
    """
    user_id = g.current_user.id
    
    success, message = notification_service.mark_as_read(notification_id, user_id)
    
    if not success:
        return jsonify({'error': message}), 404
    
    return jsonify({
        'message': message
    })


@notification_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_as_read():
    """标记所有通知为已读
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    responses:
      200:
        description: 标记成功
        schema:
          type: object
          properties:
            message:
              type: string
            count:
              type: integer
    """
    user_id = g.current_user.id
    
    count = notification_service.mark_all_as_read(user_id)
    
    return jsonify({
        'message': f'已标记 {count} 条通知为已读',
        'count': count
    })


@notification_bp.route('/<notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """删除通知
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    parameters:
      - name: notification_id
        in: path
        type: string
        required: true
        description: 通知ID
    responses:
      200:
        description: 删除成功
      404:
        description: 通知不存在
    """
    user_id = g.current_user.id
    
    success, message = notification_service.delete_notification(notification_id, user_id)
    
    if not success:
        return jsonify({'error': message}), 404
    
    return jsonify({
        'message': message
    })


@notification_bp.route('/clear-read', methods=['DELETE'])
@login_required
def clear_read_notifications():
    """清除所有已读通知
    ---
    tags:
      - 通知系统
    security:
      - BearerAuth: []
    responses:
      200:
        description: 清除成功
        schema:
          type: object
          properties:
            message:
              type: string
            count:
              type: integer
    """
    user_id = g.current_user.id
    
    count = notification_service.delete_all_read(user_id)
    
    return jsonify({
        'message': f'已清除 {count} 条已读通知',
        'count': count
    })
