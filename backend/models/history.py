"""
历史记录模型
记录数据生成历史
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from extensions import db
from .base import BaseModel


class GenerationHistory(BaseModel):
    """数据生成历史记录"""
    __tablename__ = 'generation_history'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, default='未命名生成')
    
    # 关联
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, index=True)
    template_id = db.Column(db.String(36), nullable=True)  # 使用的模板 ID
    
    # 生成配置
    fields_config = db.Column(db.Text, nullable=False)  # JSON: 字段配置
    row_count = db.Column(db.Integer, nullable=False, default=10)
    
    # 导出信息
    export_format = db.Column(db.String(20), default='json')  # json, csv, sql
    table_name = db.Column(db.String(100))  # SQL 导出时的表名
    
    # 状态
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    error_message = db.Column(db.Text)
    
    # 统计
    execution_time_ms = db.Column(db.Integer)  # 执行耗时（毫秒）
    data_size_bytes = db.Column(db.Integer)  # 数据大小（字节）
    
    # 关系
    user = db.relationship('User', backref=db.backref('generation_history', lazy='dynamic'))
    project = db.relationship('Project', backref=db.backref('generation_history', lazy='dynamic'))
    
    @property
    def fields(self) -> list:
        """获取字段配置列表"""
        try:
            return json.loads(self.fields_config) if self.fields_config else []
        except:
            return []
    
    @fields.setter
    def fields(self, value: list):
        """设置字段配置"""
        self.fields_config = json.dumps(value, ensure_ascii=False)
    
    def to_dict(self, include_fields: bool = True) -> dict:
        """转换为字典"""
        data = {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'template_id': self.template_id,
            'row_count': self.row_count,
            'export_format': self.export_format,
            'table_name': self.table_name,
            'status': self.status,
            'error_message': self.error_message,
            'execution_time_ms': self.execution_time_ms,
            'data_size_bytes': self.data_size_bytes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_fields:
            data['fields'] = self.fields
        return data
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def find_by_user(cls, user_id: int, limit: int = 50, offset: int = 0):
        """查找用户的历史记录"""
        return cls.query.filter_by(user_id=user_id)\
            .order_by(cls.created_at.desc())\
            .limit(limit).offset(offset).all()
    
    @classmethod
    def find_by_project(cls, project_id: int, limit: int = 50, offset: int = 0):
        """查找项目的历史记录"""
        return cls.query.filter_by(project_id=project_id)\
            .order_by(cls.created_at.desc())\
            .limit(limit).offset(offset).all()
    
    @classmethod
    def count_by_user(cls, user_id: int) -> int:
        """统计用户的历史记录数"""
        return cls.query.filter_by(user_id=user_id).count()
    
    @classmethod
    def count_by_project(cls, project_id: int) -> int:
        """统计项目的历史记录数"""
        return cls.query.filter_by(project_id=project_id).count()
    
    def __repr__(self):
        return f'<GenerationHistory {self.uuid}>'
