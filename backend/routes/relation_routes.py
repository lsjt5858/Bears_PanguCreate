"""
关联数据生成路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.relation_generator_service import relation_generator_service

relation_bp = Blueprint('relation', __name__, url_prefix='/api/relation')

@relation_bp.route('/generate', methods=['POST'])
@login_required
def generate_relation_data():
    """生成关联数据
    ---
    tags:
      - 关联数据生成
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - tables
          properties:
            tables:
              type: array
              description: 表定义列表
              items:
                type: object
                properties:
                  name:
                    type: string
                    description: 表名
                  count:
                    type: integer
                    description: 生成数量
                  fields:
                    type: array
                    description: 字段定义
                    items:
                      type: object
            relations:
              type: array
              description: 关联关系定义
              items:
                type: object
                properties:
                  sourceTable:
                    type: string
                    description: 源表名
                  sourceField:
                    type: string
                    description: 源字段
                  targetTable:
                    type: string
                    description: 目标表名
                  targetField:
                    type: string
                    description: 目标字段
                  type:
                    type: string
                    description: 关联类型 (one-to-one/one-to-many/many-to-many)
    responses:
      200:
        description: 生成成功
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              description: 生成的关联数据
      400:
        description: 请求参数错误
      500:
        description: 生成失败
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    tables = data.get('tables', [])
    relations = data.get('relations', [])
    
    if not tables:
        return jsonify({'error': 'Tables definition is required'}), 400
        
    try:
        result = relation_generator_service.generate_relation_data(tables, relations)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Relation generation error: {e}")
        return jsonify({'error': str(e)}), 500
