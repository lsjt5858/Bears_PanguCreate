#!/usr/bin/env python3
"""
添加演示数据到数据库
用于展示前端页面的真实数据对接
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User, DataSource, ApiKey, ScheduledTask, GenerationHistory
from datetime import datetime, timedelta
import json

def add_demo_datasources(user_id):
    """添加演示数据源"""
    print("\n📊 添加演示数据源...")
    
    datasources = [
        {
            'name': '本地MySQL数据库',
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'database': 'test_db',
            'username': 'root',
            'password': 'password',
            'description': '本地开发环境MySQL数据库',
            'status': 'connected'
        },
        {
            'name': '生产PostgreSQL',
            'type': 'postgresql',
            'host': '192.168.1.100',
            'port': 5432,
            'database': 'prod_db',
            'username': 'postgres',
            'password': 'secret',
            'description': '生产环境PostgreSQL数据库',
            'status': 'disconnected'
        },
        {
            'name': 'MongoDB集群',
            'type': 'mongodb',
            'host': 'mongodb.example.com',
            'port': 27017,
            'database': 'analytics',
            'username': 'admin',
            'password': 'mongo123',
            'description': '数据分析MongoDB集群',
            'status': 'connected'
        }
    ]
    
    for ds_data in datasources:
        ds = DataSource(
            user_id=user_id,
            name=ds_data['name'],
            type=ds_data['type'],
            host=ds_data['host'],
            port=ds_data['port'],
            database=ds_data['database'],
            username=ds_data['username'],
            password=ds_data['password'],
            description=ds_data['description'],
            status=ds_data['status'],
            last_connected_at=datetime.now() if ds_data['status'] == 'connected' else None
        )
        db.session.add(ds)
        print(f"   ✅ 添加数据源: {ds_data['name']}")
    
    db.session.commit()
    print(f"   ✨ 成功添加 {len(datasources)} 个数据源")

def add_demo_api_keys(user_id):
    """添加演示API密钥"""
    print("\n🔑 添加演示API密钥...")
    
    # 使用API服务创建密钥
    from services.api_key_service import api_key_service
    
    api_keys_data = [
        {
            'name': '生产环境密钥',
            'permissions': ['read', 'write'],
            'expires_at': datetime.now() + timedelta(days=365)
        },
        {
            'name': '测试环境密钥',
            'permissions': ['read'],
            'expires_at': datetime.now() + timedelta(days=90)
        },
        {
            'name': '临时密钥',
            'permissions': ['read'],
            'expires_at': datetime.now() + timedelta(days=7)
        }
    ]
    
    for key_data in api_keys_data:
        api_key, error = api_key_service.create_key(
            user_id=user_id,
            name=key_data['name'],
            permissions=key_data['permissions'],
            expires_at=key_data['expires_at']
        )
        if api_key:
            print(f"   ✅ 添加API密钥: {key_data['name']}")
        else:
            print(f"   ❌ 添加失败: {key_data['name']} - {error}")
    
    print(f"   ✨ API密钥添加完成")

def add_demo_history(user_id):
    """添加演示历史记录"""
    print("\n📜 添加演示历史记录...")
    
    histories = [
        {
            'name': '用户数据生成',
            'fields': [
                {'id': '1', 'name': 'id', 'type': 'uuid'},
                {'id': '2', 'name': 'name', 'type': 'chineseName'},
                {'id': '3', 'name': 'email', 'type': 'email'},
                {'id': '4', 'name': 'phone', 'type': 'chinesePhone'}
            ],
            'row_count': 1000,
            'export_format': 'json',
            'created_at': datetime.now() - timedelta(hours=5)
        },
        {
            'name': '订单数据生成',
            'fields': [
                {'id': '1', 'name': 'order_id', 'type': 'uuid'},
                {'id': '2', 'name': 'amount', 'type': 'amount'},
                {'id': '3', 'name': 'status', 'type': 'string'},
                {'id': '4', 'name': 'created_at', 'type': 'datetime'}
            ],
            'row_count': 5000,
            'export_format': 'csv',
            'created_at': datetime.now() - timedelta(hours=3)
        },
        {
            'name': '产品信息生成',
            'fields': [
                {'id': '1', 'name': 'product_id', 'type': 'uuid'},
                {'id': '2', 'name': 'name', 'type': 'string'},
                {'id': '3', 'name': 'price', 'type': 'amount'},
                {'id': '4', 'name': 'stock', 'type': 'number'}
            ],
            'row_count': 500,
            'export_format': 'sql',
            'created_at': datetime.now() - timedelta(hours=1)
        }
    ]
    
    for hist_data in histories:
        history = GenerationHistory(
            user_id=user_id,
            name=hist_data['name'],
            fields=json.dumps(hist_data['fields']),
            row_count=hist_data['row_count'],
            export_format=hist_data['export_format'],
            created_at=hist_data['created_at']
        )
        db.session.add(history)
        print(f"   ✅ 添加历史记录: {hist_data['name']} ({hist_data['row_count']}条)")
    
    db.session.commit()
    print(f"   ✨ 成功添加 {len(histories)} 条历史记录")

def add_demo_scheduled_tasks(user_id):
    """添加演示定时任务"""
    print("\n⏰ 添加演示定时任务...")
    
    tasks = [
        {
            'name': '每日用户数据生成',
            'description': '每天凌晨2点生成1000条用户数据',
            'cron_expression': '0 2 * * *',
            'fields': [
                {'id': '1', 'name': 'id', 'type': 'uuid'},
                {'id': '2', 'name': 'name', 'type': 'chineseName'},
                {'id': '3', 'name': 'email', 'type': 'email'}
            ],
            'row_count': 1000,
            'export_format': 'json',
            'is_enabled': True,
            'status': 'active'
        },
        {
            'name': '每周订单报表',
            'description': '每周一上午9点生成订单数据',
            'cron_expression': '0 9 * * 1',
            'fields': [
                {'id': '1', 'name': 'order_id', 'type': 'uuid'},
                {'id': '2', 'name': 'amount', 'type': 'amount'}
            ],
            'row_count': 5000,
            'export_format': 'csv',
            'is_enabled': True,
            'status': 'active'
        },
        {
            'name': '测试数据生成（已暂停）',
            'description': '测试用定时任务',
            'cron_expression': '*/5 * * * *',
            'fields': [
                {'id': '1', 'name': 'test_id', 'type': 'uuid'}
            ],
            'row_count': 100,
            'export_format': 'json',
            'is_enabled': False,
            'status': 'paused'
        }
    ]
    
    for task_data in tasks:
        task = ScheduledTask(
            user_id=user_id,
            name=task_data['name'],
            description=task_data['description'],
            cron_expression=task_data['cron_expression'],
            fields=json.dumps(task_data['fields']),
            row_count=task_data['row_count'],
            export_format=task_data['export_format'],
            is_enabled=task_data['is_enabled'],
            status=task_data['status'],
            run_count=5 if task_data['is_enabled'] else 0,
            success_count=5 if task_data['is_enabled'] else 0,
            last_run_at=datetime.now() - timedelta(hours=12) if task_data['is_enabled'] else None
        )
        db.session.add(task)
        print(f"   ✅ 添加定时任务: {task_data['name']}")
    
    db.session.commit()
    print(f"   ✨ 成功添加 {len(tasks)} 个定时任务")

def main():
    """主函数"""
    print("=" * 60)
    print("🎨 Bears PanguCreate - 添加演示数据")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # 获取admin用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("❌ 找不到admin用户，请先运行 python database/init_db.py")
            return
        
        print(f"\n👤 使用用户: {admin.username} (ID: {admin.id})")
        
        # 清除现有演示数据（可选）
        print("\n🗑️  清除现有演示数据...")
        DataSource.query.filter_by(user_id=admin.id).delete()
        ApiKey.query.filter_by(user_id=admin.id).delete()
        GenerationHistory.query.filter_by(user_id=admin.id).delete()
        ScheduledTask.query.filter_by(user_id=admin.id).delete()
        db.session.commit()
        print("   ✅ 清除完成")
        
        # 添加演示数据
        add_demo_datasources(admin.id)
        add_demo_api_keys(admin.id)
        add_demo_history(admin.id)
        add_demo_scheduled_tasks(admin.id)
        
        print("\n" + "=" * 60)
        print("✅ 演示数据添加完成！")
        print("=" * 60)
        print("\n📊 数据统计:")
        print(f"   - 数据源: {DataSource.query.filter_by(user_id=admin.id).count()} 个")
        print(f"   - API密钥: {ApiKey.query.filter_by(user_id=admin.id).count()} 个")
        print(f"   - 历史记录: {GenerationHistory.query.filter_by(user_id=admin.id).count()} 条")
        print(f"   - 定时任务: {ScheduledTask.query.filter_by(user_id=admin.id).count()} 个")
        print("\n💡 现在可以登录前端查看真实数据了！")
        print("   用户名: admin")
        print("   密码: admin123")
        print("=" * 60)

if __name__ == "__main__":
    main()
