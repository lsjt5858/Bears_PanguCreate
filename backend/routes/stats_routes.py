"""
统计路由
提供仪表盘和报表 API
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g

from middleware import login_required, admin_required, optional_auth
from services.stats_service import stats_service

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@stats_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    """获取仪表盘统计数据"""
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    
    # 获取统计数据
    stats = stats_service.get_dashboard_stats(
        user_id=user.id,
        project_id=project_id
    )
    
    return jsonify({'data': stats})


@stats_bp.route('/trend', methods=['GET'])
@login_required
def get_trend():
    """获取生成趋势数据"""
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    days = request.args.get('days', 30, type=int)
    group_by = request.args.get('group_by', 'day')
    
    # 限制查询范围
    days = min(days, 365)
    if group_by not in ['day', 'week', 'month']:
        group_by = 'day'
    
    trend_data = stats_service.get_trend_data(
        user_id=user.id,
        project_id=project_id,
        days=days,
        group_by=group_by
    )
    
    return jsonify({'data': trend_data})


@stats_bp.route('/activities', methods=['GET'])
@login_required
def get_activities():
    """获取最近活动"""
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)
    
    activities = stats_service.get_recent_activities(
        user_id=user.id,
        project_id=project_id,
        limit=limit
    )
    
    return jsonify({'data': activities})


@stats_bp.route('/format-distribution', methods=['GET'])
@login_required
def get_format_distribution():
    """获取导出格式分布"""
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    
    distribution = stats_service.get_format_distribution(
        user_id=user.id,
        project_id=project_id
    )
    
    return jsonify({'data': distribution})


@stats_bp.route('/project/<int:project_id>', methods=['GET'])
@login_required
def get_project_stats(project_id):
    """获取项目统计"""
    # TODO: 添加项目权限检查
    stats = stats_service.get_project_stats(project_id)
    
    if not stats:
        return jsonify({'error': '项目不存在'}), 404
    
    return jsonify({'data': stats})


@stats_bp.route('/overview', methods=['GET'])
@admin_required
def get_system_overview():
    """获取系统总览（管理员）"""
    overview = stats_service.get_system_overview()
    return jsonify({'data': overview})


@stats_bp.route('/top-users', methods=['GET'])
@admin_required
def get_top_users():
    """获取生成量最多的用户（管理员）"""
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 100)
    
    users = stats_service.get_top_users(limit=limit)
    return jsonify({'data': users})


# 公开统计端点（无需登录）
@stats_bp.route('/public', methods=['GET'])
def get_public_stats():
    """获取公开统计数据"""
    overview = stats_service.get_system_overview()
    
    # 只返回部分公开数据
    return jsonify({
        'data': {
            'total_users': overview['total_users'],
            'total_generated': overview['total_generated']
        }
    })
