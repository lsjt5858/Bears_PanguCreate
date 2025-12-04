"""
DataForge Backend - Flask API
企业级测试数据生成平台
"""
import sys
import os

# 添加当前目录到路径，确保模块可以正确导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

from routes import types_bp, generate_bp, templates_bp, export_bp


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    
    # CORS配置
    CORS(app, origins=[
        "http://localhost:5173", 
        "http://localhost:3000", 
        "http://127.0.0.1:5173"
    ])
    
    # 注册蓝图
    app.register_blueprint(types_bp)
    app.register_blueprint(generate_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(export_bp)
    
    # 健康检查端点
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok", 
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        })
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
