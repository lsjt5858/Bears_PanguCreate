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
    """
    获取仪表盘统计数据
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: query
        name: project_id
        type: integer
        description: 项目ID（可选）
    responses:
      200:
        description: 返回仪表盘数据
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                total_generated:
                  type: integer
                  description: 总生成量
                total_templates:
                  type: integer
                  description: 模板数量
                total_members:
                  type: integer
                  description: 团队成员数
                api_calls:
                  type: integer
                  description: API调用次数
                generated_this_month:
                  type: integer
                  description: 本月生成量
                generated_last_month:
                  type: integer
                  description: 上月生成量
    """
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    
    stats = stats_service.get_dashboard_stats(
        user_id=user.id,
        project_id=project_id
    )
    
    return jsonify({'data': stats})


@stats_bp.route('/trend', methods=['GET'])
@login_required
def get_trend():
    """
    获取生成趋势数据
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: query
        name: project_id
        type: integer
        description: 项目ID
      - in: query
        name: days
        type: integer
        default: 30
        description: 查询天数（最大365）
      - in: query
        name: group_by
        type: string
        enum: [day, week, month]
        default: day
        description: 分组方式
    responses:
      200:
        description: 返回趋势数据
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                  count:
                    type: integer
                  rows:
                    type: integer
    """
    user = g.current_user
    project_id = request.args.get('project_id', type=int)
    days = request.args.get('days', 30, type=int)
    group_by = request.args.get('group_by', 'day')
    
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
    """
    获取最近活动
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: query
        name: project_id
        type: integer
        description: 项目ID
      - in: query
        name: limit
        type: integer
        default: 10
        description: 返回数量（最大50）
    responses:
      200:
        description: 返回最近活动列表
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  user_id:
                    type: integer
                  user:
                    type: object
                  action:
                    type: string
                  target:
                    type: string
                  created_at:
                    type: string
    """
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
    """
    获取导出格式分布
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: query
        name: project_id
        type: integer
        description: 项目ID
    responses:
      200:
        description: 返回格式分布数据
    """
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
    """
    获取项目统计
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
    responses:
      200:
        description: 返回项目统计数据
      404:
        description: 项目不存在
    """
    stats = stats_service.get_project_stats(project_id)
    
    if not stats:
        return jsonify({'error': '项目不存在'}), 404
    
    return jsonify({'data': stats})


@stats_bp.route('/overview', methods=['GET'])
@admin_required
def get_system_overview():
    """
    获取系统总览（管理员）
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    responses:
      200:
        description: 返回系统总览数据
      403:
        description: 需要管理员权限
    """
    overview = stats_service.get_system_overview()
    return jsonify({'data': overview})


@stats_bp.route('/top-users', methods=['GET'])
@admin_required
def get_top_users():
    """
    获取生成量最多的用户（管理员）
    ---
    tags:
      - 统计
    security:
      - Bearer: []
    parameters:
      - in: query
        name: limit
        type: integer
        default: 10
        description: 返回数量（最大100）
    responses:
      200:
        description: 返回用户排行
      403:
        description: 需要管理员权限
    """
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 100)
    
    users = stats_service.get_top_users(limit=limit)
    return jsonify({'data': users})


@stats_bp.route('/public', methods=['GET'])
def get_public_stats():
    """
    获取公开统计数据
    ---
    tags:
      - 统计
    responses:
      200:
        description: 返回公开统计数据
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                total_users:
                  type: integer
                total_generated:
                  type: integer
    """
    overview = stats_service.get_system_overview()
    
    return jsonify({
        'data': {
            'total_users': overview['total_users'],
            'total_generated': overview['total_generated']
        }
    })
