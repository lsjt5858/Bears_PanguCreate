"""
应用配置文件
支持多环境配置：development, testing, production
支持多种数据库：SQLite, MySQL, PostgreSQL
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent


def get_database_uri():
    """
    根据环境变量构建数据库连接 URI
    优先级：DATABASE_URL > DB_TYPE 配置 > 默认 SQLite
    """
    # 1. 如果直接提供了 DATABASE_URL，直接使用
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url
    
    # 2. 根据 DB_TYPE 构建连接字符串
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'mysql':
        host = os.environ.get('MYSQL_HOST', 'localhost')
        port = os.environ.get('MYSQL_PORT', '3306')
        user = os.environ.get('MYSQL_USER', 'root')
        password = os.environ.get('MYSQL_PASSWORD', '')
        database = os.environ.get('MYSQL_DATABASE', 'pangudata')
        
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
    
    elif db_type == 'postgresql':
        host = os.environ.get('POSTGRES_HOST', 'localhost')
        port = os.environ.get('POSTGRES_PORT', '5432')
        user = os.environ.get('POSTGRES_USER', 'postgres')
        password = os.environ.get('POSTGRES_PASSWORD', '')
        database = os.environ.get('POSTGRES_DATABASE', 'pangudata')
        
        return f'postgresql://{user}:{password}@{host}:{port}/{database}'
    
    else:  # sqlite (默认)
        sqlite_path = os.environ.get('SQLITE_PATH', 'data/app.db')
        db_file = BASE_DIR / sqlite_path
        # 确保目录存在
        db_file.parent.mkdir(parents=True, exist_ok=True)
        return f'sqlite:///{db_file}'


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLAlchemy 配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 设为 True 可打印 SQL 语句
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    
    # 数据库连接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # 连接前检查连接是否有效
    }
    
    # JWT 配置
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))
    
    # CORS 配置
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
    CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 开发时打印 SQL


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 生产环境必须设置 SECRET_KEY 环境变量
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY or SECRET_KEY == 'dev-secret-key-change-in-production':
        raise ValueError("生产环境必须设置 SECRET_KEY 环境变量！")


# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """获取当前环境配置"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])


def print_config_info():
    """打印当前配置信息（用于调试）"""
    current_config = get_config()
    db_uri = current_config.SQLALCHEMY_DATABASE_URI
    
    # 隐藏密码
    if '@' in db_uri:
        parts = db_uri.split('@')
        if '://' in parts[0]:
            protocol_user = parts[0].split('://')
            if ':' in protocol_user[1]:
                user = protocol_user[1].split(':')[0]
                masked_uri = f"{protocol_user[0]}://{user}:****@{parts[1]}"
            else:
                masked_uri = db_uri
        else:
            masked_uri = db_uri
    else:
        masked_uri = db_uri
    
    print("=" * 60)
    print("📊 数据库配置信息")
    print("=" * 60)
    print(f"环境: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"数据库类型: {os.environ.get('DB_TYPE', 'sqlite')}")
    print(f"连接字符串: {masked_uri}")
    print("=" * 60)

