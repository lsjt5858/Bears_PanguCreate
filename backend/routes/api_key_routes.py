"""
API 密钥路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g
from datetime import datetime

from middleware import login_required
from services.api_key_service import api_key_service

api_key_bp = Blueprint('api_keys', __name__, url_prefix='/api/api-keys')


@api_key_bp.route('', methods=['GET'])
@login_required
def list_keys():
    """
    获取用户的API密钥列表
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: query
        name: project_id
        type: integer
      - in: query
        name: include_inactive
        type: boolean
        default: false
    responses:
      200:
        description: 返回密钥列表
    """
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
    keys = api_key_service.list_keys(user_id=user.id, project_id=project_id, include_inactive=include_inactive)
    return jsonify({'data': [k.to_dict() for k in keys]})


@api_key_bp.route('/<key_id>', methods=['GET'])
@login_required
def get_key(key_id):
    """
    获取密钥详情
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
    responses:
      200:
        description: 返回密钥详情
      404:
        description: 密钥不存在
    """
    user = g.current_user
    api_key = api_key_service.get_key(key_id, user.id)
    if not api_key:
        return jsonify({'error': '密钥不存在或无权访问'}), 404
    return jsonify({'data': api_key.to_dict()})


@api_key_bp.route('', methods=['POST'])
@login_required
def create_key():
    """
    创建API密钥
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: 密钥名称
            permissions:
              type: array
              items:
                type: string
                enum: [read, write, admin]
              default: [read]
            project_id:
              type: integer
            expires_at:
              type: string
              format: date-time
    responses:
      201:
        description: 创建成功，返回完整密钥（仅此一次）
    """
    user = g.current_user
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': '密钥名称不能为空'}), 400
    
    expires_at = None
    if data.get('expires_at'):
        try:
            expires_at = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': '无效的过期时间格式'}), 400
    
    api_key, full_key = api_key_service.create_key(
        user_id=user.id, name=data['name'], permissions=data.get('permissions', ['read']),
        project_id=data.get('project_id'), expires_at=expires_at
    )
    
    result = api_key.to_dict()
    result['key'] = full_key
    return jsonify({'message': '密钥创建成功，请妥善保存，密钥只显示一次', 'data': result}), 201


@api_key_bp.route('/<key_id>', methods=['PUT'])
@login_required
def update_key(key_id):
    """
    更新密钥
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            permissions:
              type: array
            expires_at:
              type: string
    responses:
      200:
        description: 更新成功
    """
    user = g.current_user
    data = request.get_json()
    
    if 'expires_at' in data and data['expires_at']:
        try:
            data['expires_at'] = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': '无效的过期时间格式'}), 400
    
    api_key, error = api_key_service.update_key(key_id, user.id, **data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': '密钥更新成功', 'data': api_key.to_dict()})


@api_key_bp.route('/<key_id>', methods=['DELETE'])
@login_required
def delete_key(key_id):
    """
    删除密钥
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
    responses:
      200:
        description: 删除成功
    """
    user = g.current_user
    success, error = api_key_service.delete_key(key_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    return jsonify({'message': '密钥删除成功'})


@api_key_bp.route('/<key_id>/revoke', methods=['POST'])
@login_required
def revoke_key(key_id):
    """
    撤销密钥
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
    responses:
      200:
        description: 撤销成功
    """
    user = g.current_user
    success, error = api_key_service.revoke_key(key_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    return jsonify({'message': '密钥已撤销'})


@api_key_bp.route('/<key_id>/regenerate', methods=['POST'])
@login_required
def regenerate_key(key_id):
    """
    重新生成密钥
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
    responses:
      200:
        description: 重新生成成功
    """
    user = g.current_user
    new_key, error = api_key_service.regenerate_key(key_id, user.id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': '密钥已重新生成，请妥善保存', 'key': new_key})


@api_key_bp.route('/<key_id>/stats', methods=['GET'])
@login_required
def get_key_stats(key_id):
    """
    获取密钥使用统计
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
      - in: query
        name: days
        type: integer
        default: 7
    responses:
      200:
        description: 返回使用统计
    """
    user = g.current_user
    days = request.args.get('days', 7, type=int)
    days = min(days, 90)
    stats = api_key_service.get_usage_stats(key_id, user.id, days=days)
    if stats is None:
        return jsonify({'error': '密钥不存在或无权访问'}), 404
    return jsonify({'data': stats})


@api_key_bp.route('/<key_id>/logs', methods=['GET'])
@login_required
def get_key_logs(key_id):
    """
    获取密钥使用日志
    ---
    tags:
      - API密钥
    security:
      - Bearer: []
    parameters:
      - in: path
        name: key_id
        type: string
        required: true
      - in: query
        name: page
        type: integer
      - in: query
        name: page_size
        type: integer
    responses:
      200:
        description: 返回使用日志
    """
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    page_size = min(page_size, 100)
    logs, total = api_key_service.get_usage_logs(key_id, user.id, page=page, page_size=page_size)
    return jsonify({'data': logs, 'pagination': {'page': page, 'page_size': page_size, 'total': total, 'total_pages': (total + page_size - 1) // page_size}})


@api_key_bp.route('/verify', methods=['POST'])
def verify_key():
    """
    验证API密钥
    ---
    tags:
      - API密钥
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - key
          properties:
            key:
              type: string
              description: API密钥
    responses:
      200:
        description: 密钥有效
      401:
        description: 密钥无效
    """
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify({'valid': False, 'error': '请提供密钥'}), 400
    api_key = api_key_service.verify_key(key)
    if not api_key:
        return jsonify({'valid': False, 'error': '无效的密钥'}), 401
    return jsonify({'valid': True, 'data': {'name': api_key.name, 'permissions': api_key.permission_list, 'expires_at': api_key.expires_at.isoformat() if api_key.expires_at else None}})
