"""
数据生成路由
"""
from flask import Blueprint, jsonify, request

from services import data_generator_service

generate_bp = Blueprint('generate', __name__, url_prefix='/api')


@generate_bp.route('/generate', methods=['POST'])
def generate():
    """生成测试数据"""
    data = request.get_json()
    fields = data.get("fields", [])
    count = data.get("count", 10)
    
    # 参数验证
    if count < 1 or count > 10000:
        return jsonify({
            "success": False, 
            "error": "count must be between 1 and 10000"
        }), 400
    
    if not fields:
        return jsonify({
            "success": False, 
            "error": "fields is required"
        }), 400
    
    # 生成数据
    result = data_generator_service.generate_data(fields, count)
    
    return jsonify({
        "success": True, 
        "data": result, 
        "count": len(result),
        "fields": fields  # 返回字段配置以便前端确认顺序
    })
