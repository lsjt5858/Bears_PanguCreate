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
from datetime import datetime

from config import get_config
from extensions import init_extensions, db
from routes import types_bp, generate_bp, templates_bp, export_bp, auth_bp, history_bp, stats_bp, template_market_bp, api_key_bp, scheduler_bp


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
    
    # 初始化调度器
    from services.scheduler_service import scheduler_service
    scheduler_service.init_scheduler(app)
    
    # 健康检查端点
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok", 
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": "connected"
        })
    
    # 数据库状态检查端点
    @app.route("/api/db-status", methods=["GET"])
    def db_status():
        try:
            # 执行简单查询测试数据库连接
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
