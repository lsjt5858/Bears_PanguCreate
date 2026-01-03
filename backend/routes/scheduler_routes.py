"""
定时任务路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g
from datetime import datetime

from middleware import login_required
from services.scheduler_service import scheduler_service

scheduler_bp = Blueprint('scheduler', __name__, url_prefix='/api/scheduled-tasks')


@scheduler_bp.route('', methods=['GET'])
@login_required
def list_tasks():
    """获取定时任务列表"""
    user = g.current_user
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    page_size = min(page_size, 50)
    
    project_id = request.args.get('project_id', type=int)
    status = request.args.get('status')
    
    tasks, total = scheduler_service.list_tasks(
        user_id=user.id,
        project_id=project_id,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'data': [t.to_dict(include_fields=False) for t in tasks],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@scheduler_bp.route('/<task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """获取任务详情"""
    user = g.current_user
    
    task = scheduler_service.get_task(task_id, user.id)
    if not task:
        return jsonify({'error': '任务不存在或无权访问'}), 404
    
    return jsonify({'data': task.to_dict()})


@scheduler_bp.route('', methods=['POST'])
@login_required
def create_task():
    """创建定时任务"""
    user = g.current_user
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('name'):
        return jsonify({'error': '任务名称不能为空'}), 400
    
    if not data.get('cron_expression'):
        return jsonify({'error': 'Cron 表达式不能为空'}), 400
    
    if not data.get('fields'):
        return jsonify({'error': '字段配置不能为空'}), 400
    
    # 解析过期时间
    expires_at = None
    if data.get('expires_at'):
        try:
            expires_at = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': '无效的过期时间格式'}), 400
    
    task, error = scheduler_service.create_task(
        user_id=user.id,
        name=data['name'],
        cron_expression=data['cron_expression'],
        fields=data['fields'],
        row_count=data.get('row_count', 100),
        description=data.get('description'),
        project_id=data.get('project_id'),
        template_id=data.get('template_id'),
        export_format=data.get('export_format', 'json'),
        table_name=data.get('table_name'),
        output_type=data.get('output_type', 'none'),
        output_config=data.get('output_config'),
        timezone=data.get('timezone', 'Asia/Shanghai'),
        max_runs=data.get('max_runs'),
        expires_at=expires_at
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '任务创建成功',
        'data': task.to_dict()
    }), 201


@scheduler_bp.route('/<task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """更新任务"""
    user = g.current_user
    data = request.get_json()
    
    # 解析过期时间
    if 'expires_at' in data and data['expires_at']:
        try:
            data['expires_at'] = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': '无效的过期时间格式'}), 400
    
    task, error = scheduler_service.update_task(
        task_id=task_id,
        user_id=user.id,
        **data
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '任务更新成功',
        'data': task.to_dict()
    })


@scheduler_bp.route('/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """删除任务"""
    user = g.current_user
    
    success, error = scheduler_service.delete_task(task_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '任务删除成功'})


@scheduler_bp.route('/<task_id>/pause', methods=['POST'])
@login_required
def pause_task(task_id):
    """暂停任务"""
    user = g.current_user
    
    success, error = scheduler_service.pause_task(task_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '任务已暂停'})


@scheduler_bp.route('/<task_id>/resume', methods=['POST'])
@login_required
def resume_task(task_id):
    """恢复任务"""
    user = g.current_user
    
    success, error = scheduler_service.resume_task(task_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '任务已恢复'})


@scheduler_bp.route('/<task_id>/run', methods=['POST'])
@login_required
def run_task_now(task_id):
    """立即执行任务"""
    user = g.current_user
    
    success, error = scheduler_service.run_task_now(task_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': '任务已触发执行'})


@scheduler_bp.route('/<task_id>/logs', methods=['GET'])
@login_required
def get_task_logs(task_id):
    """获取任务执行日志"""
    user = g.current_user
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    page_size = min(page_size, 100)
    
    logs, total = scheduler_service.get_execution_logs(
        task_id=task_id,
        user_id=user.id,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'data': logs,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@scheduler_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """获取任务统计"""
    user = g.current_user
    stats = scheduler_service.get_task_stats(user.id)
    return jsonify({'data': stats})


@scheduler_bp.route('/cron/parse', methods=['POST'])
@login_required
def parse_cron():
    """解析 Cron 表达式"""
    data = request.get_json()
    expression = data.get('expression')
    
    if not expression:
        return jsonify({'error': '请提供 Cron 表达式'}), 400
    
    description = scheduler_service.parse_cron_description(expression)
    next_runs = scheduler_service.get_next_runs(expression, count=5)
    
    if not next_runs:
        return jsonify({'error': '无效的 Cron 表达式'}), 400
    
    return jsonify({
        'data': {
            'expression': expression,
            'description': description,
            'next_runs': next_runs
        }
    })


@scheduler_bp.route('/cron/presets', methods=['GET'])
def get_cron_presets():
    """获取常用 Cron 预设"""
    presets = [
        {'expression': '* * * * *', 'name': '每分钟', 'description': '每分钟执行一次'},
        {'expression': '*/5 * * * *', 'name': '每5分钟', 'description': '每5分钟执行一次'},
        {'expression': '*/15 * * * *', 'name': '每15分钟', 'description': '每15分钟执行一次'},
        {'expression': '*/30 * * * *', 'name': '每30分钟', 'description': '每30分钟执行一次'},
        {'expression': '0 * * * *', 'name': '每小时', 'description': '每小时整点执行'},
        {'expression': '0 */2 * * *', 'name': '每2小时', 'description': '每2小时执行一次'},
        {'expression': '0 */6 * * *', 'name': '每6小时', 'description': '每6小时执行一次'},
        {'expression': '0 0 * * *', 'name': '每天午夜', 'description': '每天 00:00 执行'},
        {'expression': '0 8 * * *', 'name': '每天早8点', 'description': '每天 08:00 执行'},
        {'expression': '0 12 * * *', 'name': '每天中午', 'description': '每天 12:00 执行'},
        {'expression': '0 18 * * *', 'name': '每天晚6点', 'description': '每天 18:00 执行'},
        {'expression': '0 0 * * 1', 'name': '每周一', 'description': '每周一 00:00 执行'},
        {'expression': '0 0 * * 1-5', 'name': '工作日', 'description': '周一至周五 00:00 执行'},
        {'expression': '0 0 1 * *', 'name': '每月1日', 'description': '每月1日 00:00 执行'},
        {'expression': '0 0 1 1 *', 'name': '每年1月1日', 'description': '每年1月1日 00:00 执行'},
    ]
    
    return jsonify({'data': presets})
