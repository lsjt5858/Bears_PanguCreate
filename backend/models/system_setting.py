"""
系统设置模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from extensions import db
from .base import BaseModel


class SystemSetting(BaseModel):
    """系统设置模型"""
    __tablename__ = 'system_settings'
    
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(20), default='string')  # string, integer, boolean, json
    category = db.Column(db.String(50), default='general', index=True)
    description = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=False)  # 是否对普通用户可见
    
    def get_value(self):
        """获取类型化的值"""
        if self.value is None:
            return None
        
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes')
        elif self.value_type == 'json':
            try:
                return json.loads(self.value)
            except:
                return self.value
        else:
            return self.value
    
    def set_value(self, value):
        """设置值"""
        if self.value_type == 'json' and isinstance(value, (dict, list)):
            self.value = json.dumps(value, ensure_ascii=False)
        elif self.value_type == 'boolean':
            self.value = 'true' if value else 'false'
        else:
            self.value = str(value) if value is not None else None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.get_value(),
            'value_type': self.value_type,
            'category': self.category,
            'description': self.description,
            'is_public': self.is_public,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_key(cls, key: str):
        """根据键获取设置"""
        return cls.query.filter_by(key=key).first()
    
    @classmethod
    def get_by_category(cls, category: str, public_only: bool = False):
        """根据分类获取设置"""
        query = cls.query.filter_by(category=category)
        if public_only:
            query = query.filter_by(is_public=True)
        return query.all()
    
    @classmethod
    def get_all_public(cls):
        """获取所有公开设置"""
        return cls.query.filter_by(is_public=True).all()
    
    @classmethod
    def set_setting(cls, key: str, value, value_type: str = 'string',
                    category: str = 'general', description: str = None,
                    is_public: bool = False):
        """设置或更新配置"""
        setting = cls.get_by_key(key)
        if setting:
            setting.value_type = value_type
            setting.set_value(value)
            setting.category = category
            if description:
                setting.description = description
            setting.is_public = is_public
            setting.updated_at = datetime.utcnow()
            db.session.commit()
        else:
            setting = cls(
                key=key,
                value_type=value_type,
                category=category,
                description=description,
                is_public=is_public
            )
            setting.set_value(value)
            setting.save()
        return setting
    
    def __repr__(self):
        return f'<SystemSetting {self.key}>'
