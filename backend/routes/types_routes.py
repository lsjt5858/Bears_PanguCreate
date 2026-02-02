"""
数据类型路由
"""
from flask import Blueprint, jsonify, request

from services import data_type_service

types_bp = Blueprint('types', __name__, url_prefix='/api')


@types_bp.route('/types', methods=['GET'])
def get_types():
    """
    获取所有支持的数据类型
    支持搜索功能
    ---
    tags:
      - 数据生成
    parameters:
      - in: query
        name: keyword
        type: string
        required: false
        description: 搜索关键词（可选）
    responses:
      200:
        description: 返回所有数据类型列表
        schema:
          type: object
          properties:
            success:
              type: boolean
            types:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  icon:
                    type: string
                  category:
                    type: string
                  description:
                    type: string
    """
    keyword = request.args.get('keyword', '').strip()
    
    if keyword:
        types = data_type_service.search_types(keyword)
    else:
        types = data_type_service.get_all_types()
    
    return jsonify({
        "success": True, 
        "types": types,
        "count": len(types)
    })


@types_bp.route('/types/<type_id>', methods=['GET'])
def get_type_by_id(type_id: str):
    """
    根据ID获取单个数据类型
    ---
    tags:
      - 数据生成
    parameters:
      - in: path
        name: type_id
        type: string
        required: true
        description: 数据类型ID
    responses:
      200:
        description: 返回数据类型详情
      404:
        description: 数据类型不存在
    """
    data_type = data_type_service.get_type_by_id(type_id)
    
    if data_type:
        return jsonify({"success": True, "type": data_type})
    else:
        return jsonify({"success": False, "message": "数据类型不存在"}), 404


@types_bp.route('/types/category/<category>', methods=['GET'])
def get_types_by_category(category: str):
    """
    按分类获取数据类型
    ---
    tags:
      - 数据生成
    parameters:
      - in: path
        name: category
        type: string
        required: true
        description: 分类ID（如 identifier, personal, address 等）
    responses:
      200:
        description: 返回指定分类的数据类型
    """
    types = data_type_service.get_types_by_category(category)
    return jsonify({
        "success": True, 
        "types": types,
        "count": len(types)
    })


@types_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    获取所有数据类型分类
    ---
    tags:
      - 数据生成
    responses:
      200:
        description: 返回所有分类列表
    """
    categories = data_type_service.get_categories()
    return jsonify({
        "success": True, 
        "categories": categories,
        "count": len(categories)
    })


@types_bp.route('/types/statistics', methods=['GET'])
def get_statistics():
    """
    获取数据类型统计信息
    ---
    tags:
      - 数据生成
    responses:
      200:
        description: 返回统计信息
    """
    stats = data_type_service.get_statistics()
    return jsonify({
        "success": True,
        "statistics": stats
    })

