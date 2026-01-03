"""
历史记录服务
管理数据生成历史
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import json
from typing import Optional, List, Tuple
from datetime import datetime, timedelta

from extensions import db
from models import User, Project
from models.history import GenerationHistory


class HistoryService:
    """历史记录服务"""
    
    def create_history(
        self,
        user_id: int,
        fields: list,
        row_count: int,
        name: str = None,
        project_id: int = None,
        template_id: str = None,
        export_format: str = 'json',
        table_name: str = None,
        execution_time_ms: int = None,
        data_size_bytes: int = None
    ) -> GenerationHistory:
        """创建历史记录"""
        history = GenerationHistory(
            user_id=user_id,
            project_id=project_id,
            template_id=template_id,
            name=name or f"生成 {row_count} 条数据",
            row_count=row_count,
            export_format=export_format,
            table_name=table_name,
            execution_time_ms=execution_time_ms,
            data_size_bytes=data_size_bytes,
            status='completed'
        )
        history.fields = fields
        history.save()
        
        # 更新项目统计
        if project_id:
            project = Project.query.get(project_id)
            if project:
                project.increment_generation(row_count)
        
        return history
    
    def get_history(self, history_id: int, user_id: int = None) -> Optional[GenerationHistory]:
        """获取单条历史记录"""
        history = GenerationHistory.query.get(history_id)
        if not history:
            return None
        
        # 权限检查
        if user_id and history.user_id != user_id:
            return None
        
        return history
    
    def get_history_by_uuid(self, uuid: str, user_id: int = None) -> Optional[GenerationHistory]:
        """根据 UUID 获取历史记录"""
        history = GenerationHistory.find_by_uuid(uuid)
        if not history:
            return None
        
        if user_id and history.user_id != user_id:
            return None
        
        return history
    
    def list_history(
        self,
        user_id: int = None,
        project_id: int = None,
        page: int = 1,
        page_size: int = 20,
        search: str = None,
        export_format: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> Tuple[List[GenerationHistory], int]:
        """
        获取历史记录列表
        返回: (记录列表, 总数)
        """
        query = GenerationHistory.query
        
        # 用户过滤
        if user_id:
            query = query.filter(GenerationHistory.user_id == user_id)
        
        # 项目过滤
        if project_id:
            query = query.filter(GenerationHistory.project_id == project_id)
        
        # 搜索
        if search:
            query = query.filter(GenerationHistory.name.ilike(f'%{search}%'))
        
        # 格式过滤
        if export_format:
            query = query.filter(GenerationHistory.export_format == export_format)
        
        # 日期范围
        if start_date:
            query = query.filter(GenerationHistory.created_at >= start_date)
        if end_date:
            query = query.filter(GenerationHistory.created_at <= end_date)
        
        # 总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        records = query.order_by(GenerationHistory.created_at.desc())\
            .limit(page_size).offset(offset).all()
        
        return records, total
    
    def delete_history(self, history_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        删除历史记录
        返回: (成功, 错误信息)
        """
        history = GenerationHistory.query.get(history_id)
        if not history:
            return False, "记录不存在"
        
        if history.user_id != user_id:
            return False, "无权删除此记录"
        
        history.delete()
        return True, None
    
    def batch_delete(self, history_ids: List[int], user_id: int) -> Tuple[int, int]:
        """
        批量删除历史记录
        返回: (成功数, 失败数)
        """
        success = 0
        failed = 0
        
        for history_id in history_ids:
            ok, _ = self.delete_history(history_id, user_id)
            if ok:
                success += 1
            else:
                failed += 1
        
        return success, failed
    
    def get_user_stats(self, user_id: int) -> dict:
        """获取用户统计信息"""
        total_count = GenerationHistory.count_by_user(user_id)
        
        # 总生成行数
        total_rows = db.session.query(db.func.sum(GenerationHistory.row_count))\
            .filter(GenerationHistory.user_id == user_id).scalar() or 0
        
        # 按格式统计
        format_stats = db.session.query(
            GenerationHistory.export_format,
            db.func.count(GenerationHistory.id)
        ).filter(GenerationHistory.user_id == user_id)\
            .group_by(GenerationHistory.export_format).all()
        
        # 最近 7 天统计
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_count = GenerationHistory.query\
            .filter(GenerationHistory.user_id == user_id)\
            .filter(GenerationHistory.created_at >= week_ago).count()
        
        # 最近 7 天每日统计
        daily_stats = db.session.query(
            db.func.date(GenerationHistory.created_at).label('date'),
            db.func.count(GenerationHistory.id).label('count'),
            db.func.sum(GenerationHistory.row_count).label('rows')
        ).filter(GenerationHistory.user_id == user_id)\
            .filter(GenerationHistory.created_at >= week_ago)\
            .group_by(db.func.date(GenerationHistory.created_at))\
            .order_by(db.func.date(GenerationHistory.created_at)).all()
        
        return {
            'total_count': total_count,
            'total_rows': int(total_rows),
            'recent_count': recent_count,
            'format_stats': {fmt: cnt for fmt, cnt in format_stats},
            'daily_stats': [
                {'date': str(d.date), 'count': d.count, 'rows': int(d.rows or 0)}
                for d in daily_stats
            ]
        }
    
    def get_project_stats(self, project_id: int) -> dict:
        """获取项目统计信息"""
        total_count = GenerationHistory.count_by_project(project_id)
        
        total_rows = db.session.query(db.func.sum(GenerationHistory.row_count))\
            .filter(GenerationHistory.project_id == project_id).scalar() or 0
        
        return {
            'total_count': total_count,
            'total_rows': int(total_rows)
        }


# 单例实例
history_service = HistoryService()
