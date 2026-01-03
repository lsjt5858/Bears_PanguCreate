"""
路由模块
"""
from .types_routes import types_bp
from .generate_routes import generate_bp
from .templates_routes import templates_bp
from .export_routes import export_bp
from .auth_routes import auth_bp
from .history_routes import history_bp
from .stats_routes import stats_bp
from .template_market_routes import template_market_bp
from .api_key_routes import api_key_bp
from .scheduler_routes import scheduler_bp
from .datasource_routes import datasource_bp

from .relation_routes import relation_bp
from .notification_routes import notification_bp
from .webhook_routes import webhook_bp
from .masking_routes import masking_bp
from .validation_routes import validation_bp

__all__ = [
    "types_bp",
    "generate_bp", 
    "templates_bp",
    "export_bp",
    "auth_bp",
    "history_bp",
    "stats_bp",
    "template_market_bp",
    "api_key_bp",
    "scheduler_bp",
    "datasource_bp",
    "relation_bp",
    "notification_bp",
    "webhook_bp",
    "masking_bp",
    "validation_bp",
]
