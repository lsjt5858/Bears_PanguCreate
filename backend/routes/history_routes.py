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
    """
    获取历史记录列表
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: 页码
      - in: query
        name: page_size
        type: integer
        default: 20
        description: 每页数量（最大100）
      - in: query
        name: project_id
        type: integer
        description: 项目ID筛选
      - in: query
        name: search
        type: string
        description: 搜索关键词
      - in: query
        name: format
        type: string
        enum: [json, csv, sql]
        description: 导出格式筛选
      - in: query
        name: start_date
        type: string
        format: date
        description: 开始日期
      - in: query
        name: end_date
        type: string
        format: date
        description: 结束日期
    responses:
      200:
        description: 返回历史记录列表
        schema:
          type: object
          properties:
            data:
              type: array
            pagination:
              type: object
              properties:
                page:
                  type: integer
                page_size:
                  type: integer
                total:
                  type: integer
                total_pages:
                  type: integer
    """
    user = g.current_user
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    page_size = min(page_size, 100)
    
    project_id = request.args.get('project_id', type=int)
    search = request.args.get('search')
    export_format = request.args.get('format')
    
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
    """
    获取单条历史记录详情
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: path
        name: history_id
        type: integer
        required: true
        description: 历史记录ID
    responses:
      200:
        description: 返回历史记录详情
      404:
        description: 记录不存在
    """
    user = g.current_user
    
    history = history_service.get_history(history_id, user_id=user.id)
    if not history:
        return jsonify({'error': '记录不存在或无权访问'}), 404
    
    return jsonify({'data': history.to_dict()})


@history_bp.route('/uuid/<uuid>', methods=['GET'])
@login_required
def get_history_by_uuid(uuid):
    """
    根据UUID获取历史记录
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: path
        name: uuid
        type: string
        required: true
        description: 历史记录UUID
    responses:
      200:
        description: 返回历史记录详情
      404:
        description: 记录不存在
    """
    user = g.current_user
    
    history = history_service.get_history_by_uuid(uuid, user_id=user.id)
    if not history:
        return jsonify({'error': '记录不存在或无权访问'}), 404
    
    return jsonify({'data': history.to_dict()})


@history_bp.route('/<int:history_id>', methods=['DELETE'])
@login_required
def delete_history(history_id):
    """
    删除历史记录
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: path
        name: history_id
        type: integer
        required: true
    responses:
      200:
        description: 删除成功
      400:
        description: 删除失败
    """
    user = g.current_user
    
    success, error = history_service.delete_history(history_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '删除成功'})


@history_bp.route('/batch', methods=['DELETE'])
@login_required
def batch_delete_history():
    """
    批量删除历史记录
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - ids
          properties:
            ids:
              type: array
              items:
                type: integer
              description: 要删除的记录ID列表
    responses:
      200:
        description: 删除结果
    """
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
    """
    获取用户统计信息
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    responses:
      200:
        description: 返回统计信息
    """
    user = g.current_user
    stats = history_service.get_user_stats(user.id)
    return jsonify({'data': stats})


@history_bp.route('/project/<int:project_id>/stats', methods=['GET'])
@login_required
def get_project_stats(project_id):
    """
    获取项目统计信息
    ---
    tags:
      - 历史记录
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
    responses:
      200:
        description: 返回项目统计信息
    """
    stats = history_service.get_project_stats(project_id)
    return jsonify({'data': stats})
