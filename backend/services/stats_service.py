"""
统计服务
提供仪表盘和报表所需的统计数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_

from extensions import db
from models import User, Project, GenerationHistory


class StatsService:
    """统计服务"""
    
    def get_dashboard_stats(self, user_id: int = None, project_id: int = None) -> Dict[str, Any]:
        """
        获取仪表盘统计数据
        
        返回:
        - total_generated: 数据生成总量（行数）
        - total_templates: 模板数量
        - total_members: 团队成员数
        - api_calls: API 调用次数（生成次数）
        - generated_this_month: 本月生成量
        - generated_last_month: 上月生成量
        """
        now = datetime.utcnow()
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        
        # 基础查询条件
        base_filter = []
        if user_id:
            base_filter.append(GenerationHistory.user_id == user_id)
        if project_id:
            base_filter.append(GenerationHistory.project_id == project_id)
        
        # 数据生成总量
        total_generated = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).filter(*base_filter).scalar() or 0
        
        # API 调用次数（生成次数）
        api_calls = db.session.query(
            func.count(GenerationHistory.id)
        ).filter(*base_filter).scalar() or 0
        
        # 本月生成量
        this_month_filter = base_filter + [GenerationHistory.created_at >= this_month_start]
        generated_this_month = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).filter(*this_month_filter).scalar() or 0
        
        # 上月生成量
        last_month_filter = base_filter + [
            GenerationHistory.created_at >= last_month_start,
            GenerationHistory.created_at < this_month_start
        ]
        generated_last_month = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).filter(*last_month_filter).scalar() or 0
        
        # 模板数量（从模板服务获取，这里简化处理）
        # TODO: 集成模板服务
        total_templates = 0
        
        # 团队成员数
        if project_id:
            project = Project.query.get(project_id)
            total_members = len(project.members) + 1 if project else 1  # +1 for owner
        else:
            total_members = User.query.filter_by(is_active=True).count()
        
        return {
            'total_generated': int(total_generated),
            'total_templates': total_templates,
            'total_members': total_members,
            'api_calls': api_calls,
            'generated_this_month': int(generated_this_month),
            'generated_last_month': int(generated_last_month)
        }
    
    def get_trend_data(
        self, 
        user_id: int = None, 
        project_id: int = None,
        days: int = 30,
        group_by: str = 'day'  # day, week, month
    ) -> List[Dict[str, Any]]:
        """
        获取生成趋势数据
        
        参数:
        - days: 查询天数
        - group_by: 分组方式 (day/week/month)
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # 基础查询条件
        base_filter = [GenerationHistory.created_at >= start_date]
        if user_id:
            base_filter.append(GenerationHistory.user_id == user_id)
        if project_id:
            base_filter.append(GenerationHistory.project_id == project_id)
        
        # 根据分组方式选择日期格式
        if group_by == 'month':
            date_format = func.strftime('%Y-%m', GenerationHistory.created_at)
        elif group_by == 'week':
            date_format = func.strftime('%Y-%W', GenerationHistory.created_at)
        else:  # day
            date_format = func.date(GenerationHistory.created_at)
        
        # 查询
        results = db.session.query(
            date_format.label('date'),
            func.count(GenerationHistory.id).label('count'),
            func.coalesce(func.sum(GenerationHistory.row_count), 0).label('rows')
        ).filter(*base_filter)\
            .group_by(date_format)\
            .order_by(date_format)\
            .all()
        
        return [
            {
                'date': str(r.date),
                'count': r.count,
                'rows': int(r.rows)
            }
            for r in results
        ]
    
    def get_recent_activities(
        self,
        user_id: int = None,
        project_id: int = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取最近活动"""
        query = db.session.query(GenerationHistory).join(User)
        
        if user_id:
            query = query.filter(GenerationHistory.user_id == user_id)
        if project_id:
            query = query.filter(GenerationHistory.project_id == project_id)
        
        records = query.order_by(desc(GenerationHistory.created_at))\
            .limit(limit).all()
        
        activities = []
        for r in records:
            activities.append({
                'id': str(r.id),
                'user_id': str(r.user_id),
                'user': {
                    'id': str(r.user.id),
                    'name': r.user.nickname or r.user.username,
                    'email': r.user.email,
                    'avatar': r.user.avatar
                },
                'action': '生成数据',
                'target': f"{r.name} ({r.row_count}条)",
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
        
        return activities
    
    def get_format_distribution(
        self,
        user_id: int = None,
        project_id: int = None
    ) -> Dict[str, int]:
        """获取导出格式分布"""
        base_filter = []
        if user_id:
            base_filter.append(GenerationHistory.user_id == user_id)
        if project_id:
            base_filter.append(GenerationHistory.project_id == project_id)
        
        results = db.session.query(
            GenerationHistory.export_format,
            func.count(GenerationHistory.id).label('count')
        ).filter(*base_filter)\
            .group_by(GenerationHistory.export_format)\
            .all()
        
        return {r.export_format or 'json': r.count for r in results}
    
    def get_top_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取生成量最多的用户"""
        results = db.session.query(
            User.id,
            User.username,
            User.nickname,
            User.avatar,
            func.count(GenerationHistory.id).label('generation_count'),
            func.coalesce(func.sum(GenerationHistory.row_count), 0).label('total_rows')
        ).join(GenerationHistory, User.id == GenerationHistory.user_id)\
            .group_by(User.id)\
            .order_by(desc('total_rows'))\
            .limit(limit)\
            .all()
        
        return [
            {
                'id': r.id,
                'username': r.username,
                'nickname': r.nickname,
                'avatar': r.avatar,
                'generation_count': r.generation_count,
                'total_rows': int(r.total_rows)
            }
            for r in results
        ]
    
    def get_project_stats(self, project_id: int) -> Dict[str, Any]:
        """获取项目统计"""
        project = Project.query.get(project_id)
        if not project:
            return None
        
        # 生成统计
        total_generated = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).filter(GenerationHistory.project_id == project_id).scalar() or 0
        
        generation_count = db.session.query(
            func.count(GenerationHistory.id)
        ).filter(GenerationHistory.project_id == project_id).scalar() or 0
        
        return {
            'project': project.to_dict(),
            'total_generated': int(total_generated),
            'generation_count': generation_count,
            'member_count': len(project.members) + 1
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """获取系统总览（管理员用）"""
        total_users = User.query.filter_by(is_active=True).count()
        total_projects = Project.query.filter_by(is_active=True).count()
        
        total_generated = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).scalar() or 0
        
        total_generations = db.session.query(
            func.count(GenerationHistory.id)
        ).scalar() or 0
        
        # 今日统计
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_generated = db.session.query(
            func.coalesce(func.sum(GenerationHistory.row_count), 0)
        ).filter(GenerationHistory.created_at >= today_start).scalar() or 0
        
        today_generations = db.session.query(
            func.count(GenerationHistory.id)
        ).filter(GenerationHistory.created_at >= today_start).scalar() or 0
        
        return {
            'total_users': total_users,
            'total_projects': total_projects,
            'total_generated': int(total_generated),
            'total_generations': total_generations,
            'today_generated': int(today_generated),
            'today_generations': today_generations
        }


# 单例实例
stats_service = StatsService()
