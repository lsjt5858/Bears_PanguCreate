"""
数据源模型
管理数据库连接配置
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from datetime import datetime
from extensions import db
from models.base import BaseModel


class DataSource(BaseModel):
    """数据源模型"""
    __tablename__ = 'datasources'
    
    # UUID 用于外部引用
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # 所属用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 所属项目（可选）
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    
    # 基本信息
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # 连接类型: mysql, postgresql, mongodb, restapi
    type = db.Column(db.String(20), nullable=False)
    
    # 连接配置
    host = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    database = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=True)
    
    # 加密存储的密码
    _password = db.Column('password', db.Text, nullable=True)
    
    # REST API 特有配置
    _api_config = db.Column('api_config', db.Text, nullable=True)
    
    # SSL 配置
    use_ssl = db.Column(db.Boolean, default=False)
    _ssl_config = db.Column('ssl_config', db.Text, nullable=True)
    
    # 连接状态
    status = db.Column(db.String(20), default='disconnected')  # connected, disconnected, error
    last_connected_at = db.Column(db.DateTime, nullable=True)
    last_error = db.Column(db.Text, nullable=True)
    
    # 统计
    connection_count = db.Column(db.Integer, default=0)
    query_count = db.Column(db.Integer, default=0)
    
    # 关系
    user = db.relationship('User', backref=db.backref('datasources', lazy='dynamic'))
    project = db.relationship('Project', backref=db.backref('datasources', lazy='dynamic'))
    
    @property
    def password(self):
        """密码不可直接读取"""
        return None
    
    @password.setter
    def password(self, value):
        """设置密码（简单加密存储）"""
        if value:
            # 简单的 base64 编码，生产环境应使用更安全的加密
            import base64
            self._password = base64.b64encode(value.encode()).decode()
        else:
            self._password = None
    
    def get_password(self):
        """获取解密后的密码"""
        if self._password:
            import base64
            return base64.b64decode(self._password.encode()).decode()
        return None
    
    @property
    def api_config(self):
        """获取 API 配置"""
        if self._api_config:
            return json.loads(self._api_config)
        return {}
    
    @api_config.setter
    def api_config(self, value):
        """设置 API 配置"""
        if value:
            self._api_config = json.dumps(value, ensure_ascii=False)
        else:
            self._api_config = None
    
    @property
    def ssl_config(self):
        """获取 SSL 配置"""
        if self._ssl_config:
            return json.loads(self._ssl_config)
        return {}
    
    @ssl_config.setter
    def ssl_config(self, value):
        """设置 SSL 配置"""
        if value:
            self._ssl_config = json.dumps(value, ensure_ascii=False)
        else:
            self._ssl_config = None
    
    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.uuid,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'username': self.username,
            'use_ssl': self.use_ssl,
            'status': self.status,
            'last_connected_at': self.last_connected_at.isoformat() if self.last_connected_at else None,
            'last_error': self.last_error,
            'connection_count': self.connection_count,
            'query_count': self.query_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if self.type == 'restapi':
            data['api_config'] = self.api_config
        
        return data
    
    def update_status(self, status, error=None):
        """更新连接状态"""
        self.status = status
        if status == 'connected':
            self.last_connected_at = datetime.utcnow()
            self.last_error = None
            self.connection_count += 1
        elif status == 'error':
            self.last_error = error
        db.session.commit()
    
    def record_query(self):
        """记录查询次数"""
        self.query_count += 1
        db.session.commit()
    
    @classmethod
    def find_by_uuid(cls, uuid_str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid_str).first()
    
    @classmethod
    def find_by_user(cls, user_id, project_id=None):
        """查找用户的数据源"""
        query = cls.query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        return query.order_by(cls.created_at.desc()).all()
    
    def get_connection_string(self):
        """获取连接字符串"""
        password = self.get_password()
        
        if self.type == 'mysql':
            auth = f"{self.username}:{password}@" if self.username else ""
            return f"mysql+pymysql://{auth}{self.host}:{self.port}/{self.database or ''}"
        
        elif self.type == 'postgresql':
            auth = f"{self.username}:{password}@" if self.username else ""
            return f"postgresql://{auth}{self.host}:{self.port}/{self.database or ''}"
        
        elif self.type == 'mongodb':
            auth = f"{self.username}:{password}@" if self.username else ""
            return f"mongodb://{auth}{self.host}:{self.port}/{self.database or ''}"
        
        elif self.type == 'restapi':
            protocol = 'https' if self.use_ssl else 'http'
            return f"{protocol}://{self.host}:{self.port}"
        
        return None
