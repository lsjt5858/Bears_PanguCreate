"""
Bears_PanguCreate Backend - Flask API
企业级测试数据生成平台
"""
import sys
import os

# 添加当前目录到路径，确保模块可以正确导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime

from config import get_config
from extensions import init_extensions, db
from routes import types_bp, generate_bp, templates_bp, export_bp, auth_bp, history_bp, stats_bp, template_market_bp, api_key_bp, scheduler_bp, datasource_bp, relation_bp

# Swagger 配置
SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

SWAGGER_TEMPLATE = {
    "info": {
        "title": "Bears PanguCreate API",
        "description": "企业级测试数据生成平台 API 文档",
        "version": "1.0.0",
        "contact": {
            "name": "API Support"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT 认证，格式: Bearer {token}"
        }
    },
    "security": [{"Bearer": []}],
    "tags": [
        {"name": "认证", "description": "用户登录注册相关接口"},
        {"name": "数据生成", "description": "测试数据生成相关接口"},
        {"name": "模板", "description": "模板管理相关接口"},
        {"name": "模板市场", "description": "模板市场相关接口"},
        {"name": "历史记录", "description": "生成历史相关接口"},
        {"name": "统计", "description": "仪表盘统计相关接口"},
        {"name": "API密钥", "description": "API密钥管理相关接口"},
        {"name": "定时任务", "description": "定时任务调度相关接口"},
        {"name": "数据源", "description": "数据源管理相关接口"},
        {"name": "关联数据", "description": "关联数据生成相关接口"},
        {"name": "导出", "description": "数据导出相关接口"},
        {"name": "系统", "description": "系统状态相关接口"},
    ]
}


def create_app(config_class=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # 初始化扩展 (包括 SQLAlchemy)
    init_extensions(app)
    
    # CORS 配置
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # 初始化 Swagger
    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)
    
    # 注册蓝图
    app.register_blueprint(types_bp)
    app.register_blueprint(generate_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(template_market_bp)
    app.register_blueprint(api_key_bp)
    app.register_blueprint(scheduler_bp)
    app.register_blueprint(datasource_bp)
    app.register_blueprint(relation_bp)
    
    # 初始化调度器
    from services.scheduler_service import scheduler_service
    scheduler_service.init_scheduler(app)
    
    # 健康检查端点
    @app.route("/api/health", methods=["GET"])
    def health():
        """
        健康检查
        ---
        tags:
          - 系统
        responses:
          200:
            description: 服务正常
        """
        return jsonify({
            "status": "ok", 
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": "connected"
        })
    
    # 数据库状态检查端点
    @app.route("/api/db-status", methods=["GET"])
    def db_status():
        """
        数据库状态检查
        ---
        tags:
          - 系统
        responses:
          200:
            description: 数据库连接正常
          500:
            description: 数据库连接失败
        """
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({
                "status": "ok",
                "message": "Database connection successful"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
