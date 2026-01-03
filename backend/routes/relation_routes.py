"""
关联数据生成路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, g
from middleware.auth import login_required
from services.relation_generator_service import relation_generator_service

relation_bp = Blueprint('relation', __name__, url_prefix='/api/relation')

@relation_bp.route('/generate', methods=['POST'])
@login_required
def generate_relation_data():
    """
    生成关联数据
    Request Body:
    {
        "tables": [{"name": "t1", "count": 10, "fields": [...]}, ...],
        "relations": [{"sourceTable": "t1", ...}, ...]
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    tables = data.get('tables', [])
    relations = data.get('relations', [])
    
    if not tables:
        return jsonify({'error': 'Tables definition is required'}), 400
        
    try:
        result = relation_generator_service.generate_relation_data(tables, relations)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Relation generation error: {e}")
        return jsonify({'error': str(e)}), 500
