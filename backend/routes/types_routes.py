"""
数据类型路由
"""
from flask import Blueprint, jsonify

from services import data_type_service

types_bp = Blueprint('types', __name__, url_prefix='/api')


@types_bp.route('/types', methods=['GET'])
def get_types():
    """
    获取所有支持的数据类型
    ---
    tags:
      - 数据生成
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
    """
    types = data_type_service.get_all_types()
    return jsonify({"success": True, "types": types})


@types_bp.route('/types/<category>', methods=['GET'])
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
        description: 分类名称（如 basic, personal, business 等）
    responses:
      200:
        description: 返回指定分类的数据类型
    """
    types = data_type_service.get_types_by_category(category)
    return jsonify({"success": True, "types": types})


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
    return jsonify({"success": True, "categories": categories})
