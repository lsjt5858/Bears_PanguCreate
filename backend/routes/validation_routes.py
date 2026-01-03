"""
数据验证路由
处理数据验证相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.validation_service import validation_service

validation_bp = Blueprint('validation', __name__, url_prefix='/api/validation')


@validation_bp.route('/rule-types', methods=['GET'])
@login_required
def get_rule_types():
    """获取支持的验证规则类型
    ---
    tags:
      - 数据验证
    security:
      - BearerAuth: []
    responses:
      200:
        description: 规则类型列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    rule_types = validation_service.get_rule_types()
    return jsonify({
        'data': rule_types
    })


@validation_bp.route('/presets', methods=['GET'])
@login_required
def get_preset_rules():
    """获取预定义的验证规则
    ---
    tags:
      - 数据验证
    security:
      - BearerAuth: []
    responses:
      200:
        description: 预定义规则列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    presets = validation_service.get_preset_rules()
    return jsonify({
        'data': presets
    })


@validation_bp.route('/validate', methods=['POST'])
@login_required
def validate_data():
    """验证数据
    ---
    tags:
      - 数据验证
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
            - rules
          properties:
            data:
              type: array
              description: 要验证的数据记录
              items:
                type: object
            rules:
              type: object
              description: 字段验证规则
              additionalProperties:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: 规则类型
                    message:
                      type: string
                      description: 错误消息
            check_unique:
              type: boolean
              description: 是否检查记录间唯一性
    responses:
      200:
        description: 验证结果
        schema:
          type: object
          properties:
            results:
              type: array
              items:
                type: object
            summary:
              type: object
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    records = data.get('data', [])
    rules = data.get('rules', {})
    check_unique = data.get('check_unique', False)
    
    if not records:
        return jsonify({'error': '数据不能为空'}), 400
    
    if not rules:
        return jsonify({'error': '验证规则不能为空'}), 400
    
    try:
        results = validation_service.validate_records(records, rules, check_unique)
        summary = validation_service.get_validation_summary(results)
        
        return jsonify({
            'results': results,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@validation_bp.route('/validate-value', methods=['POST'])
@login_required
def validate_single_value():
    """验证单个值
    ---
    tags:
      - 数据验证
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - value
            - rules
          properties:
            value:
              description: 要验证的值
            rules:
              type: array
              description: 验证规则列表
              items:
                type: object
                properties:
                  type:
                    type: string
                    description: 规则类型
    responses:
      200:
        description: 验证结果
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    value = data.get('value')
    rules = data.get('rules', [])
    
    if not rules:
        return jsonify({'error': '验证规则不能为空'}), 400
    
    try:
        errors = validation_service.validate_field(value, rules)
        
        return jsonify({
            'value': value,
            'valid': len(errors) == 0,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@validation_bp.route('/validate-preset', methods=['POST'])
@login_required
def validate_with_preset():
    """使用预定义规则验证
    ---
    tags:
      - 数据验证
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - value
            - preset
          properties:
            value:
              type: string
              description: 要验证的值
            preset:
              type: string
              description: 预定义规则名称
    responses:
      200:
        description: 验证结果
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    value = data.get('value')
    preset = data.get('preset')
    
    if not preset:
        return jsonify({'error': '预定义规则名称不能为空'}), 400
    
    try:
        valid, error = validation_service.validate_preset(value, preset)
        
        return jsonify({
            'value': value,
            'preset': preset,
            'valid': valid,
            'error': error
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
