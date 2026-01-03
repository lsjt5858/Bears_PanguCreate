"""
用户模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from .base import BaseModel


class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # 个人资料
    nickname = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    
    # 状态
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login_at = db.Column(db.DateTime)
    
    # 关联
    projects = db.relationship('Project', backref='owner', lazy='dynamic', foreign_keys='Project.owner_id')
    
    def set_password(self, password: str):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_email: bool = False) -> dict:
        """转换为字典"""
        data = {
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'nickname': self.nickname or self.username,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        if include_email:
            data['email'] = self.email
        return data
    
    @classmethod
    def find_by_username(cls, username: str):
        """根据用户名查找"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email: str):
        """根据邮箱查找"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    def __repr__(self):
        return f'<User {self.username}>'
