"""
项目模型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from extensions import db
from .base import BaseModel


# 项目成员关联表
project_members = db.Table(
    'project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role', db.String(20), default='member'),  # owner, admin, member
    db.Column('joined_at', db.DateTime, default=db.func.now())
)


class Project(BaseModel):
    """项目模型"""
    __tablename__ = 'projects'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # 所有者
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 状态
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # 统计
    generation_count = db.Column(db.Integer, default=0)
    template_count = db.Column(db.Integer, default=0)
    
    # 成员关系
    members = db.relationship(
        'User',
        secondary=project_members,
        lazy='dynamic',
        backref=db.backref('member_projects', lazy='dynamic')
    )
    
    def add_member(self, user, role: str = 'member'):
        """添加成员"""
        if not self.is_member(user):
            stmt = project_members.insert().values(
                project_id=self.id,
                user_id=user.id,
                role=role
            )
            db.session.execute(stmt)
            db.session.commit()
    
    def remove_member(self, user):
        """移除成员"""
        if self.is_member(user):
            stmt = project_members.delete().where(
                db.and_(
                    project_members.c.project_id == self.id,
                    project_members.c.user_id == user.id
                )
            )
            db.session.execute(stmt)
            db.session.commit()
    
    def is_member(self, user) -> bool:
        """检查是否为成员"""
        return self.members.filter(project_members.c.user_id == user.id).count() > 0
    
    def get_member_role(self, user) -> str:
        """获取成员角色"""
        result = db.session.execute(
            db.select(project_members.c.role).where(
                db.and_(
                    project_members.c.project_id == self.id,
                    project_members.c.user_id == user.id
                )
            )
        ).first()
        return result[0] if result else None
    
    def increment_generation(self, count: int = 1):
        """增加生成次数"""
        self.generation_count += count
        db.session.commit()
    
    def to_dict(self, include_members: bool = False) -> dict:
        """转换为字典"""
        data = {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'is_active': self.is_active,
            'generation_count': self.generation_count,
            'template_count': self.template_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_members:
            data['members'] = [m.to_dict() for m in self.members.all()]
        return data
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def find_by_owner(cls, owner_id: int):
        """查找用户拥有的项目"""
        return cls.query.filter_by(owner_id=owner_id, is_active=True).all()
    
    def __repr__(self):
        return f'<Project {self.name}>'
