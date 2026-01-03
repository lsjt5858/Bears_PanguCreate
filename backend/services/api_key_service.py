"""
API 密钥服务
管理 API 密钥的创建、验证、统计等功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc

from extensions import db
from models.api_key import ApiKey, ApiKeyUsageLog


class ApiKeyService:
    """API 密钥服务"""
    
    def create_key(
        self,
        user_id: int,
        name: str,
        permissions: List[str] = None,
        project_id: int = None,
        expires_at: datetime = None
    ) -> Tuple[ApiKey, str]:
        """
        创建 API 密钥
        返回: (ApiKey 对象, 完整密钥)
        注意: 完整密钥只在创建时返回一次，之后无法获取
        """
        if permissions is None:
            permissions = ['read']
        
        # 验证权限
        valid_permissions = {'read', 'write', 'admin'}
        permissions = [p for p in permissions if p in valid_permissions]
        if not permissions:
            permissions = ['read']
        
        # 生成密钥
        full_key, key_prefix, key_hash = ApiKey.generate_key()
        
        # 创建记录
        api_key = ApiKey(
            user_id=user_id,
            project_id=project_id,
            name=name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            expires_at=expires_at
        )
        api_key.permission_list = permissions
        api_key.save()
        
        return api_key, full_key
    
    def get_key(self, key_id: str, user_id: int) -> Optional[ApiKey]:
        """获取密钥详情"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key or api_key.user_id != user_id:
            return None
        return api_key
    
    def list_keys(
        self,
        user_id: int,
        project_id: int = None,
        include_inactive: bool = False
    ) -> List[ApiKey]:
        """获取用户的密钥列表"""
        query = ApiKey.query.filter_by(user_id=user_id)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if not include_inactive:
            query = query.filter_by(is_active=True)
        
        return query.order_by(desc(ApiKey.created_at)).all()
    
    def update_key(
        self,
        key_id: str,
        user_id: int,
        **kwargs
    ) -> Tuple[Optional[ApiKey], Optional[str]]:
        """更新密钥"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key:
            return None, "密钥不存在"
        
        if api_key.user_id != user_id:
            return None, "无权修改此密钥"
        
        if 'name' in kwargs:
            api_key.name = kwargs['name']
        
        if 'permissions' in kwargs:
            valid_permissions = {'read', 'write', 'admin'}
            permissions = [p for p in kwargs['permissions'] if p in valid_permissions]
            if permissions:
                api_key.permission_list = permissions
        
        if 'is_active' in kwargs:
            api_key.is_active = kwargs['is_active']
        
        if 'expires_at' in kwargs:
            api_key.expires_at = kwargs['expires_at']
        
        api_key.save()
        return api_key, None
    
    def delete_key(self, key_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """删除密钥"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key:
            return False, "密钥不存在"
        
        if api_key.user_id != user_id:
            return False, "无权删除此密钥"
        
        api_key.delete()
        return True, None
    
    def revoke_key(self, key_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """撤销密钥（软删除）"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key:
            return False, "密钥不存在"
        
        if api_key.user_id != user_id:
            return False, "无权撤销此密钥"
        
        api_key.is_active = False
        api_key.save()
        return True, None
    
    def verify_key(self, key: str) -> Optional[ApiKey]:
        """验证 API 密钥"""
        return ApiKey.verify_key(key)
    
    def record_usage(
        self,
        api_key: ApiKey,
        endpoint: str,
        method: str,
        ip_address: str = None,
        user_agent: str = None,
        status_code: int = None,
        response_time_ms: int = None
    ):
        """记录 API 使用"""
        # 更新密钥统计
        api_key.record_usage(ip_address)
        
        # 记录详细日志
        log = ApiKeyUsageLog(
            api_key_id=api_key.id,
            endpoint=endpoint,
            method=method,
            ip_address=ip_address,
            user_agent=user_agent[:500] if user_agent else None,
            status_code=status_code,
            response_time_ms=response_time_ms
        )
        log.save()
    
    def get_usage_stats(
        self,
        key_id: str,
        user_id: int,
        days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """获取密钥使用统计"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key or api_key.user_id != user_id:
            return None
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # 每日调用统计
        daily_stats = db.session.query(
            func.date(ApiKeyUsageLog.created_at).label('date'),
            func.count(ApiKeyUsageLog.id).label('count')
        ).filter(
            ApiKeyUsageLog.api_key_id == api_key.id,
            ApiKeyUsageLog.created_at >= start_date
        ).group_by(func.date(ApiKeyUsageLog.created_at))\
            .order_by(func.date(ApiKeyUsageLog.created_at)).all()
        
        # 端点统计
        endpoint_stats = db.session.query(
            ApiKeyUsageLog.endpoint,
            func.count(ApiKeyUsageLog.id).label('count')
        ).filter(
            ApiKeyUsageLog.api_key_id == api_key.id,
            ApiKeyUsageLog.created_at >= start_date
        ).group_by(ApiKeyUsageLog.endpoint)\
            .order_by(desc('count')).limit(10).all()
        
        # 平均响应时间
        avg_response_time = db.session.query(
            func.avg(ApiKeyUsageLog.response_time_ms)
        ).filter(
            ApiKeyUsageLog.api_key_id == api_key.id,
            ApiKeyUsageLog.created_at >= start_date,
            ApiKeyUsageLog.response_time_ms.isnot(None)
        ).scalar() or 0
        
        return {
            'total_calls': api_key.call_count,
            'daily_stats': [
                {'date': str(d.date), 'count': d.count}
                for d in daily_stats
            ],
            'endpoint_stats': [
                {'endpoint': e.endpoint, 'count': e.count}
                for e in endpoint_stats
            ],
            'avg_response_time_ms': round(avg_response_time, 2)
        }
    
    def get_usage_logs(
        self,
        key_id: str,
        user_id: int,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[Dict], int]:
        """获取使用日志"""
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key or api_key.user_id != user_id:
            return [], 0
        
        query = ApiKeyUsageLog.query.filter_by(api_key_id=api_key.id)
        total = query.count()
        
        offset = (page - 1) * page_size
        logs = query.order_by(desc(ApiKeyUsageLog.created_at))\
            .limit(page_size).offset(offset).all()
        
        return [log.to_dict() for log in logs], total
    
    def regenerate_key(
        self,
        key_id: str,
        user_id: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        重新生成密钥
        返回: (新的完整密钥, 错误信息)
        """
        api_key = ApiKey.find_by_uuid(key_id)
        if not api_key:
            return None, "密钥不存在"
        
        if api_key.user_id != user_id:
            return None, "无权操作此密钥"
        
        # 生成新密钥
        full_key, key_prefix, key_hash = ApiKey.generate_key()
        
        # 更新记录
        api_key.key_prefix = key_prefix
        api_key.key_hash = key_hash
        api_key.save()
        
        return full_key, None


# 单例实例
api_key_service = ApiKeyService()
