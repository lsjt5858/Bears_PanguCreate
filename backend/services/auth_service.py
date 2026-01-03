"""
JWT 认证服务
处理用户认证、Token 生成与验证
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple
from functools import wraps
from flask import request, jsonify, current_app, g

from extensions import db
from models import User, Project


class AuthService:
    """认证服务"""
    
    # Token 过期时间
    ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    
    def register(self, username: str, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        用户注册
        返回: (user, error_message)
        """
        # 验证用户名
        if not username or len(username) < 3:
            return None, "用户名至少3个字符"
        if len(username) > 50:
            return None, "用户名不能超过50个字符"
        
        # 验证邮箱
        if not email or '@' not in email:
            return None, "邮箱格式不正确"
        
        # 验证密码
        if not password or len(password) < 6:
            return None, "密码至少6个字符"
        
        # 检查用户名是否已存在
        if User.find_by_username(username):
            return None, "用户名已存在"
        
        # 检查邮箱是否已存在
        if User.find_by_email(email):
            return None, "邮箱已被注册"
        
        # 创建用户
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        
        # 创建默认项目
        default_project = Project(
            name=f"{username}的项目",
            description="默认项目",
            owner_id=user.id
        )
        default_project.save()
        default_project.add_member(user, role='owner')
        
        return user, None
    
    def login(self, username_or_email: str, password: str) -> Tuple[Optional[dict], Optional[str]]:
        """
        用户登录
        返回: (token_data, error_message)
        """
        if not username_or_email or not password:
            return None, "用户名和密码不能为空"
        
        # 查找用户（支持用户名或邮箱登录）
        user = User.find_by_username(username_or_email)
        if not user:
            user = User.find_by_email(username_or_email)
        
        if not user:
            return None, "用户不存在"
        
        if not user.is_active:
            return None, "账户已被禁用"
        
        if not user.check_password(password):
            return None, "密码错误"
        
        # 更新最后登录时间
        user.update_last_login()
        
        # 生成 Token
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(self.ACCESS_TOKEN_EXPIRES.total_seconds()),
            'user': user.to_dict(include_email=True)
        }, None
    
    def generate_access_token(self, user: User) -> str:
        """生成访问令牌"""
        payload = {
            'sub': user.uuid,
            'username': user.username,
            'is_admin': user.is_admin,
            'type': 'access',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + self.ACCESS_TOKEN_EXPIRES
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def generate_refresh_token(self, user: User) -> str:
        """生成刷新令牌"""
        payload = {
            'sub': user.uuid,
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + self.REFRESH_TOKEN_EXPIRES
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def verify_token(self, token: str, token_type: str = 'access') -> Tuple[Optional[User], Optional[str]]:
        """
        验证 Token
        返回: (user, error_message)
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            if payload.get('type') != token_type:
                return None, f"无效的 Token 类型"
            
            user_uuid = payload.get('sub')
            if not user_uuid:
                return None, "无效的 Token"
            
            user = User.find_by_uuid(user_uuid)
            if not user:
                return None, "用户不存在"
            
            if not user.is_active:
                return None, "账户已被禁用"
            
            return user, None
            
        except jwt.ExpiredSignatureError:
            return None, "Token 已过期"
        except jwt.InvalidTokenError:
            return None, "无效的 Token"
    
    def refresh_access_token(self, refresh_token: str) -> Tuple[Optional[dict], Optional[str]]:
        """
        刷新访问令牌
        返回: (token_data, error_message)
        """
        user, error = self.verify_token(refresh_token, token_type='refresh')
        if error:
            return None, error
        
        access_token = self.generate_access_token(user)
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': int(self.ACCESS_TOKEN_EXPIRES.total_seconds())
        }, None
    
    def get_current_user(self) -> Optional[User]:
        """从请求中获取当前用户"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        
        token = parts[1]
        user, _ = self.verify_token(token)
        return user


# 单例实例
auth_service = AuthService()


# 装饰器：需要登录
def login_required(f):
    """需要登录的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': '未提供认证信息'}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': '认证格式错误'}), 401
        
        token = parts[1]
        user, error = auth_service.verify_token(token)
        
        if error:
            return jsonify({'error': error}), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated


# 装饰器：需要管理员权限
def admin_required(f):
    """需要管理员权限的装饰器"""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.current_user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    
    return decorated
