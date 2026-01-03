"""
数据库模型基类
提供通用字段和方法
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from extensions import db


class BaseModel(db.Model):
    """所有数据库模型的基类"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def save(self):
        """保存当前对象到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除当前对象"""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        """转换为字典，子类应重写此方法"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_id(cls, id):
        """根据 ID 获取记录"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """获取所有记录"""
        return cls.query.all()
    
    @classmethod
    def create(cls, **kwargs):
        """创建新记录"""
        instance = cls(**kwargs)
        return instance.save()
