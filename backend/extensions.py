"""
Flask 扩展初始化
集中管理所有 Flask 扩展实例
"""
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 实例
db = SQLAlchemy()


def init_extensions(app):
    """初始化所有扩展"""
    db.init_app(app)
    
    # 确保数据目录存在
    import os
    from pathlib import Path
    data_dir = Path(app.root_path) / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # 导入所有模型以确保表被创建
    from models import User, Project, GenerationHistory
    
    # 在应用上下文中创建所有表
    with app.app_context():
        db.create_all()
