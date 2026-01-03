"""
API 密钥模型
用于管理用户的 API 访问密钥
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import secrets
import hashlib
from datetime import datetime
from extensions import db
from .base import BaseModel


class ApiKey(BaseModel):
    """API 密钥模型"""
    __tablename__ = 'api_keys'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    
    # 密钥信息
    key_prefix = db.Column(db.String(20), nullable=False)  # 密钥前缀，用于显示
    key_hash = db.Column(db.String(64), nullable=False, unique=True)  # 密钥哈希，用于验证
    
    # 关联
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, index=True)
    
    # 权限: read, write, admin (逗号分隔)
    permissions = db.Column(db.String(100), default='read')
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    
    # 统计
    call_count = db.Column(db.Integer, default=0)
    last_used_at = db.Column(db.DateTime)
    last_used_ip = db.Column(db.String(50))
    
    # 过期时间
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    user = db.relationship('User', backref=db.backref('api_keys', lazy='dynamic'))
    project = db.relationship('Project', backref=db.backref('api_keys', lazy='dynamic'))
    
    @property
    def permission_list(self) -> list:
        """获取权限列表"""
        return [p.strip() for p in self.permissions.split(',') if p.strip()]
    
    @permission_list.setter
    def permission_list(self, value: list):
        """设置权限列表"""
        self.permissions = ','.join(value)
    
    @property
    def is_expired(self) -> bool:
        """检查是否过期"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """检查密钥是否有效"""
        return self.is_active and not self.is_expired
    
    def has_permission(self, permission: str) -> bool:
        """检查是否有指定权限"""
        perms = self.permission_list
        if 'admin' in perms:
            return True
        return permission in perms
    
    def record_usage(self, ip_address: str = None):
        """记录使用"""
        self.call_count += 1
        self.last_used_at = datetime.utcnow()
        if ip_address:
            self.last_used_ip = ip_address
        db.session.commit()
    
    def to_dict(self, include_key: bool = False) -> dict:
        """转换为字典"""
        data = {
            'id': self.uuid,
            'name': self.name,
            'key_prefix': self.key_prefix,
            'permissions': self.permission_list,
            'is_active': self.is_active,
            'call_count': self.call_count,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_expired': self.is_expired,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        return data
    
    @classmethod
    def generate_key(cls) -> tuple:
        """
        生成新的 API 密钥
        返回: (完整密钥, 密钥前缀, 密钥哈希)
        """
        # 生成随机密钥
        random_part = secrets.token_hex(16)
        full_key = f"df_{random_part}"
        
        # 前缀用于显示
        key_prefix = full_key[:12]
        
        # 哈希用于存储和验证
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()
        
        return full_key, key_prefix, key_hash
    
    @classmethod
    def verify_key(cls, key: str) -> 'ApiKey':
        """验证 API 密钥"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        api_key = cls.query.filter_by(key_hash=key_hash).first()
        
        if api_key and api_key.is_valid:
            return api_key
        return None
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def find_by_user(cls, user_id: int, include_inactive: bool = False):
        """查找用户的所有密钥"""
        query = cls.query.filter_by(user_id=user_id)
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.order_by(cls.created_at.desc()).all()
    
    def __repr__(self):
        return f'<ApiKey {self.name}>'


class ApiKeyUsageLog(BaseModel):
    """API 密钥使用日志"""
    __tablename__ = 'api_key_usage_logs'
    
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_keys.id'), nullable=False, index=True)
    endpoint = db.Column(db.String(200))  # 访问的端点
    method = db.Column(db.String(10))  # HTTP 方法
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    status_code = db.Column(db.Integer)  # 响应状态码
    response_time_ms = db.Column(db.Integer)  # 响应时间
    
    api_key = db.relationship('ApiKey', backref=db.backref('usage_logs', lazy='dynamic'))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'method': self.method,
            'ip_address': self.ip_address,
            'status_code': self.status_code,
            'response_time_ms': self.response_time_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
