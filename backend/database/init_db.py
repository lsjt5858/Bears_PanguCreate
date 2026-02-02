#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建数据库表和初始化数据
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from config import print_config_info
import pymysql


def create_database_if_not_exists():
    """如果数据库不存在，则创建数据库（仅MySQL）"""
    from config import get_config
    config = get_config()
    db_uri = config.SQLALCHEMY_DATABASE_URI
    
    # 只处理 MySQL
    if 'mysql' in db_uri:
        import os
        host = os.environ.get('MYSQL_HOST', 'localhost')
        port = int(os.environ.get('MYSQL_PORT', '3306'))
        user = os.environ.get('MYSQL_USER', 'root')
        password = os.environ.get('MYSQL_PASSWORD', '')
        database = os.environ.get('MYSQL_DATABASE', 'pangudata')
        
        try:
            # 连接到 MySQL 服务器（不指定数据库）
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            
            with connection.cursor() as cursor:
                # 创建数据库（如果不存在）
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 数据库 '{database}' 已准备就绪")
            
            connection.close()
        except Exception as e:
            print(f"❌ 创建数据库失败: {str(e)}")
            raise


def init_database(drop_existing=False):
    """
    初始化数据库
    
    Args:
        drop_existing: 是否删除现有表（默认False，生产环境慎用！）
    """
    print("\n" + "=" * 60)
    print("🚀 开始初始化数据库")
    print("=" * 60)
    
    # 打印配置信息
    print_config_info()
    
    # 创建应用实例
    app = create_app()
    
    with app.app_context():
        try:
            # 如果是 MySQL，先确保数据库存在
            create_database_if_not_exists()
            
            # 删除所有表（谨慎使用！）
            if drop_existing:
                print("\n⚠️  删除现有表...")
                db.drop_all()
                print("✅ 现有表已删除")
            
            # 创建所有表
            print("\n📦 创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建成功")
            
            # 创建默认管理员用户
            print("\n👤 创建默认管理员用户...")
            from models.user import User
            
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@pangudata.com',
                    nickname='系统管理员',
                    is_admin=True,
                    is_active=True
                )
                admin.set_password('admin123')
                admin.save()
                print(f"✅ 管理员用户创建成功")
                print(f"   用户名: admin")
                print(f"   密码: admin123")
                print(f"   ⚠️  请在生产环境中修改默认密码！")
            else:
                print("ℹ️  管理员用户已存在")
            
            # 创建测试用户
            print("\n👥 创建测试用户...")
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@pangudata.com',
                    nickname='测试用户',
                    is_admin=False,
                    is_active=True
                )
                test_user.set_password('test123')
                test_user.save()
                print(f"✅ 测试用户创建成功")
                print(f"   用户名: testuser")
                print(f"   密码: test123")
            else:
                print("ℹ️  测试用户已存在")
            
            # 初始化默认模板
            print("\n📋 初始化默认模板...")
            from services.template_market_service import template_market_service
            template_market_service.init_default_templates(admin.id)
            print("✅ 默认模板初始化成功")
            
            # 显示统计信息
            print("\n" + "=" * 60)
            print("📊 数据库统计")
            print("=" * 60)
            
            from models.template import Template
            from models.user import User
            
            user_count = User.query.count()
            template_count = Template.query.count()
            
            print(f"用户数量: {user_count}")
            print(f"模板数量: {template_count}")
            
            print("\n" + "=" * 60)
            print("🎉 数据库初始化完成！")
            print("=" * 60)
            print("\n可以使用以下命令启动服务:")
            print("  cd backend")
            print("  source venv/bin/activate")
            print("  python app.py")
            print("\n或访问 API 文档:")
            print("  http://localhost:5001/docs")
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"\n❌ 数据库初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='初始化数据库')
    parser.add_argument('--drop', action='store_true', help='删除现有表（谨慎使用！）')
    args = parser.parse_args()
    
    if args.drop:
        confirm = input("⚠️  确定要删除所有现有表吗？这将清空所有数据！(yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ 操作已取消")
            sys.exit(0)
    
    init_database(drop_existing=args.drop)
