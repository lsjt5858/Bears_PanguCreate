"""
数据脱敏路由
处理数据脱敏相关的 API 请求
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.masking_service import masking_service

masking_bp = Blueprint('masking', __name__, url_prefix='/api/masking')


@masking_bp.route('/strategies', methods=['GET'])
@login_required
def get_strategies():
    """获取支持的脱敏策略
    ---
    tags:
      - 数据脱敏
    security:
      - BearerAuth: []
    responses:
      200:
        description: 脱敏策略列表
        schema:
          type: object
          properties:
            data:
              type: object
    """
    strategies = masking_service.get_strategies()
    return jsonify({
        'data': strategies
    })


@masking_bp.route('/presets', methods=['GET'])
@login_required
def get_preset_rules():
    """获取预定义的脱敏规则
    ---
    tags:
      - 数据脱敏
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
    presets = masking_service.get_preset_rules()
    return jsonify({
        'data': presets
    })


@masking_bp.route('/mask', methods=['POST'])
@login_required
def mask_data():
    """对数据进行脱敏处理
    ---
    tags:
      - 数据脱敏
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
              description: 要脱敏的数据记录
              items:
                type: object
            rules:
              type: object
              description: 字段脱敏规则
              additionalProperties:
                type: object
                properties:
                  strategy:
                    type: string
                    description: 脱敏策略
                  preset:
                    type: string
                    description: 预定义规则名称
    responses:
      200:
        description: 脱敏后的数据
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    records = data.get('data', [])
    rules = data.get('rules', {})
    
    if not records:
        return jsonify({'error': '数据不能为空'}), 400
    
    if not rules:
        return jsonify({'error': '脱敏规则不能为空'}), 400
    
    try:
        masked_records = masking_service.mask_records(records, rules)
        return jsonify({
            'data': masked_records,
            'count': len(masked_records)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@masking_bp.route('/mask-value', methods=['POST'])
@login_required
def mask_single_value():
    """对单个值进行脱敏
    ---
    tags:
      - 数据脱敏
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
          properties:
            value:
              type: string
              description: 要脱敏的值
            strategy:
              type: string
              description: 脱敏策略
            preset:
              type: string
              description: 预定义规则名称
            options:
              type: object
              description: 策略选项
    responses:
      200:
        description: 脱敏后的值
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    value = data.get('value')
    if value is None:
        return jsonify({'error': '值不能为空'}), 400
    
    preset = data.get('preset')
    strategy = data.get('strategy', 'mask')
    options = data.get('options', {})
    
    try:
        if preset:
            masked_value = masking_service.apply_preset_rule(value, preset)
        else:
            masked_value = masking_service.mask_value(value, strategy, **options)
        
        return jsonify({
            'original': value,
            'masked': masked_value,
            'strategy': preset or strategy
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@masking_bp.route('/auto-detect', methods=['POST'])
@login_required
def auto_detect_and_mask():
    """自动检测数据类型并脱敏
    ---
    tags:
      - 数据脱敏
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
          properties:
            value:
              type: string
              description: 要检测和脱敏的值
    responses:
      200:
        description: 检测和脱敏结果
      400:
        description: 请求参数错误
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    value = data.get('value')
    if value is None:
        return jsonify({'error': '值不能为空'}), 400
    
    try:
        masked_value, detected_type = masking_service.auto_detect_and_mask(str(value))
        
        return jsonify({
            'original': value,
            'masked': masked_value,
            'detected_type': detected_type,
            'auto_detected': detected_type is not None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
