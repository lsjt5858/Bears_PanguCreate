"""
定时任务模型
管理数据生成的定时任务
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from datetime import datetime
from extensions import db
from .base import BaseModel


class ScheduledTask(BaseModel):
    """定时任务模型"""
    __tablename__ = 'scheduled_tasks'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # 关联
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, index=True)
    template_id = db.Column(db.String(36), nullable=True)  # 关联的模板 UUID
    
    # 调度配置
    cron_expression = db.Column(db.String(100), nullable=False)  # Cron 表达式
    timezone = db.Column(db.String(50), default='Asia/Shanghai')
    
    # 生成配置
    fields_config = db.Column(db.Text, nullable=False)  # JSON: 字段配置
    row_count = db.Column(db.Integer, nullable=False, default=100)
    export_format = db.Column(db.String(20), default='json')  # json, csv, sql
    table_name = db.Column(db.String(100))  # SQL 导出时的表名
    
    # 输出配置
    output_type = db.Column(db.String(20), default='none')  # none, webhook, email, storage
    output_config = db.Column(db.Text)  # JSON: 输出配置
    
    # 状态
    status = db.Column(db.String(20), default='active', index=True)  # active, paused, error, completed
    is_enabled = db.Column(db.Boolean, default=True)
    
    # 执行统计
    run_count = db.Column(db.Integer, default=0)  # 执行次数
    success_count = db.Column(db.Integer, default=0)  # 成功次数
    fail_count = db.Column(db.Integer, default=0)  # 失败次数
    last_run_at = db.Column(db.DateTime)  # 上次执行时间
    last_run_status = db.Column(db.String(20))  # success, failed
    last_error = db.Column(db.Text)  # 最后一次错误信息
    next_run_at = db.Column(db.DateTime)  # 下次执行时间
    
    # 限制
    max_runs = db.Column(db.Integer)  # 最大执行次数，null 表示无限
    expires_at = db.Column(db.DateTime)  # 过期时间
    
    # 关系
    user = db.relationship('User', backref=db.backref('scheduled_tasks', lazy='dynamic'))
    project = db.relationship('Project', backref=db.backref('scheduled_tasks', lazy='dynamic'))
    
    @property
    def fields(self) -> list:
        """获取字段配置"""
        try:
            return json.loads(self.fields_config) if self.fields_config else []
        except:
            return []
    
    @fields.setter
    def fields(self, value: list):
        """设置字段配置"""
        self.fields_config = json.dumps(value, ensure_ascii=False)
    
    @property
    def output_settings(self) -> dict:
        """获取输出配置"""
        try:
            return json.loads(self.output_config) if self.output_config else {}
        except:
            return {}
    
    @output_settings.setter
    def output_settings(self, value: dict):
        """设置输出配置"""
        self.output_config = json.dumps(value, ensure_ascii=False)
    
    @property
    def is_active(self) -> bool:
        """检查任务是否活跃"""
        if not self.is_enabled:
            return False
        if self.status != 'active':
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        if self.max_runs and self.run_count >= self.max_runs:
            return False
        return True
    
    def to_dict(self, include_fields: bool = True) -> dict:
        """转换为字典"""
        data = {
            'id': self.uuid,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'template_id': self.template_id,
            'cron_expression': self.cron_expression,
            'timezone': self.timezone,
            'row_count': self.row_count,
            'export_format': self.export_format,
            'table_name': self.table_name,
            'output_type': self.output_type,
            'status': self.status,
            'is_enabled': self.is_enabled,
            'is_active': self.is_active,
            'run_count': self.run_count,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'last_run_status': self.last_run_status,
            'last_error': self.last_error,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None,
            'max_runs': self.max_runs,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_fields:
            data['fields'] = self.fields
            data['output_config'] = self.output_settings
        
        return data
    
    def record_run(self, success: bool, error: str = None):
        """记录执行结果"""
        self.run_count += 1
        self.last_run_at = datetime.utcnow()
        
        if success:
            self.success_count += 1
            self.last_run_status = 'success'
            self.last_error = None
        else:
            self.fail_count += 1
            self.last_run_status = 'failed'
            self.last_error = error
        
        # 检查是否达到最大执行次数
        if self.max_runs and self.run_count >= self.max_runs:
            self.status = 'completed'
        
        db.session.commit()
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def find_active_tasks(cls):
        """查找所有活跃任务"""
        return cls.query.filter_by(is_enabled=True, status='active').all()
    
    def __repr__(self):
        return f'<ScheduledTask {self.name}>'


class TaskExecutionLog(BaseModel):
    """任务执行日志"""
    __tablename__ = 'task_execution_logs'
    
    task_id = db.Column(db.Integer, db.ForeignKey('scheduled_tasks.id'), nullable=False, index=True)
    
    # 执行信息
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)  # 执行耗时
    
    # 结果
    status = db.Column(db.String(20), nullable=False)  # success, failed
    rows_generated = db.Column(db.Integer)  # 生成的行数
    data_size_bytes = db.Column(db.Integer)  # 数据大小
    error_message = db.Column(db.Text)
    
    # 输出
    output_status = db.Column(db.String(20))  # 输出状态
    output_message = db.Column(db.Text)
    
    task = db.relationship('ScheduledTask', backref=db.backref('execution_logs', lazy='dynamic'))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'task_id': self.task_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'duration_ms': self.duration_ms,
            'status': self.status,
            'rows_generated': self.rows_generated,
            'data_size_bytes': self.data_size_bytes,
            'error_message': self.error_message,
            'output_status': self.output_status,
            'output_message': self.output_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
