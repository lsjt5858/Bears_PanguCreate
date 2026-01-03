"""
审计日志模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from datetime import datetime
from extensions import db
from .base import BaseModel


class AuditLog(BaseModel):
    """审计日志模型"""
    __tablename__ = 'audit_logs'
    
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # 操作信息
    action = db.Column(db.String(50), nullable=False, index=True)  # create, update, delete, login, etc.
    resource_type = db.Column(db.String(50), nullable=False, index=True)  # user, template, datasource, etc.
    resource_id = db.Column(db.String(36))
    resource_name = db.Column(db.String(200))
    
    # 详细信息
    description = db.Column(db.Text)
    old_value = db.Column(db.Text)  # JSON 格式的旧值
    new_value = db.Column(db.Text)  # JSON 格式的新值
    
    # 请求信息
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    request_method = db.Column(db.String(10))
    request_path = db.Column(db.String(500))
    
    # 结果
    status = db.Column(db.String(20), default='success')  # success, failed
    error_message = db.Column(db.Text)
    
    # 关联
    user = db.relationship('User', backref=db.backref('audit_logs', lazy='dynamic'))
    
    def set_old_value(self, value: dict):
        """设置旧值"""
        self.old_value = json.dumps(value, ensure_ascii=False) if value else None
    
    def set_new_value(self, value: dict):
        """设置新值"""
        self.new_value = json.dumps(value, ensure_ascii=False) if value else None
    
    def get_old_value(self) -> dict:
        """获取旧值"""
        try:
            return json.loads(self.old_value) if self.old_value else None
        except:
            return None
    
    def get_new_value(self) -> dict:
        """获取新值"""
        try:
            return json.loads(self.new_value) if self.new_value else None
        except:
            return None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.uuid,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'description': self.description,
            'old_value': self.get_old_value(),
            'new_value': self.get_new_value(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'request_method': self.request_method,
            'request_path': self.request_path,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def get_logs(cls, user_id: int = None, action: str = None, 
                 resource_type: str = None, start_date: datetime = None,
                 end_date: datetime = None, page: int = 1, page_size: int = 20):
        """获取审计日志列表"""
        query = cls.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if action:
            query = query.filter_by(action=action)
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if start_date:
            query = query.filter(cls.created_at >= start_date)
        if end_date:
            query = query.filter(cls.created_at <= end_date)
        
        query = query.order_by(cls.created_at.desc())
        
        total = query.count()
        logs = query.offset((page - 1) * page_size).limit(page_size).all()
        return logs, total
    
    def __repr__(self):
        return f'<AuditLog {self.action} {self.resource_type}>'
