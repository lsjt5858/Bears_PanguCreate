"""
数据类型路由
"""
from flask import Blueprint, jsonify

from services import data_type_service

types_bp = Blueprint('types', __name__, url_prefix='/api')


@types_bp.route('/types', methods=['GET'])
def get_types():
    """获取所有支持的数据类型"""
    types = data_type_service.get_all_types()
    return jsonify({"success": True, "types": types})


@types_bp.route('/types/<category>', methods=['GET'])
def get_types_by_category(category: str):
    """按分类获取数据类型"""
    types = data_type_service.get_types_by_category(category)
    return jsonify({"success": True, "types": types})


@types_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有数据类型分类"""
    categories = data_type_service.get_categories()
    return jsonify({"success": True, "categories": categories})
