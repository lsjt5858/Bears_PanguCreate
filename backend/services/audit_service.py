"""
审计日志服务
记录系统操作日志
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Tuple, Any
from datetime import datetime, timedelta
from flask import request, g
from models.audit_log import AuditLog
from extensions import db


class AuditService:
    """审计日志服务类"""
    
    # 操作类型
    ACTIONS = {
        'create': '创建',
        'update': '更新',
        'delete': '删除',
        'login': '登录',
        'logout': '登出',
        'export': '导出',
        'import': '导入',
        'generate': '生成数据',
        'execute': '执行',
        'test': '测试',
        'view': '查看'
    }
    
    # 资源类型
    RESOURCE_TYPES = {
        'user': '用户',
        'template': '模板',
        'datasource': '数据源',
        'api_key': 'API密钥',
        'scheduled_task': '定时任务',
        'webhook': 'Webhook',
        'data': '数据',
        'system': '系统'
    }
    
    def get_actions(self) -> dict:
        """获取操作类型"""
        return self.ACTIONS
    
    def get_resource_types(self) -> dict:
        """获取资源类型"""
        return self.RESOURCE_TYPES
    
    def _get_request_info(self) -> dict:
        """获取请求信息"""
        try:
            return {
                'ip_address': request.remote_addr,
                'user_agent': request.user_agent.string[:500] if request.user_agent else None,
                'request_method': request.method,
                'request_path': request.path
            }
        except:
            return {}
    
    def _get_current_user_id(self) -> Optional[int]:
        """获取当前用户ID"""
        try:
            if hasattr(g, 'current_user') and g.current_user:
                return g.current_user.id
        except:
            pass
        return None
    
    def log(
        self,
        action: str,
        resource_type: str,
        resource_id: str = None,
        resource_name: str = None,
        description: str = None,
        old_value: dict = None,
        new_value: dict = None,
        user_id: int = None,
        status: str = 'success',
        error_message: str = None
    ) -> AuditLog:
        """记录审计日志"""
        if user_id is None:
            user_id = self._get_current_user_id()
        
        request_info = self._get_request_info()
        
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            description=description,
            status=status,
            error_message=error_message,
            **request_info
        )
        
        if old_value:
            log.set_old_value(old_value)
        if new_value:
            log.set_new_value(new_value)
        
        log.save()
        return log
    
    def log_create(self, resource_type: str, resource_id: str, 
                   resource_name: str = None, new_value: dict = None, **kwargs):
        """记录创建操作"""
        return self.log(
            action='create',
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            description=f'创建{self.RESOURCE_TYPES.get(resource_type, resource_type)}: {resource_name or resource_id}',
            new_value=new_value,
            **kwargs
        )
    
    def log_update(self, resource_type: str, resource_id: str,
                   resource_name: str = None, old_value: dict = None, 
                   new_value: dict = None, **kwargs):
        """记录更新操作"""
        return self.log(
            action='update',
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            description=f'更新{self.RESOURCE_TYPES.get(resource_type, resource_type)}: {resource_name or resource_id}',
            old_value=old_value,
            new_value=new_value,
            **kwargs
        )
    
    def log_delete(self, resource_type: str, resource_id: str,
                   resource_name: str = None, old_value: dict = None, **kwargs):
        """记录删除操作"""
        return self.log(
            action='delete',
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            description=f'删除{self.RESOURCE_TYPES.get(resource_type, resource_type)}: {resource_name or resource_id}',
            old_value=old_value,
            **kwargs
        )
    
    def log_login(self, user_id: int, username: str, success: bool = True, 
                  error: str = None):
        """记录登录操作"""
        return self.log(
            action='login',
            resource_type='user',
            resource_id=str(user_id) if user_id else None,
            resource_name=username,
            description=f'用户登录: {username}',
            user_id=user_id,
            status='success' if success else 'failed',
            error_message=error
        )
    
    def log_logout(self, user_id: int, username: str):
        """记录登出操作"""
        return self.log(
            action='logout',
            resource_type='user',
            resource_id=str(user_id),
            resource_name=username,
            description=f'用户登出: {username}',
            user_id=user_id
        )
    
    def log_export(self, resource_type: str, format: str, count: int, **kwargs):
        """记录导出操作"""
        return self.log(
            action='export',
            resource_type=resource_type,
            description=f'导出{self.RESOURCE_TYPES.get(resource_type, resource_type)}数据，格式: {format}，数量: {count}',
            **kwargs
        )
    
    def log_generate(self, template_name: str = None, count: int = 0, **kwargs):
        """记录数据生成操作"""
        return self.log(
            action='generate',
            resource_type='data',
            resource_name=template_name,
            description=f'生成测试数据，模板: {template_name or "自定义"}，数量: {count}',
            **kwargs
        )
    
    def get_logs(
        self,
        user_id: int = None,
        action: str = None,
        resource_type: str = None,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[AuditLog], int]:
        """获取审计日志列表"""
        start_dt = None
        end_dt = None
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except:
                pass
        
        return AuditLog.get_logs(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            start_date=start_dt,
            end_date=end_dt,
            page=page,
            page_size=page_size
        )
    
    def get_log(self, log_id: str) -> Optional[AuditLog]:
        """获取单条审计日志"""
        return AuditLog.find_by_uuid(log_id)
    
    def get_user_activity_summary(self, user_id: int, days: int = 7) -> dict:
        """获取用户活动摘要"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = AuditLog.query.filter(
            AuditLog.user_id == user_id,
            AuditLog.created_at >= start_date
        ).all()
        
        # 按操作类型统计
        action_counts = {}
        for log in logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1
        
        # 按资源类型统计
        resource_counts = {}
        for log in logs:
            resource_counts[log.resource_type] = resource_counts.get(log.resource_type, 0) + 1
        
        # 按日期统计
        daily_counts = {}
        for log in logs:
            date_str = log.created_at.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        return {
            'total': len(logs),
            'action_counts': action_counts,
            'resource_counts': resource_counts,
            'daily_counts': daily_counts,
            'period_days': days
        }
    
    def get_system_activity_summary(self, days: int = 7) -> dict:
        """获取系统活动摘要"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = AuditLog.query.filter(
            AuditLog.created_at >= start_date
        ).all()
        
        # 按操作类型统计
        action_counts = {}
        for log in logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1
        
        # 按用户统计
        user_counts = {}
        for log in logs:
            if log.user_id:
                user_counts[log.user_id] = user_counts.get(log.user_id, 0) + 1
        
        # 成功/失败统计
        status_counts = {'success': 0, 'failed': 0}
        for log in logs:
            status_counts[log.status] = status_counts.get(log.status, 0) + 1
        
        return {
            'total': len(logs),
            'action_counts': action_counts,
            'active_users': len(user_counts),
            'status_counts': status_counts,
            'period_days': days
        }


# 单例
audit_service = AuditService()
