"""
历史记录路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g
from datetime import datetime

from middleware import login_required
from services.history_service import history_service

history_bp = Blueprint('history', __name__, url_prefix='/api/history')


@history_bp.route('', methods=['GET'])
@login_required
def list_history():
    """获取历史记录列表"""
    user = g.current_user
    
    # 分页参数
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    page_size = min(page_size, 100)  # 最大 100 条
    
    # 过滤参数
    project_id = request.args.get('project_id', type=int)
    search = request.args.get('search')
    export_format = request.args.get('format')
    
    # 日期范围
    start_date = None
    end_date = None
    if request.args.get('start_date'):
        try:
            start_date = datetime.fromisoformat(request.args.get('start_date'))
        except:
            pass
    if request.args.get('end_date'):
        try:
            end_date = datetime.fromisoformat(request.args.get('end_date'))
        except:
            pass
    
    records, total = history_service.list_history(
        user_id=user.id,
        project_id=project_id,
        page=page,
        page_size=page_size,
        search=search,
        export_format=export_format,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'data': [r.to_dict(include_fields=True) for r in records],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@history_bp.route('/<int:history_id>', methods=['GET'])
@login_required
def get_history(history_id):
    """获取单条历史记录详情"""
    user = g.current_user
    
    history = history_service.get_history(history_id, user_id=user.id)
    if not history:
        return jsonify({'error': '记录不存在或无权访问'}), 404
    
    return jsonify({'data': history.to_dict()})


@history_bp.route('/uuid/<uuid>', methods=['GET'])
@login_required
def get_history_by_uuid(uuid):
    """根据 UUID 获取历史记录"""
    user = g.current_user
    
    history = history_service.get_history_by_uuid(uuid, user_id=user.id)
    if not history:
        return jsonify({'error': '记录不存在或无权访问'}), 404
    
    return jsonify({'data': history.to_dict()})


@history_bp.route('/<int:history_id>', methods=['DELETE'])
@login_required
def delete_history(history_id):
    """删除历史记录"""
    user = g.current_user
    
    success, error = history_service.delete_history(history_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '删除成功'})


@history_bp.route('/batch', methods=['DELETE'])
@login_required
def batch_delete_history():
    """批量删除历史记录"""
    user = g.current_user
    data = request.get_json()
    
    if not data or 'ids' not in data:
        return jsonify({'error': '请提供要删除的记录 ID 列表'}), 400
    
    ids = data.get('ids', [])
    if not isinstance(ids, list) or not ids:
        return jsonify({'error': '无效的 ID 列表'}), 400
    
    success, failed = history_service.batch_delete(ids, user.id)
    
    return jsonify({
        'message': f'成功删除 {success} 条记录',
        'success': success,
        'failed': failed
    })


@history_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """获取用户统计信息"""
    user = g.current_user
    stats = history_service.get_user_stats(user.id)
    return jsonify({'data': stats})


@history_bp.route('/project/<int:project_id>/stats', methods=['GET'])
@login_required
def get_project_stats(project_id):
    """获取项目统计信息"""
    # TODO: 添加项目权限检查
    stats = history_service.get_project_stats(project_id)
    return jsonify({'data': stats})
