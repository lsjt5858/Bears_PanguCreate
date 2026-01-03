"""
路由模块
"""
from .types_routes import types_bp
from .generate_routes import generate_bp
from .templates_routes import templates_bp
from .export_routes import export_bp
from .auth_routes import auth_bp

__all__ = [
    "types_bp",
    "generate_bp", 
    "templates_bp",
    "export_bp",
    "auth_bp",
]
