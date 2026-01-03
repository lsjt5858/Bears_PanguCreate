"""
审计日志路由
处理审计日志相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.audit_service import audit_service

audit_bp = Blueprint('audit', __name__, url_prefix='/api/audit')


@audit_bp.route('/actions', methods=['GET'])
@login_required
def get_actions():
    """获取操作类型列表
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    responses:
      200:
        description: 操作类型列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    actions = audit_service.get_actions()
    return jsonify({
        'data': actions
    })


@audit_bp.route('/resource-types', methods=['GET'])
@login_required
def get_resource_types():
    """获取资源类型列表
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    responses:
      200:
        description: 资源类型列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    resource_types = audit_service.get_resource_types()
    return jsonify({
        'data': resource_types
    })


@audit_bp.route('/logs', methods=['GET'])
@login_required
def get_logs():
    """获取审计日志列表
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: query
        type: integer
        required: false
        description: 用户ID
      - name: action
        in: query
        type: string
        required: false
        description: 操作类型
      - name: resource_type
        in: query
        type: string
        required: false
        description: 资源类型
      - name: start_date
        in: query
        type: string
        required: false
        description: 开始日期 (ISO 格式)
      - name: end_date
        in: query
        type: string
        required: false
        description: 结束日期 (ISO 格式)
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
        description: 审计日志列表
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
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action')
    resource_type = request.args.get('resource_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    logs, total = audit_service.get_logs(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'data': [log.to_dict() for log in logs],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@audit_bp.route('/logs/<log_id>', methods=['GET'])
@login_required
def get_log(log_id):
    """获取审计日志详情
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    parameters:
      - name: log_id
        in: path
        type: string
        required: true
        description: 日志ID
    responses:
      200:
        description: 审计日志详情
      404:
        description: 日志不存在
    """
    log = audit_service.get_log(log_id)
    
    if not log:
        return jsonify({'error': '日志不存在'}), 404
    
    return jsonify({
        'data': log.to_dict()
    })


@audit_bp.route('/my-activity', methods=['GET'])
@login_required
def get_my_activity():
    """获取当前用户活动摘要
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    parameters:
      - name: days
        in: query
        type: integer
        required: false
        default: 7
        description: 统计天数
    responses:
      200:
        description: 用户活动摘要
    """
    user_id = g.current_user.id
    days = request.args.get('days', 7, type=int)
    
    summary = audit_service.get_user_activity_summary(user_id, days)
    
    return jsonify({
        'data': summary
    })


@audit_bp.route('/system-activity', methods=['GET'])
@login_required
def get_system_activity():
    """获取系统活动摘要（管理员）
    ---
    tags:
      - 审计日志
    security:
      - BearerAuth: []
    parameters:
      - name: days
        in: query
        type: integer
        required: false
        default: 7
        description: 统计天数
    responses:
      200:
        description: 系统活动摘要
    """
    days = request.args.get('days', 7, type=int)
    
    summary = audit_service.get_system_activity_summary(days)
    
    return jsonify({
        'data': summary
    })
