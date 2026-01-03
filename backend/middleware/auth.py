"""
认证与权限中间件
提供各种权限验证装饰器
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functools import wraps
from flask import request, jsonify, g
import jwt
from typing import Optional

from extensions import db
from models import User, Project


def _get_token_from_header() -> Optional[str]:
    """从请求头获取 Token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]


def _verify_token(token: str) -> tuple[Optional[User], Optional[str]]:
    """验证 Token 并返回用户"""
    from flask import current_app
    
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        
        if payload.get('type') != 'access':
            return None, "无效的 Token 类型"
        
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


def get_current_user() -> Optional[User]:
    """获取当前登录用户（不强制要求登录）"""
    if hasattr(g, 'current_user'):
        return g.current_user
    
    token = _get_token_from_header()
    if not token:
        return None
    
    user, _ = _verify_token(token)
    return user


def login_required(f):
    """
    需要登录的装饰器
    验证失败返回 401
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token_from_header()
        if not token:
            return jsonify({'error': '未提供认证信息'}), 401
        
        user, error = _verify_token(token)
        if error:
            return jsonify({'error': error}), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    需要管理员权限的装饰器
    验证失败返回 401 或 403
    """
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.current_user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    
    return decorated


def optional_auth(f):
    """
    可选认证装饰器
    有 Token 则验证，无 Token 也放行
    用于某些接口需要区分登录/未登录用户
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token_from_header()
        if token:
            user, _ = _verify_token(token)
            g.current_user = user
        else:
            g.current_user = None
        return f(*args, **kwargs)
    
    return decorated


def project_access_required(f):
    """
    需要项目访问权限的装饰器
    要求 URL 参数中有 project_id 或请求体中有 project_id
    用户必须是项目所有者或成员
    """
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        # 从 URL 参数获取 project_id
        project_id = kwargs.get('project_id')
        
        # 如果 URL 中没有，尝试从请求体获取
        if not project_id:
            data = request.get_json(silent=True) or {}
            project_id = data.get('project_id')
        
        # 如果还没有，尝试从查询参数获取
        if not project_id:
            project_id = request.args.get('project_id')
        
        if not project_id:
            return jsonify({'error': '缺少项目 ID'}), 400
        
        # 查找项目
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        if not project.is_active:
            return jsonify({'error': '项目已被禁用'}), 403
        
        user = g.current_user
        
        # 检查权限：所有者或成员
        if project.owner_id != user.id and not project.is_member(user):
            return jsonify({'error': '无权访问此项目'}), 403
        
        g.current_project = project
        return f(*args, **kwargs)
    
    return decorated


def project_admin_required(f):
    """
    需要项目管理员权限的装饰器
    用户必须是项目所有者或项目管理员
    """
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        # 从 URL 参数获取 project_id
        project_id = kwargs.get('project_id')
        
        if not project_id:
            data = request.get_json(silent=True) or {}
            project_id = data.get('project_id')
        
        if not project_id:
            project_id = request.args.get('project_id')
        
        if not project_id:
            return jsonify({'error': '缺少项目 ID'}), 400
        
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        if not project.is_active:
            return jsonify({'error': '项目已被禁用'}), 403
        
        user = g.current_user
        
        # 检查权限：所有者或管理员角色
        is_owner = project.owner_id == user.id
        member_role = project.get_member_role(user)
        is_admin = member_role in ('owner', 'admin')
        
        if not is_owner and not is_admin:
            return jsonify({'error': '需要项目管理员权限'}), 403
        
        g.current_project = project
        return f(*args, **kwargs)
    
    return decorated


class RateLimiter:
    """
    简单的请求频率限制器
    基于内存存储，适合单实例部署
    生产环境建议使用 Redis
    """
    def __init__(self):
        self._requests = {}  # {key: [(timestamp, count)]}
    
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """
        检查是否允许请求
        key: 限制键（如 IP 或用户 ID）
        limit: 时间窗口内最大请求数
        window: 时间窗口（秒）
        """
        import time
        now = time.time()
        
        if key not in self._requests:
            self._requests[key] = []
        
        # 清理过期记录
        self._requests[key] = [
            (ts, cnt) for ts, cnt in self._requests[key]
            if now - ts < window
        ]
        
        # 计算当前窗口内的请求数
        total = sum(cnt for _, cnt in self._requests[key])
        
        if total >= limit:
            return False
        
        self._requests[key].append((now, 1))
        return True


# 全局限流器实例
rate_limiter = RateLimiter()


def rate_limit(limit: int = 60, window: int = 60, key_func=None):
    """
    请求频率限制装饰器
    limit: 时间窗口内最大请求数（默认 60）
    window: 时间窗口秒数（默认 60）
    key_func: 自定义限制键函数，默认使用 IP
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if key_func:
                key = key_func()
            else:
                # 默认使用 IP 地址
                key = request.remote_addr or 'unknown'
            
            if not rate_limiter.is_allowed(key, limit, window):
                return jsonify({
                    'error': '请求过于频繁，请稍后再试',
                    'retry_after': window
                }), 429
            
            return f(*args, **kwargs)
        return decorated
    return decorator
