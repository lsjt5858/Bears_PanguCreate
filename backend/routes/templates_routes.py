"""
模板路由
"""
from flask import Blueprint, jsonify, request

from services import template_service

templates_bp = Blueprint('templates', __name__, url_prefix='/api')


@templates_bp.route('/templates', methods=['GET'])
def get_templates():
    """获取所有模板"""
    templates = template_service.get_all()
    return jsonify({"success": True, "templates": templates})


@templates_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id: str):
    """获取单个模板"""
    template = template_service.get_by_id(template_id)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "template": template})


@templates_bp.route('/templates/category/<category>', methods=['GET'])
def get_templates_by_category(category: str):
    """按分类获取模板"""
    templates = template_service.get_by_category(category)
    return jsonify({"success": True, "templates": templates})


@templates_bp.route('/templates', methods=['POST'])
def create_template():
    """创建模板"""
    data = request.get_json()
    template = template_service.create(data)
    return jsonify({"success": True, "template": template}), 201


@templates_bp.route('/templates/<template_id>', methods=['PUT'])
def update_template(template_id: str):
    """更新模板"""
    data = request.get_json()
    template = template_service.update(template_id, data)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "template": template})


@templates_bp.route('/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id: str):
    """删除模板"""
    success = template_service.delete(template_id)
    if not success:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "message": "Template deleted"})
