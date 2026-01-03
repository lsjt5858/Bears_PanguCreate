"""
模板市场路由
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g

from middleware import login_required, optional_auth
from services.template_market_service import template_market_service

template_market_bp = Blueprint('template_market', __name__, url_prefix='/api/market')


@template_market_bp.route('/templates', methods=['GET'])
@optional_auth
def list_templates():
    """
    获取模板市场列表
    ---
    tags:
      - 模板市场
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: page_size
        type: integer
        default: 20
      - in: query
        name: category
        type: string
      - in: query
        name: search
        type: string
      - in: query
        name: sort_by
        type: string
        enum: [downloads, rating, created_at]
        default: downloads
      - in: query
        name: tags
        type: array
        items:
          type: string
    responses:
      200:
        description: 返回模板列表
    """
    user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    page_size = min(page_size, 50)
    
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'downloads')
    tags = request.args.getlist('tags')
    
    templates, total = template_market_service.list_templates(
        page=page, page_size=page_size, category=category,
        search=search, tags=tags, sort_by=sort_by, user_id=user_id
    )
    
    return jsonify({
        'data': templates,
        'pagination': {
            'page': page, 'page_size': page_size, 'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@template_market_bp.route('/templates/<template_id>', methods=['GET'])
@optional_auth
def get_template(template_id):
    """
    获取模板详情
    ---
    tags:
      - 模板市场
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
    responses:
      200:
        description: 返回模板详情
      404:
        description: 模板不存在
    """
    user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    template = template_market_service.get_template(template_id, user_id=user_id)
    if not template:
        return jsonify({'error': '模板不存在'}), 404
    return jsonify({'data': template})


@template_market_bp.route('/templates', methods=['POST'])
@login_required
def create_template():
    """
    创建模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - fields
          properties:
            name:
              type: string
            description:
              type: string
            category:
              type: string
            fields:
              type: array
            tags:
              type: array
            is_public:
              type: boolean
              default: true
    responses:
      201:
        description: 创建成功
    """
    user = g.current_user
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': '模板名称不能为空'}), 400
    if not data.get('fields'):
        return jsonify({'error': '字段配置不能为空'}), 400
    
    template = template_market_service.create_template(
        author_id=user.id, name=data['name'], description=data.get('description'),
        category=data.get('category', 'other'), fields=data['fields'],
        tags=data.get('tags', []), is_public=data.get('is_public', True)
    )
    
    return jsonify({'message': '模板创建成功', 'data': template.to_dict()}), 201


@template_market_bp.route('/templates/<template_id>', methods=['PUT'])
@login_required
def update_template(template_id):
    """
    更新模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
    responses:
      200:
        description: 更新成功
    """
    user = g.current_user
    data = request.get_json()
    template, error = template_market_service.update_template(template_id=template_id, user_id=user.id, **data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': '模板更新成功', 'data': template.to_dict()})


@template_market_bp.route('/templates/<template_id>', methods=['DELETE'])
@login_required
def delete_template(template_id):
    """
    删除模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
    responses:
      200:
        description: 删除成功
    """
    user = g.current_user
    success, error = template_market_service.delete_template(template_id, user.id)
    if not success:
        return jsonify({'error': error}), 400
    return jsonify({'message': '模板删除成功'})


@template_market_bp.route('/templates/<template_id>/use', methods=['POST'])
@optional_auth
def use_template(template_id):
    """
    使用模板（记录下载）
    ---
    tags:
      - 模板市场
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
    responses:
      200:
        description: 获取成功
    """
    user_id = g.current_user.id if hasattr(g, 'current_user') and g.current_user else None
    template = template_market_service.use_template(template_id=template_id, user_id=user_id, ip_address=request.remote_addr)
    if not template:
        return jsonify({'error': '模板不存在'}), 404
    return jsonify({'message': '模板获取成功', 'data': template.to_dict()})


@template_market_bp.route('/templates/<template_id>/rate', methods=['POST'])
@login_required
def rate_template(template_id):
    """
    评分模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - score
          properties:
            score:
              type: integer
              minimum: 1
              maximum: 5
            comment:
              type: string
    responses:
      200:
        description: 评分成功
    """
    user = g.current_user
    data = request.get_json()
    score = data.get('score')
    if not score or not isinstance(score, int):
        return jsonify({'error': '请提供有效的评分 (1-5)'}), 400
    rating, error = template_market_service.rate_template(template_id=template_id, user_id=user.id, score=score, comment=data.get('comment'))
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': '评分成功', 'data': rating.to_dict()})


@template_market_bp.route('/templates/<template_id>/ratings', methods=['GET'])
def get_template_ratings(template_id):
    """
    获取模板评分列表
    ---
    tags:
      - 模板市场
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
      - in: query
        name: page
        type: integer
      - in: query
        name: page_size
        type: integer
    responses:
      200:
        description: 返回评分列表
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    ratings, total = template_market_service.get_template_ratings(template_id=template_id, page=page, page_size=page_size)
    return jsonify({'data': ratings, 'pagination': {'page': page, 'page_size': page_size, 'total': total, 'total_pages': (total + page_size - 1) // page_size}})


@template_market_bp.route('/templates/<template_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(template_id):
    """
    切换收藏状态
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    parameters:
      - in: path
        name: template_id
        type: string
        required: true
    responses:
      200:
        description: 操作成功
    """
    user = g.current_user
    success, is_favorite = template_market_service.toggle_favorite(template_id=template_id, user_id=user.id)
    if not success:
        return jsonify({'error': '模板不存在'}), 404
    return jsonify({'message': '收藏成功' if is_favorite else '已取消收藏', 'is_favorite': is_favorite})


@template_market_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    """
    获取用户收藏的模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    responses:
      200:
        description: 返回收藏列表
    """
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    templates, total = template_market_service.get_user_favorites(user_id=user.id, page=page, page_size=page_size)
    return jsonify({'data': templates, 'pagination': {'page': page, 'page_size': page_size, 'total': total, 'total_pages': (total + page_size - 1) // page_size}})


@template_market_bp.route('/my-templates', methods=['GET'])
@login_required
def get_my_templates():
    """
    获取我创建的模板
    ---
    tags:
      - 模板市场
    security:
      - Bearer: []
    responses:
      200:
        description: 返回我的模板列表
    """
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    templates, total = template_market_service.list_templates(page=page, page_size=page_size, author_id=user.id, is_public=None, user_id=user.id)
    return jsonify({'data': templates, 'pagination': {'page': page, 'page_size': page_size, 'total': total, 'total_pages': (total + page_size - 1) // page_size}})


@template_market_bp.route('/tags', methods=['GET'])
def get_popular_tags():
    """
    获取热门标签
    ---
    tags:
      - 模板市场
    parameters:
      - in: query
        name: limit
        type: integer
        default: 20
    responses:
      200:
        description: 返回标签列表
    """
    limit = request.args.get('limit', 20, type=int)
    tags = template_market_service.get_popular_tags(limit=limit)
    return jsonify({'data': tags})


@template_market_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    获取分类列表
    ---
    tags:
      - 模板市场
    responses:
      200:
        description: 返回分类列表
    """
    categories = template_market_service.get_categories()
    predefined = [
        {'id': 'all', 'name': '全部'}, {'id': 'user', 'name': '用户相关'},
        {'id': 'order', 'name': '订单交易'}, {'id': 'finance', 'name': '财务金融'},
        {'id': 'product', 'name': '商品信息'}, {'id': 'address', 'name': '地址物流'},
        {'id': 'other', 'name': '其他'}
    ]
    category_counts = {c['id']: c['count'] for c in categories}
    for cat in predefined:
        cat['count'] = category_counts.get(cat['id'], 0)
    return jsonify({'data': predefined})


@template_market_bp.route('/stats', methods=['GET'])
def get_market_stats():
    """
    获取市场统计
    ---
    tags:
      - 模板市场
    responses:
      200:
        description: 返回市场统计数据
    """
    stats = template_market_service.get_market_stats()
    return jsonify({'data': stats})
