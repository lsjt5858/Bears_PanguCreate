"""
认证路由
处理登录、注册、Token 刷新等
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, g
from services.auth_service import auth_service, login_required
from models import Project

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    user, error = auth_service.register(username, email, password)
    
    if error:
        return jsonify({'error': error}), 400
    
    # 注册成功后自动登录
    token_data, _ = auth_service.login(username, password)
    
    return jsonify({
        'message': '注册成功',
        'data': token_data
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    username_or_email = data.get('username') or data.get('email', '')
    password = data.get('password', '')
    
    token_data, error = auth_service.login(username_or_email.strip(), password)
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'message': '登录成功',
        'data': token_data
    })


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """刷新访问令牌"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    refresh_token = data.get('refresh_token', '')
    
    if not refresh_token:
        return jsonify({'error': '刷新令牌不能为空'}), 400
    
    token_data, error = auth_service.refresh_access_token(refresh_token)
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'message': '刷新成功',
        'data': token_data
    })


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    user = g.current_user
    
    # 获取用户的项目列表
    projects = Project.find_by_owner(user.id)
    member_projects = user.member_projects.all()
    
    return jsonify({
        'user': user.to_dict(include_email=True),
        'projects': [p.to_dict() for p in projects],
        'member_projects': [p.to_dict() for p in member_projects if p.owner_id != user.id]
    })


@auth_bp.route('/password', methods=['PUT'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    user = g.current_user
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({'error': '旧密码和新密码不能为空'}), 400
    
    if not user.check_password(old_password):
        return jsonify({'error': '旧密码错误'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': '新密码至少6个字符'}), 400
    
    user.set_password(new_password)
    user.save()
    
    return jsonify({'message': '密码修改成功'})


@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新个人资料"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    user = g.current_user
    
    # 更新昵称
    if 'nickname' in data:
        nickname = data['nickname'].strip()
        if len(nickname) > 50:
            return jsonify({'error': '昵称不能超过50个字符'}), 400
        user.nickname = nickname
    
    # 更新头像
    if 'avatar' in data:
        user.avatar = data['avatar']
    
    user.save()
    
    return jsonify({
        'message': '资料更新成功',
        'user': user.to_dict(include_email=True)
    })
