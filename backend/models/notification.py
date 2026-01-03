"""
通知模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime
from extensions import db
from .base import BaseModel


class Notification(BaseModel):
    """通知模型"""
    __tablename__ = 'notifications'
    
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 通知类型: info, success, warning, error, system
    type = db.Column(db.String(20), nullable=False, default='info')
    
    # 通知内容
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    
    # 关联资源
    resource_type = db.Column(db.String(50))  # task, template, datasource, etc.
    resource_id = db.Column(db.String(36))
    
    # 状态
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    read_at = db.Column(db.DateTime)
    
    # 关联
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.uuid,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def get_user_notifications(cls, user_id: int, unread_only: bool = False, 
                                page: int = 1, page_size: int = 20):
        """获取用户通知列表"""
        query = cls.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        query = query.order_by(cls.created_at.desc())
        
        total = query.count()
        notifications = query.offset((page - 1) * page_size).limit(page_size).all()
        return notifications, total
    
    @classmethod
    def get_unread_count(cls, user_id: int) -> int:
        """获取未读通知数量"""
        return cls.query.filter_by(user_id=user_id, is_read=False).count()
    
    @classmethod
    def mark_all_as_read(cls, user_id: int):
        """标记所有通知为已读"""
        cls.query.filter_by(user_id=user_id, is_read=False).update({
            'is_read': True,
            'read_at': datetime.utcnow()
        })
        db.session.commit()
    
    def __repr__(self):
        return f'<Notification {self.uuid}>'
