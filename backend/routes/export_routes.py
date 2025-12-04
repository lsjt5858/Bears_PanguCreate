"""
导出路由
"""
from flask import Blueprint, jsonify, request, Response

from services import export_service

export_bp = Blueprint('export', __name__, url_prefix='/api')


@export_bp.route('/export/json', methods=['POST'])
def export_json():
    """导出为JSON格式"""
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
    """导出为CSV格式"""
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
    """导出为SQL格式"""
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
