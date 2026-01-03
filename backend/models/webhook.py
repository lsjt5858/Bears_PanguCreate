"""
Webhook 模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from datetime import datetime
from extensions import db
from .base import BaseModel


class Webhook(BaseModel):
    """Webhook 配置模型"""
    __tablename__ = 'webhooks'
    
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 基本信息
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    
    # 触发事件: task_completed, task_failed, data_generated, datasource_connected, etc.
    events = db.Column(db.Text, nullable=False, default='[]')
    
    # 请求配置
    method = db.Column(db.String(10), default='POST')  # POST, GET
    headers = db.Column(db.Text, default='{}')  # JSON 格式的自定义请求头
    secret = db.Column(db.String(100))  # 用于签名验证
    
    # 状态
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_triggered_at = db.Column(db.DateTime)
    last_status = db.Column(db.String(20))  # success, failed
    last_error = db.Column(db.Text)
    
    # 统计
    trigger_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    fail_count = db.Column(db.Integer, default=0)
    
    # 关联
    user = db.relationship('User', backref=db.backref('webhooks', lazy='dynamic'))
    
    def get_events(self) -> list:
        """获取事件列表"""
        try:
            return json.loads(self.events) if self.events else []
        except:
            return []
    
    def set_events(self, events: list):
        """设置事件列表"""
        self.events = json.dumps(events)
    
    def get_headers(self) -> dict:
        """获取自定义请求头"""
        try:
            return json.loads(self.headers) if self.headers else {}
        except:
            return {}
    
    def set_headers(self, headers: dict):
        """设置自定义请求头"""
        self.headers = json.dumps(headers)
    
    def record_trigger(self, success: bool, error: str = None):
        """记录触发结果"""
        self.last_triggered_at = datetime.utcnow()
        self.trigger_count += 1
        if success:
            self.last_status = 'success'
            self.success_count += 1
            self.last_error = None
        else:
            self.last_status = 'failed'
            self.fail_count += 1
            self.last_error = error
        db.session.commit()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.uuid,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'events': self.get_events(),
            'method': self.method,
            'headers': self.get_headers(),
            'is_active': self.is_active,
            'last_triggered_at': self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            'last_status': self.last_status,
            'last_error': self.last_error,
            'trigger_count': self.trigger_count,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def get_active_webhooks_for_event(cls, user_id: int, event: str):
        """获取用户针对特定事件的活跃 Webhook"""
        webhooks = cls.query.filter_by(user_id=user_id, is_active=True).all()
        return [w for w in webhooks if event in w.get_events()]
    
    def __repr__(self):
        return f'<Webhook {self.name}>'
