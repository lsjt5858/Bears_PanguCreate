#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库备份脚本
支持 MySQL 和 SQLite 数据库备份
"""
import sys
import os
from datetime import datetime
import subprocess
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config


def backup_mysql():
    """备份 MySQL 数据库"""
    host = os.environ.get('MYSQL_HOST', 'localhost')
    port = os.environ.get('MYSQL_PORT', '3306')
    user = os.environ.get('MYSQL_USER', 'root')
    password = os.environ.get('MYSQL_PASSWORD', '')
    database = os.environ.get('MYSQL_DATABASE', 'pangudata')
    
    # 创建备份目录
    backup_dir = Path(__file__).parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'mysql_backup_{database}_{timestamp}.sql'
    
    print(f"📦 开始备份 MySQL 数据库...")
    print(f"   数据库: {database}")
    print(f"   备份文件: {backup_file}")
    
    try:
        # 使用 mysqldump 命令备份
        cmd = [
            'mysqldump',
            f'--host={host}',
            f'--port={port}',
            f'--user={user}',
            f'--password={password}',
            '--single-transaction',
            '--routines',
            '--triggers',
            database
        ]
        
        with open(backup_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True, stderr=subprocess.PIPE)
        
        # 获取文件大小
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        print(f"✅ 备份成功！")
        print(f"   文件大小: {size_mb:.2f} MB")
        print(f"   保存位置: {backup_file}")
        
        return str(backup_file)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 备份失败: {e.stderr.decode()}")
        if backup_file.exists():
            backup_file.unlink()
        raise
    except FileNotFoundError:
        print("❌ 未找到 mysqldump 命令，请确保已安装 MySQL 客户端")
        raise


def backup_sqlite():
    """备份 SQLite 数据库"""
    import shutil
    
    sqlite_path = os.environ.get('SQLITE_PATH', 'data/app.db')
    base_dir = Path(__file__).parent.parent
    db_file = base_dir / sqlite_path
    
    if not db_file.exists():
        print(f"❌ SQLite 数据库文件不存在: {db_file}")
        return None
    
    # 创建备份目录
    backup_dir = Path(__file__).parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'sqlite_backup_{timestamp}.db'
    
    print(f"📦 开始备份 SQLite 数据库...")
    print(f"   源文件: {db_file}")
    print(f"   备份文件: {backup_file}")
    
    try:
        # 复制文件
        shutil.copy2(db_file, backup_file)
        
        # 获取文件大小
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        print(f"✅ 备份成功！")
        print(f"   文件大小: {size_mb:.2f} MB")
        print(f"   保存位置: {backup_file}")
        
        return str(backup_file)
        
    except Exception as e:
        print(f"❌ 备份失败: {str(e)}")
        raise


def backup_database():
    """根据配置备份数据库"""
    print("\n" + "=" * 60)
    print("💾 数据库备份工具")
    print("=" * 60)
    
    config = get_config()
    db_uri = config.SQLALCHEMY_DATABASE_URI
    
    print(f"\n数据库类型: {os.environ.get('DB_TYPE', 'sqlite')}")
    
    try:
        if 'mysql' in db_uri:
            backup_file = backup_mysql()
        elif 'sqlite' in db_uri:
            backup_file = backup_sqlite()
        else:
            print("❌ 不支持的数据库类型")
            return
        
        print("\n" + "=" * 60)
        print("🎉 备份完成！")
        print("=" * 60)
        
        # 清理旧备份（保留最近10个）
        backup_dir = Path(__file__).parent / 'backups'
        backups = sorted(backup_dir.glob('*backup*.sql')) + sorted(backup_dir.glob('*backup*.db'))
        if len(backups) > 10:
            print(f"\n🧹 清理旧备份文件...")
            for old_backup in backups[:-10]:
                old_backup.unlink()
                print(f"   删除: {old_backup.name}")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ 备份失败")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    backup_database()
