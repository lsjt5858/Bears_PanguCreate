"""
模板路由
"""
from flask import Blueprint, jsonify, request

from services import template_service

templates_bp = Blueprint('templates', __name__, url_prefix='/api')


@templates_bp.route('/templates', methods=['GET'])
def get_templates():
    """
    获取所有模板
    ---
    tags:
      - 模板
    responses:
      200:
        description: 返回模板列表
        schema:
          type: object
          properties:
            success:
              type: boolean
            templates:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
                  category:
                    type: string
                  fields:
                    type: array
    """
    templates = template_service.get_all()
    return jsonify({"success": True, "templates": templates})


@templates_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id: str):
    """
    获取单个模板
    ---
    tags:
      - 模板
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
        description: 模板ID
    responses:
      200:
        description: 返回模板详情
      404:
        description: 模板不存在
    """
    template = template_service.get_by_id(template_id)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "template": template})


@templates_bp.route('/templates/category/<category>', methods=['GET'])
def get_templates_by_category(category: str):
    """
    按分类获取模板
    ---
    tags:
      - 模板
    parameters:
      - in: path
        name: category
        type: string
        required: true
        description: 分类名称
    responses:
      200:
        description: 返回指定分类的模板列表
    """
    templates = template_service.get_by_category(category)
    return jsonify({"success": True, "templates": templates})


@templates_bp.route('/templates', methods=['POST'])
def create_template():
    """
    创建模板
    ---
    tags:
      - 模板
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - fields
          properties:
            name:
              type: string
              description: 模板名称
            description:
              type: string
              description: 模板描述
            category:
              type: string
              description: 分类
            fields:
              type: array
              description: 字段配置
              items:
                type: object
    responses:
      201:
        description: 创建成功
    """
    data = request.get_json()
    template = template_service.create(data)
    return jsonify({"success": True, "template": template}), 201


@templates_bp.route('/templates/<template_id>', methods=['PUT'])
def update_template(template_id: str):
    """
    更新模板
    ---
    tags:
      - 模板
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            category:
              type: string
            fields:
              type: array
    responses:
      200:
        description: 更新成功
      404:
        description: 模板不存在
    """
    data = request.get_json()
    template = template_service.update(template_id, data)
    if not template:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "template": template})


@templates_bp.route('/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id: str):
    """
    删除模板
    ---
    tags:
      - 模板
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
    responses:
      200:
        description: 删除成功
      404:
        description: 模板不存在
    """
    success = template_service.delete(template_id)
    if not success:
        return jsonify({"success": False, "error": "Template not found"}), 404
    return jsonify({"success": True, "message": "Template deleted"})
