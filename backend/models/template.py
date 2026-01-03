"""
模板模型
支持模板市场功能：评分、下载统计、收藏、标签
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
from datetime import datetime
from extensions import db
from .base import BaseModel


# 模板标签关联表
template_tags = db.Table(
    'template_tags',
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Tag(BaseModel):
    """标签模型"""
    __tablename__ = 'tags'
    
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    usage_count = db.Column(db.Integer, default=0)  # 使用次数
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'usage_count': self.usage_count
        }
    
    @classmethod
    def get_or_create(cls, name: str) -> 'Tag':
        """获取或创建标签"""
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = cls(name=name)
            tag.save()
        return tag
    
    @classmethod
    def get_popular(cls, limit: int = 20) -> list:
        """获取热门标签"""
        return cls.query.order_by(cls.usage_count.desc()).limit(limit).all()


class Template(BaseModel):
    """模板模型"""
    __tablename__ = 'templates'
    
    # 基本信息
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='other', index=True)
    
    # 字段配置 (JSON)
    fields_config = db.Column(db.Text, nullable=False, default='[]')
    
    # 作者信息
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 可见性
    is_public = db.Column(db.Boolean, default=True)  # 是否公开到市场
    is_official = db.Column(db.Boolean, default=False)  # 是否官方模板
    
    # 统计数据
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)  # 平均评分
    rating_count = db.Column(db.Integer, default=0)  # 评分人数
    rating_sum = db.Column(db.Integer, default=0)  # 评分总和（用于计算平均分）
    favorite_count = db.Column(db.Integer, default=0)  # 收藏数
    
    # 关系
    author = db.relationship('User', backref=db.backref('templates', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=template_tags, backref=db.backref('templates', lazy='dynamic'))
    
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
    
    def to_dict(self, include_author: bool = True, include_fields: bool = True) -> dict:
        """转换为字典"""
        data = {
            'id': self.uuid,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'is_public': self.is_public,
            'is_official': self.is_official,
            'downloads': self.downloads,
            'rating': round(self.rating, 1),
            'rating_count': self.rating_count,
            'favorite_count': self.favorite_count,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_author and self.author:
            data['author'] = {
                'id': self.author.uuid,
                'name': self.author.nickname or self.author.username,
                'avatar': self.author.avatar
            }
        
        if include_fields:
            data['fields'] = self.fields
        
        return data
    
    def increment_downloads(self):
        """增加下载次数"""
        self.downloads += 1
        db.session.commit()
    
    def add_rating(self, score: int):
        """添加评分"""
        if score < 1 or score > 5:
            raise ValueError("评分必须在 1-5 之间")
        
        self.rating_sum += score
        self.rating_count += 1
        self.rating = self.rating_sum / self.rating_count
        db.session.commit()
    
    def update_rating(self, old_score: int, new_score: int):
        """更新评分"""
        if new_score < 1 or new_score > 5:
            raise ValueError("评分必须在 1-5 之间")
        
        self.rating_sum = self.rating_sum - old_score + new_score
        self.rating = self.rating_sum / self.rating_count if self.rating_count > 0 else 0
        db.session.commit()
    
    def set_tags(self, tag_names: list):
        """设置标签"""
        # 清除旧标签
        for tag in self.tags:
            tag.usage_count = max(0, tag.usage_count - 1)
        self.tags.clear()
        
        # 添加新标签
        for name in tag_names[:10]:  # 最多 10 个标签
            tag = Tag.get_or_create(name.strip())
            tag.usage_count += 1
            self.tags.append(tag)
        
        db.session.commit()
    
    @classmethod
    def find_by_uuid(cls, uuid: str):
        """根据 UUID 查找"""
        return cls.query.filter_by(uuid=uuid).first()
    
    @classmethod
    def search(cls, keyword: str, limit: int = 20):
        """搜索模板"""
        return cls.query.filter(
            cls.is_public == True,
            db.or_(
                cls.name.ilike(f'%{keyword}%'),
                cls.description.ilike(f'%{keyword}%')
            )
        ).order_by(cls.downloads.desc()).limit(limit).all()


class TemplateRating(BaseModel):
    """模板评分记录"""
    __tablename__ = 'template_ratings'
    
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)  # 1-5 分
    comment = db.Column(db.Text)  # 评论（可选）
    
    # 唯一约束：每个用户对每个模板只能评分一次
    __table_args__ = (
        db.UniqueConstraint('template_id', 'user_id', name='unique_template_user_rating'),
    )
    
    template = db.relationship('Template', backref=db.backref('ratings', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('template_ratings', lazy='dynamic'))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'template_id': self.template_id,
            'user_id': self.user_id,
            'score': self.score,
            'comment': self.comment,
            'user': {
                'name': self.user.nickname or self.user.username,
                'avatar': self.user.avatar
            } if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TemplateFavorite(BaseModel):
    """模板收藏"""
    __tablename__ = 'template_favorites'
    
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    __table_args__ = (
        db.UniqueConstraint('template_id', 'user_id', name='unique_template_user_favorite'),
    )
    
    template = db.relationship('Template', backref=db.backref('favorites', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('favorite_templates', lazy='dynamic'))


class TemplateDownload(BaseModel):
    """模板下载记录"""
    __tablename__ = 'template_downloads'
    
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)  # 可为空（匿名下载）
    ip_address = db.Column(db.String(50))
    
    template = db.relationship('Template', backref=db.backref('download_records', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('template_downloads', lazy='dynamic'))
