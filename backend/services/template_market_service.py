"""
模板市场服务
管理模板市场的评分、下载、收藏等功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_, or_

from extensions import db
from models.template import Template, Tag, TemplateRating, TemplateFavorite, TemplateDownload


class TemplateMarketService:
    """模板市场服务"""
    
    def create_template(
        self,
        author_id: int,
        name: str,
        description: str = None,
        category: str = 'other',
        fields: list = None,
        tags: list = None,
        is_public: bool = True
    ) -> Template:
        """创建模板"""
        template = Template(
            author_id=author_id,
            name=name,
            description=description,
            category=category,
            is_public=is_public
        )
        template.fields = fields or []
        template.save()
        
        if tags:
            template.set_tags(tags)
        
        return template
    
    def update_template(
        self,
        template_id: str,
        user_id: int,
        **kwargs
    ) -> Tuple[Optional[Template], Optional[str]]:
        """更新模板"""
        template = Template.find_by_uuid(template_id)
        if not template:
            return None, "模板不存在"
        
        if template.author_id != user_id:
            return None, "无权修改此模板"
        
        # 更新字段
        if 'name' in kwargs:
            template.name = kwargs['name']
        if 'description' in kwargs:
            template.description = kwargs['description']
        if 'category' in kwargs:
            template.category = kwargs['category']
        if 'fields' in kwargs:
            template.fields = kwargs['fields']
        if 'is_public' in kwargs:
            template.is_public = kwargs['is_public']
        if 'tags' in kwargs:
            template.set_tags(kwargs['tags'])
        
        template.save()
        return template, None
    
    def delete_template(self, template_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """删除模板"""
        template = Template.find_by_uuid(template_id)
        if not template:
            return False, "模板不存在"
        
        if template.author_id != user_id:
            return False, "无权删除此模板"
        
        template.delete()
        return True, None
    
    def get_template(self, template_id: str, user_id: int = None) -> Optional[Dict[str, Any]]:
        """获取模板详情"""
        template = Template.find_by_uuid(template_id)
        if not template:
            return None
        
        data = template.to_dict()
        
        # 如果用户已登录，添加用户相关信息
        if user_id:
            # 是否已收藏
            favorite = TemplateFavorite.query.filter_by(
                template_id=template.id,
                user_id=user_id
            ).first()
            data['is_favorite'] = favorite is not None
            
            # 用户的评分
            rating = TemplateRating.query.filter_by(
                template_id=template.id,
                user_id=user_id
            ).first()
            data['user_rating'] = rating.score if rating else None
        
        return data
    
    def list_templates(
        self,
        page: int = 1,
        page_size: int = 20,
        category: str = None,
        search: str = None,
        tags: List[str] = None,
        sort_by: str = 'downloads',  # downloads, rating, created_at
        author_id: int = None,
        is_public: bool = True,
        user_id: int = None  # 当前用户，用于获取收藏状态
    ) -> Tuple[List[Dict], int]:
        """获取模板列表"""
        query = Template.query
        
        # 公开/私有过滤
        if is_public is not None:
            query = query.filter(Template.is_public == is_public)
        
        # 分类过滤
        if category and category != 'all':
            query = query.filter(Template.category == category)
        
        # 作者过滤
        if author_id:
            query = query.filter(Template.author_id == author_id)
        
        # 搜索
        if search:
            query = query.filter(
                or_(
                    Template.name.ilike(f'%{search}%'),
                    Template.description.ilike(f'%{search}%')
                )
            )
        
        # 标签过滤
        if tags:
            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if tag:
                    query = query.filter(Template.tags.contains(tag))
        
        # 排序
        if sort_by == 'rating':
            query = query.order_by(desc(Template.rating), desc(Template.rating_count))
        elif sort_by == 'created_at':
            query = query.order_by(desc(Template.created_at))
        elif sort_by == 'favorites':
            query = query.order_by(desc(Template.favorite_count))
        else:  # downloads
            query = query.order_by(desc(Template.downloads))
        
        # 总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        templates = query.limit(page_size).offset(offset).all()
        
        # 获取用户收藏状态
        favorite_ids = set()
        if user_id:
            favorites = TemplateFavorite.query.filter(
                TemplateFavorite.user_id == user_id,
                TemplateFavorite.template_id.in_([t.id for t in templates])
            ).all()
            favorite_ids = {f.template_id for f in favorites}
        
        # 转换为字典
        result = []
        for t in templates:
            data = t.to_dict(include_fields=False)
            data['is_favorite'] = t.id in favorite_ids
            result.append(data)
        
        return result, total
    
    def use_template(
        self,
        template_id: str,
        user_id: int = None,
        ip_address: str = None
    ) -> Optional[Template]:
        """使用模板（记录下载）"""
        template = Template.find_by_uuid(template_id)
        if not template:
            return None
        
        # 记录下载
        download = TemplateDownload(
            template_id=template.id,
            user_id=user_id,
            ip_address=ip_address
        )
        download.save()
        
        # 增加下载次数
        template.increment_downloads()
        
        return template
    
    def rate_template(
        self,
        template_id: str,
        user_id: int,
        score: int,
        comment: str = None
    ) -> Tuple[Optional[TemplateRating], Optional[str]]:
        """评分模板"""
        if score < 1 or score > 5:
            return None, "评分必须在 1-5 之间"
        
        template = Template.find_by_uuid(template_id)
        if not template:
            return None, "模板不存在"
        
        # 检查是否已评分
        existing = TemplateRating.query.filter_by(
            template_id=template.id,
            user_id=user_id
        ).first()
        
        if existing:
            # 更新评分
            old_score = existing.score
            existing.score = score
            existing.comment = comment
            existing.save()
            template.update_rating(old_score, score)
            return existing, None
        else:
            # 新评分
            rating = TemplateRating(
                template_id=template.id,
                user_id=user_id,
                score=score,
                comment=comment
            )
            rating.save()
            template.add_rating(score)
            return rating, None
    
    def get_template_ratings(
        self,
        template_id: str,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Dict], int]:
        """获取模板评分列表"""
        template = Template.find_by_uuid(template_id)
        if not template:
            return [], 0
        
        query = TemplateRating.query.filter_by(template_id=template.id)
        total = query.count()
        
        offset = (page - 1) * page_size
        ratings = query.order_by(desc(TemplateRating.created_at))\
            .limit(page_size).offset(offset).all()
        
        return [r.to_dict() for r in ratings], total
    
    def toggle_favorite(
        self,
        template_id: str,
        user_id: int
    ) -> Tuple[bool, bool]:
        """
        切换收藏状态
        返回: (成功, 是否已收藏)
        """
        template = Template.find_by_uuid(template_id)
        if not template:
            return False, False
        
        existing = TemplateFavorite.query.filter_by(
            template_id=template.id,
            user_id=user_id
        ).first()
        
        if existing:
            # 取消收藏
            existing.delete()
            template.favorite_count = max(0, template.favorite_count - 1)
            db.session.commit()
            return True, False
        else:
            # 添加收藏
            favorite = TemplateFavorite(
                template_id=template.id,
                user_id=user_id
            )
            favorite.save()
            template.favorite_count += 1
            db.session.commit()
            return True, True
    
    def get_user_favorites(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Dict], int]:
        """获取用户收藏的模板"""
        query = Template.query.join(TemplateFavorite).filter(
            TemplateFavorite.user_id == user_id
        )
        
        total = query.count()
        offset = (page - 1) * page_size
        templates = query.order_by(desc(TemplateFavorite.created_at))\
            .limit(page_size).offset(offset).all()
        
        return [t.to_dict(include_fields=False) for t in templates], total
    
    def get_popular_tags(self, limit: int = 20) -> List[Dict]:
        """获取热门标签"""
        tags = Tag.get_popular(limit)
        return [t.to_dict() for t in tags]
    
    def get_categories(self) -> List[Dict]:
        """获取所有分类及数量"""
        results = db.session.query(
            Template.category,
            func.count(Template.id).label('count')
        ).filter(Template.is_public == True)\
            .group_by(Template.category)\
            .order_by(desc('count')).all()
        
        return [{'id': r.category, 'name': r.category, 'count': r.count} for r in results]
    
    def get_market_stats(self) -> Dict[str, Any]:
        """获取市场统计"""
        total_templates = Template.query.filter_by(is_public=True).count()
        total_downloads = db.session.query(
            func.coalesce(func.sum(Template.downloads), 0)
        ).filter(Template.is_public == True).scalar() or 0
        
        # 本周新增
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_this_week = Template.query.filter(
            Template.is_public == True,
            Template.created_at >= week_ago
        ).count()
        
        return {
            'total_templates': total_templates,
            'total_downloads': int(total_downloads),
            'new_this_week': new_this_week
        }
    
    def init_default_templates(self, admin_user_id: int):
        """初始化默认模板（首次运行时调用）"""
        # 检查是否已有模板
        if Template.query.count() > 0:
            return
        
        default_templates = [
            {
                'name': '用户注册数据',
                'description': '包含用户注册所需的完整字段，适用于用户系统测试',
                'category': 'user',
                'tags': ['用户', '注册', '基础'],
                'is_official': True,
                'fields': [
                    {'id': 'd1-1', 'name': 'user_id', 'type': 'uuid'},
                    {'id': 'd1-2', 'name': 'username', 'type': 'chineseName'},
                    {'id': 'd1-3', 'name': 'email', 'type': 'email'},
                    {'id': 'd1-4', 'name': 'phone', 'type': 'chinesePhone'},
                    {'id': 'd1-5', 'name': 'password', 'type': 'string'},
                    {'id': 'd1-6', 'name': 'created_at', 'type': 'datetime'},
                ]
            },
            {
                'name': '电商订单数据',
                'description': '电商平台订单测试数据，包含订单、用户、商品关联',
                'category': 'order',
                'tags': ['订单', '电商', '交易'],
                'is_official': True,
                'fields': [
                    {'id': 'd2-1', 'name': 'order_id', 'type': 'uuid'},
                    {'id': 'd2-2', 'name': 'customer_name', 'type': 'chineseName'},
                    {'id': 'd2-3', 'name': 'total_amount', 'type': 'amount'},
                    {'id': 'd2-4', 'name': 'shipping_address', 'type': 'chineseAddress'},
                    {'id': 'd2-5', 'name': 'order_date', 'type': 'datetime'},
                    {'id': 'd2-6', 'name': 'phone', 'type': 'chinesePhone'},
                ]
            },
            {
                'name': '财务流水记录',
                'description': '银行/支付系统的财务流水数据，包含账户、交易信息',
                'category': 'finance',
                'tags': ['财务', '银行', '流水'],
                'is_official': True,
                'fields': [
                    {'id': 'd3-1', 'name': 'transaction_id', 'type': 'uuid'},
                    {'id': 'd3-2', 'name': 'account_name', 'type': 'chineseName'},
                    {'id': 'd3-3', 'name': 'bank_card', 'type': 'bankCard'},
                    {'id': 'd3-4', 'name': 'amount', 'type': 'amount'},
                    {'id': 'd3-5', 'name': 'transaction_time', 'type': 'datetime'},
                ]
            },
            {
                'name': '商品信息数据',
                'description': '商品基础信息测试数据，适用于商品管理系统',
                'category': 'product',
                'tags': ['商品', 'SKU', '库存'],
                'is_official': True,
                'fields': [
                    {'id': 'd4-1', 'name': 'product_id', 'type': 'uuid'},
                    {'id': 'd4-2', 'name': 'product_name', 'type': 'word'},
                    {'id': 'd4-3', 'name': 'price', 'type': 'amount'},
                    {'id': 'd4-4', 'name': 'description', 'type': 'sentence'},
                    {'id': 'd4-5', 'name': 'created_at', 'type': 'datetime'},
                ]
            },
            {
                'name': '员工信息数据',
                'description': '企业员工信息测试数据，支持HR系统测试',
                'category': 'user',
                'tags': ['员工', 'HR', '企业'],
                'is_official': True,
                'fields': [
                    {'id': 'd5-1', 'name': 'employee_id', 'type': 'uuid'},
                    {'id': 'd5-2', 'name': 'name', 'type': 'chineseName'},
                    {'id': 'd5-3', 'name': 'email', 'type': 'email'},
                    {'id': 'd5-4', 'name': 'phone', 'type': 'chinesePhone'},
                    {'id': 'd5-5', 'name': 'department', 'type': 'word'},
                    {'id': 'd5-6', 'name': 'hire_date', 'type': 'date'},
                ]
            },
            {
                'name': '地址信息数据',
                'description': '中国省市区地址数据，支持完整的地址体系',
                'category': 'address',
                'tags': ['地址', '省市区', '物流'],
                'is_official': True,
                'fields': [
                    {'id': 'd6-1', 'name': 'address_id', 'type': 'uuid'},
                    {'id': 'd6-2', 'name': 'recipient', 'type': 'chineseName'},
                    {'id': 'd6-3', 'name': 'phone', 'type': 'chinesePhone'},
                    {'id': 'd6-4', 'name': 'full_address', 'type': 'chineseAddress'},
                    {'id': 'd6-5', 'name': 'postal_code', 'type': 'string'},
                ]
            }
        ]
        
        for tpl_data in default_templates:
            template = Template(
                author_id=admin_user_id,
                name=tpl_data['name'],
                description=tpl_data['description'],
                category=tpl_data['category'],
                is_public=True,
                is_official=tpl_data.get('is_official', False),
                downloads=0,
                rating=4.5 + (hash(tpl_data['name']) % 5) / 10,  # 模拟评分
                rating_count=50 + hash(tpl_data['name']) % 200
            )
            template.fields = tpl_data['fields']
            template.save()
            
            if tpl_data.get('tags'):
                template.set_tags(tpl_data['tags'])


# 单例实例
template_market_service = TemplateMarketService()
