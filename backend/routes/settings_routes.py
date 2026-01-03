"""
系统设置路由
处理系统设置相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.settings_service import settings_service

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')


@settings_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """获取设置分类
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    responses:
      200:
        description: 设置分类列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    categories = settings_service.get_categories()
    return jsonify({
        'data': categories
    })


@settings_bp.route('/public', methods=['GET'])
def get_public_settings():
    """获取公开设置（无需登录）
    ---
    tags:
      - 系统设置
    responses:
      200:
        description: 公开设置
        schema:
          type: object
          properties:
            data:
              type: object
    """
    settings = settings_service.get_public_settings()
    return jsonify({
        'data': settings
    })


@settings_bp.route('', methods=['GET'])
@login_required
def get_all_settings():
    """获取所有设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: category
        in: query
        type: string
        required: false
        description: 设置分类
    responses:
      200:
        description: 设置列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    category = request.args.get('category')
    
    # 检查是否是管理员
    is_admin = g.current_user.is_admin if hasattr(g.current_user, 'is_admin') else False
    public_only = not is_admin
    
    if category:
        settings = settings_service.get_settings_by_category(category, public_only)
        return jsonify({
            'data': {category: settings}
        })
    else:
        settings = settings_service.get_all_settings(public_only)
        return jsonify({
            'data': settings
        })


@settings_bp.route('/<key>', methods=['GET'])
@login_required
def get_setting(key):
    """获取单个设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: 设置键名
    responses:
      200:
        description: 设置详情
      404:
        description: 设置不存在
    """
    detail = settings_service.get_setting_detail(key)
    
    if not detail:
        # 尝试从默认设置获取
        value = settings_service.get_setting(key)
        if value is not None:
            return jsonify({
                'data': {
                    'key': key,
                    'value': value,
                    'is_default': True
                }
            })
        return jsonify({'error': '设置不存在'}), 404
    
    return jsonify({
        'data': detail
    })


@settings_bp.route('/<key>', methods=['PUT'])
@login_required
def update_setting(key):
    """更新单个设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: 设置键名
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - value
          properties:
            value:
              description: 设置值
            value_type:
              type: string
              description: 值类型
            description:
              type: string
              description: 描述
    responses:
      200:
        description: 更新成功
      400:
        description: 更新失败
    """
    data = request.get_json()
    
    if not data or 'value' not in data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    setting, error = settings_service.set_setting(
        key=key,
        value=data['value'],
        value_type=data.get('value_type'),
        description=data.get('description')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '设置已更新',
        'data': setting.to_dict()
    })


@settings_bp.route('', methods=['PUT'])
@login_required
def update_settings():
    """批量更新设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            settings:
              type: object
              description: 设置键值对
    responses:
      200:
        description: 更新结果
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data or 'settings' not in data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    updated, errors = settings_service.update_settings(data['settings'])
    
    return jsonify({
        'message': f'已更新 {updated} 项设置',
        'updated': updated,
        'errors': errors
    })


@settings_bp.route('/<key>', methods=['DELETE'])
@login_required
def delete_setting(key):
    """删除设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: 设置键名
    responses:
      200:
        description: 删除成功
      404:
        description: 设置不存在
    """
    success, message = settings_service.delete_setting(key)
    
    if not success:
        return jsonify({'error': message}), 404
    
    return jsonify({
        'message': message
    })


@settings_bp.route('/<key>/reset', methods=['POST'])
@login_required
def reset_setting(key):
    """重置设置为默认值
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: 设置键名
    responses:
      200:
        description: 重置成功
      400:
        description: 重置失败
    """
    success, message = settings_service.reset_to_default(key)
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'message': message
    })


@settings_bp.route('/category/<category>/reset', methods=['POST'])
@login_required
def reset_category(category):
    """重置分类下所有设置为默认值
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    parameters:
      - name: category
        in: path
        type: string
        required: true
        description: 设置分类
    responses:
      200:
        description: 重置成功
    """
    count = settings_service.reset_category_to_default(category)
    
    return jsonify({
        'message': f'已重置 {count} 项设置',
        'count': count
    })


@settings_bp.route('/init', methods=['POST'])
@login_required
def init_settings():
    """初始化默认设置
    ---
    tags:
      - 系统设置
    security:
      - BearerAuth: []
    responses:
      200:
        description: 初始化成功
    """
    settings_service.init_default_settings()
    
    return jsonify({
        'message': '默认设置已初始化'
    })
