#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库连接检查脚本
用于测试数据库连接是否正常
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from config import print_config_info


def check_database_connection():
    """检查数据库连接"""
    print("\n" + "=" * 60)
    print("🔍 检查数据库连接")
    print("=" * 60)
    
    # 打印配置信息
    print_config_info()
    
    # 创建应用实例
    app = create_app()
    
    with app.app_context():
        try:
            # 测试连接
            print("\n📡 测试数据库连接...")
            db.session.execute(db.text('SELECT 1'))
            print("✅ 数据库连接成功！")
            
            # 获取数据库信息
            print("\n📊 数据库信息:")
            
            # 检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"   表数量: {len(tables)}")
            if tables:
                print(f"   表列表:")
                for table in sorted(tables):
                    print(f"     - {table}")
            else:
                print("   ⚠️  数据库中没有表，请运行初始化脚本")
            
            # 如果有表，显示记录统计
            if tables:
                print("\n📈 数据统计:")
                
                if 'users' in tables:
                    from models.user import User
                    user_count = User.query.count()
                    print(f"   用户数量: {user_count}")
                
                if 'templates' in tables:
                    from models.template import Template
                    template_count = Template.query.count()
                    print(f"   模板数量: {template_count}")
                
                if 'history' in tables:
                    from models.history import History
                    history_count = History.query.count()
                    print(f"   历史记录: {history_count}")
            
            print("\n" + "=" * 60)
            print("✅ 数据库检查完成")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ 数据库连接失败: {str(e)}")
            print("\n💡 可能的原因:")
            print("   1. 数据库服务未启动")
            print("   2. 数据库配置错误（检查 .env 文件）")
            print("   3. 数据库用户权限不足")
            print("   4. 数据库不存在（运行 init_db.py 创建）")
            print("\n" + "=" * 60)
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    check_database_connection()
