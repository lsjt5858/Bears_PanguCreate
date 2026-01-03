"""
批量导入路由
处理批量导入相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.import_service import import_service

import_bp = Blueprint('import', __name__, url_prefix='/api/import')


@import_bp.route('/formats', methods=['GET'])
@login_required
def get_supported_formats():
    """获取支持的导入格式
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    responses:
      200:
        description: 支持的格式列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    formats = import_service.get_supported_formats()
    return jsonify({
        'data': formats
    })


@import_bp.route('/types', methods=['GET'])
@login_required
def get_import_types():
    """获取支持的导入类型
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    responses:
      200:
        description: 支持的导入类型列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    types = import_service.get_import_types()
    return jsonify({
        'data': types
    })


@import_bp.route('/parse', methods=['POST'])
@login_required
def parse_content():
    """解析导入内容（预览）
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - content
            - format
          properties:
            content:
              type: string
              description: 要解析的内容
            format:
              type: string
              description: 内容格式 (json/csv/jsonl)
            delimiter:
              type: string
              description: CSV 分隔符
            has_header:
              type: boolean
              description: CSV 是否有表头
    responses:
      200:
        description: 解析结果
      400:
        description: 解析失败
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    content = data.get('content')
    format = data.get('format', 'json')
    
    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    
    options = {
        'delimiter': data.get('delimiter', ','),
        'has_header': data.get('has_header', True)
    }
    
    parsed_data, error = import_service.parse_content(content, format, **options)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'data': parsed_data,
        'count': len(parsed_data)
    })


@import_bp.route('/validate', methods=['POST'])
@login_required
def validate_import():
    """验证导入数据
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - data
            - import_type
          properties:
            data:
              type: array
              description: 要验证的数据
              items:
                type: object
            import_type:
              type: string
              description: 导入类型 (template/fields/datasource/data)
    responses:
      200:
        description: 验证结果
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    import_data = data.get('data', [])
    import_type = data.get('import_type')
    
    if not import_data:
        return jsonify({'error': '数据不能为空'}), 400
    
    if not import_type:
        return jsonify({'error': '导入类型不能为空'}), 400
    
    valid_data, errors = import_service.validate_import_data(import_data, import_type)
    
    return jsonify({
        'total': len(import_data),
        'valid_count': len(valid_data),
        'error_count': len(errors),
        'valid_data': valid_data,
        'errors': errors
    })


@import_bp.route('', methods=['POST'])
@login_required
def import_data():
    """执行批量导入
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - content
            - format
            - import_type
          properties:
            content:
              type: string
              description: 要导入的内容
            format:
              type: string
              description: 内容格式 (json/csv/jsonl)
            import_type:
              type: string
              description: 导入类型 (template/fields/datasource/data)
            delimiter:
              type: string
              description: CSV 分隔符
            has_header:
              type: boolean
              description: CSV 是否有表头
    responses:
      200:
        description: 导入结果
      400:
        description: 导入失败
    """
    user_id = g.current_user.id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    content = data.get('content')
    format = data.get('format', 'json')
    import_type = data.get('import_type')
    
    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    
    if not import_type:
        return jsonify({'error': '导入类型不能为空'}), 400
    
    options = {
        'delimiter': data.get('delimiter', ','),
        'has_header': data.get('has_header', True)
    }
    
    result = import_service.process_import(user_id, content, format, import_type, **options)
    
    if not result['success']:
        return jsonify(result), 400
    
    return jsonify(result)


@import_bp.route('/template-example', methods=['GET'])
@login_required
def get_template_example():
    """获取模板导入示例
    ---
    tags:
      - 批量导入
    security:
      - BearerAuth: []
    responses:
      200:
        description: 模板导入示例
    """
    example = {
        'json': [
            {
                'name': '用户信息模板',
                'description': '生成用户基本信息',
                'category': 'user',
                'fields': [
                    {'name': 'id', 'type': 'uuid'},
                    {'name': 'name', 'type': 'name'},
                    {'name': 'email', 'type': 'email'},
                    {'name': 'phone', 'type': 'phone'}
                ]
            }
        ],
        'csv': 'name,type,options\nid,uuid,\nname,name,\nemail,email,\nphone,phone,'
    }
    
    return jsonify({
        'data': example
    })
