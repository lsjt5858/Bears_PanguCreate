"""
导出路由
"""
from flask import Blueprint, jsonify, request, Response

from services import export_service

export_bp = Blueprint('export', __name__, url_prefix='/api')


@export_bp.route('/export/json', methods=['POST'])
def export_json():
    """
    导出为JSON格式
    ---
    tags:
      - 导出
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - data
          properties:
            data:
              type: array
              description: 要导出的数据
              items:
                type: object
            fields:
              type: array
              description: 字段配置
              items:
                type: object
    responses:
      200:
        description: 返回JSON文件
        content:
          application/json:
            schema:
              type: string
              format: binary
      400:
        description: 无数据可导出
    """
    data = request.get_json()
    records = data.get("data", [])
    fields = data.get("fields", [])
    
    if not records:
        return jsonify({"success": False, "error": "No data to export"}), 400
    
    content = export_service.to_json(records, fields)
    
    return Response(
        content,
        mimetype='application/json',
        headers={
            'Content-Disposition': 'attachment; filename=generated_data.json'
        }
    )


@export_bp.route('/export/csv', methods=['POST'])
def export_csv():
    """
    导出为CSV格式
    ---
    tags:
      - 导出
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - data
          properties:
            data:
              type: array
              description: 要导出的数据
            fields:
              type: array
              description: 字段配置
    responses:
      200:
        description: 返回CSV文件
        content:
          text/csv:
            schema:
              type: string
              format: binary
      400:
        description: 无数据可导出
    """
    data = request.get_json()
    records = data.get("data", [])
    fields = data.get("fields", [])
    
    if not records:
        return jsonify({"success": False, "error": "No data to export"}), 400
    
    content = export_service.to_csv(records, fields)
    
    return Response(
        content,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=generated_data.csv',
            'Content-Type': 'text/csv; charset=utf-8'
        }
    )


@export_bp.route('/export/sql', methods=['POST'])
def export_sql():
    """
    导出为SQL格式
    ---
    tags:
      - 导出
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - data
          properties:
            data:
              type: array
              description: 要导出的数据
            fields:
              type: array
              description: 字段配置
            tableName:
              type: string
              description: 表名
              default: test_data
    responses:
      200:
        description: 返回SQL文件
        content:
          text/plain:
            schema:
              type: string
              format: binary
      400:
        description: 无数据可导出
    """
    data = request.get_json()
    records = data.get("data", [])
    fields = data.get("fields", [])
    table_name = data.get("tableName", "test_data")
    
    if not records:
        return jsonify({"success": False, "error": "No data to export"}), 400
    
    content = export_service.to_sql(records, fields, table_name)
    
    return Response(
        content,
        mimetype='text/plain',
        headers={
            'Content-Disposition': 'attachment; filename=generated_data.sql',
            'Content-Type': 'text/plain; charset=utf-8'
        }
    )
