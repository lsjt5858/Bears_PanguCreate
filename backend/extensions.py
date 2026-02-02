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
    
    # 确保数据目录存在（仅SQLite需要）
    import os
    from pathlib import Path
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        data_dir = Path(app.root_path) / 'data'
        data_dir.mkdir(exist_ok=True)
    
    # 导入所有模型（确保模型被注册）
    from models import User, Project, GenerationHistory
    from models.template import Template as TemplateModel, Tag, TemplateRating, TemplateFavorite, TemplateDownload
    from models.api_key import ApiKey, ApiKeyUsageLog
    from models.scheduled_task import ScheduledTask, TaskExecutionLog
    
    # 注意：不在这里自动创建表，由init_db.py脚本负责
    # 如果需要自动创建表，可以取消下面的注释
    # with app.app_context():
    #     db.create_all()
    
    # 初始化调度器（开发环境也启用）
    if not app.config.get('TESTING'):
        from services.scheduler_service import scheduler_service
        scheduler_service.init_scheduler(app)
