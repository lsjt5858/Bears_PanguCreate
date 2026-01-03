"""
数据源服务
管理数据源的创建、连接、测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from extensions import db
from models.datasource import DataSource


class DataSourceService:
    """数据源服务"""
    
    def create_datasource(
        self,
        user_id: int,
        name: str,
        ds_type: str,
        host: str,
        port: int,
        database: str = None,
        username: str = None,
        password: str = None,
        description: str = None,
        project_id: int = None,
        use_ssl: bool = False,
        ssl_config: dict = None,
        api_config: dict = None
    ) -> Tuple[Optional[DataSource], Optional[str]]:
        """创建数据源"""
        # 验证类型
        valid_types = ['mysql', 'postgresql', 'mongodb', 'restapi']
        if ds_type not in valid_types:
            return None, f"不支持的数据源类型: {ds_type}"
        
        # 验证端口
        if not (1 <= port <= 65535):
            return None, "端口号必须在 1-65535 之间"
        
        # 创建数据源
        datasource = DataSource(
            user_id=user_id,
            project_id=project_id,
            name=name,
            description=description,
            type=ds_type,
            host=host,
            port=port,
            database=database,
            username=username,
            use_ssl=use_ssl
        )
        
        # 设置密码
        if password:
            datasource.password = password
        
        # 设置 SSL 配置
        if ssl_config:
            datasource.ssl_config = ssl_config
        
        # 设置 API 配置
        if api_config:
            datasource.api_config = api_config
        
        datasource.save()
        return datasource, None
    
    def update_datasource(
        self,
        datasource_id: str,
        user_id: int,
        **kwargs
    ) -> Tuple[Optional[DataSource], Optional[str]]:
        """更新数据源"""
        datasource = DataSource.find_by_uuid(datasource_id)
        if not datasource:
            return None, "数据源不存在"
        
        if datasource.user_id != user_id:
            return None, "无权修改此数据源"
        
        # 更新字段
        if 'name' in kwargs:
            datasource.name = kwargs['name']
        if 'description' in kwargs:
            datasource.description = kwargs['description']
        if 'host' in kwargs:
            datasource.host = kwargs['host']
        if 'port' in kwargs:
            port = kwargs['port']
            if not (1 <= port <= 65535):
                return None, "端口号必须在 1-65535 之间"
            datasource.port = port
        if 'database' in kwargs:
            datasource.database = kwargs['database']
        if 'username' in kwargs:
            datasource.username = kwargs['username']
        if 'password' in kwargs and kwargs['password']:
            datasource.password = kwargs['password']
        if 'use_ssl' in kwargs:
            datasource.use_ssl = kwargs['use_ssl']
        if 'ssl_config' in kwargs:
            datasource.ssl_config = kwargs['ssl_config']
        if 'api_config' in kwargs:
            datasource.api_config = kwargs['api_config']
        
        datasource.save()
        return datasource, None
    
    def delete_datasource(self, datasource_id: str, user_id: int) -> Tuple[bool, Optional[str]]:
        """删除数据源"""
        datasource = DataSource.find_by_uuid(datasource_id)
        if not datasource:
            return False, "数据源不存在"
        
        if datasource.user_id != user_id:
            return False, "无权删除此数据源"
        
        datasource.delete()
        return True, None
    
    def get_datasource(self, datasource_id: str, user_id: int) -> Optional[DataSource]:
        """获取数据源详情"""
        datasource = DataSource.find_by_uuid(datasource_id)
        if not datasource or datasource.user_id != user_id:
            return None
        return datasource
    
    def list_datasources(
        self,
        user_id: int,
        project_id: int = None,
        ds_type: str = None,
        status: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[DataSource], int]:
        """获取数据源列表"""
        query = DataSource.query.filter_by(user_id=user_id)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        if ds_type:
            query = query.filter_by(type=ds_type)
        if status:
            query = query.filter_by(status=status)
        
        total = query.count()
        
        offset = (page - 1) * page_size
        datasources = query.order_by(DataSource.created_at.desc())\
            .limit(page_size).offset(offset).all()
        
        return datasources, total
    
    def test_connection(self, datasource_id: str, user_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """测试数据源连接"""
        datasource = DataSource.find_by_uuid(datasource_id)
        if not datasource:
            return False, "数据源不存在", None
        
        if datasource.user_id != user_id:
            return False, "无权操作此数据源", None
        
        ds_type = datasource.type
        
        try:
            if ds_type == 'mysql':
                return self._test_mysql(datasource)
            elif ds_type == 'postgresql':
                return self._test_postgresql(datasource)
            elif ds_type == 'mongodb':
                return self._test_mongodb(datasource)
            elif ds_type == 'restapi':
                return self._test_restapi(datasource)
            else:
                return False, f"不支持的数据源类型: {ds_type}", None
        except Exception as e:
            datasource.update_status('error', str(e))
            return False, str(e), None
    
    def test_connection_params(
        self,
        ds_type: str,
        host: str,
        port: int,
        database: str = None,
        username: str = None,
        password: str = None,
        use_ssl: bool = False,
        api_config: dict = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """测试连接参数（不保存）"""
        try:
            if ds_type == 'mysql':
                return self._test_mysql_params(host, port, database, username, password, use_ssl)
            elif ds_type == 'postgresql':
                return self._test_postgresql_params(host, port, database, username, password, use_ssl)
            elif ds_type == 'mongodb':
                return self._test_mongodb_params(host, port, database, username, password)
            elif ds_type == 'restapi':
                return self._test_restapi_params(host, port, use_ssl, api_config)
            else:
                return False, f"不支持的数据源类型: {ds_type}", None
        except Exception as e:
            return False, str(e), None
    
    def _test_mysql(self, datasource: DataSource) -> Tuple[bool, str, Optional[Dict]]:
        """测试 MySQL 连接"""
        return self._test_mysql_params(
            datasource.host,
            datasource.port,
            datasource.database,
            datasource.username,
            datasource.get_password(),
            datasource.use_ssl
        )
    
    def _test_mysql_params(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        use_ssl: bool
    ) -> Tuple[bool, str, Optional[Dict]]:
        """测试 MySQL 连接参数"""
        try:
            import pymysql
            
            conn = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password or '',
                database=database,
                connect_timeout=10,
                ssl={'ssl': {}} if use_ssl else None
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            
            # 获取表列表
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return True, f"连接成功 (MySQL {version})", {
                'version': version,
                'tables': tables[:20]  # 最多返回 20 个表
            }
        except ImportError:
            return False, "未安装 pymysql 库", None
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def _test_postgresql(self, datasource: DataSource) -> Tuple[bool, str, Optional[Dict]]:
        """测试 PostgreSQL 连接"""
        return self._test_postgresql_params(
            datasource.host,
            datasource.port,
            datasource.database,
            datasource.username,
            datasource.get_password(),
            datasource.use_ssl
        )
    
    def _test_postgresql_params(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        use_ssl: bool
    ) -> Tuple[bool, str, Optional[Dict]]:
        """测试 PostgreSQL 连接参数"""
        try:
            import psycopg2
            
            sslmode = 'require' if use_ssl else 'disable'
            
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password or '',
                dbname=database,
                connect_timeout=10,
                sslmode=sslmode
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            
            # 获取表列表
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' LIMIT 20
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return True, f"连接成功", {
                'version': version,
                'tables': tables
            }
        except ImportError:
            return False, "未安装 psycopg2 库", None
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def _test_mongodb(self, datasource: DataSource) -> Tuple[bool, str, Optional[Dict]]:
        """测试 MongoDB 连接"""
        return self._test_mongodb_params(
            datasource.host,
            datasource.port,
            datasource.database,
            datasource.username,
            datasource.get_password()
        )
    
    def _test_mongodb_params(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str
    ) -> Tuple[bool, str, Optional[Dict]]:
        """测试 MongoDB 连接参数"""
        try:
            from pymongo import MongoClient
            
            if username and password:
                uri = f"mongodb://{username}:{password}@{host}:{port}/"
            else:
                uri = f"mongodb://{host}:{port}/"
            
            client = MongoClient(uri, serverSelectionTimeoutMS=10000)
            
            # 测试连接
            server_info = client.server_info()
            version = server_info.get('version', 'unknown')
            
            # 获取集合列表
            if database:
                db = client[database]
                collections = db.list_collection_names()[:20]
            else:
                collections = []
            
            client.close()
            
            return True, f"连接成功 (MongoDB {version})", {
                'version': version,
                'collections': collections
            }
        except ImportError:
            return False, "未安装 pymongo 库", None
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def _test_restapi(self, datasource: DataSource) -> Tuple[bool, str, Optional[Dict]]:
        """测试 REST API 连接"""
        return self._test_restapi_params(
            datasource.host,
            datasource.port,
            datasource.use_ssl,
            datasource.api_config
        )
    
    def _test_restapi_params(
        self,
        host: str,
        port: int,
        use_ssl: bool,
        api_config: dict = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """测试 REST API 连接参数"""
        try:
            import requests
            
            protocol = 'https' if use_ssl else 'http'
            base_url = f"{protocol}://{host}:{port}"
            
            # 获取测试端点
            test_endpoint = '/'
            if api_config:
                test_endpoint = api_config.get('test_endpoint', '/')
            
            url = f"{base_url}{test_endpoint}"
            
            # 设置请求头
            headers = {}
            if api_config:
                headers = api_config.get('headers', {})
            
            response = requests.get(url, headers=headers, timeout=10, verify=use_ssl)
            
            return True, f"连接成功 (HTTP {response.status_code})", {
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type', 'unknown')
            }
        except ImportError:
            return False, "未安装 requests 库", None
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def get_tables(self, datasource_id: str, user_id: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """获取数据源的表/集合列表"""
        datasource = DataSource.find_by_uuid(datasource_id)
        if not datasource:
            return None, "数据源不存在"
        
        if datasource.user_id != user_id:
            return None, "无权操作此数据源"
        
        ds_type = datasource.type
        
        try:
            if ds_type == 'mysql':
                return self._get_mysql_tables(datasource)
            elif ds_type == 'postgresql':
                return self._get_postgresql_tables(datasource)
            elif ds_type == 'mongodb':
                return self._get_mongodb_collections(datasource)
            else:
                return None, f"不支持获取表列表: {ds_type}"
        except Exception as e:
            return None, str(e)
    
    def _get_mysql_tables(self, datasource: DataSource) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """获取 MySQL 表列表"""
        try:
            import pymysql
            
            conn = pymysql.connect(
                host=datasource.host,
                port=datasource.port,
                user=datasource.username,
                password=datasource.get_password() or '',
                database=datasource.database,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = []
            
            for row in cursor.fetchall():
                table_name = row[0]
                # 获取列信息
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = []
                for col in cursor.fetchall():
                    columns.append({
                        'name': col[0],
                        'type': col[1],
                        'nullable': col[2] == 'YES',
                        'primary_key': col[3] == 'PRI'
                    })
                tables.append({
                    'name': table_name,
                    'columns': columns
                })
            
            cursor.close()
            conn.close()
            
            datasource.record_query()
            return tables, None
        except Exception as e:
            return None, str(e)
    
    def _get_postgresql_tables(self, datasource: DataSource) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """获取 PostgreSQL 表列表"""
        try:
            import psycopg2
            
            conn = psycopg2.connect(
                host=datasource.host,
                port=datasource.port,
                user=datasource.username,
                password=datasource.get_password() or '',
                dbname=datasource.database,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            
            # 获取表列表
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            tables = []
            for row in cursor.fetchall():
                table_name = row[0]
                # 获取列信息
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, 
                           (SELECT COUNT(*) FROM information_schema.key_column_usage 
                            WHERE table_name = c.table_name AND column_name = c.column_name) as is_pk
                    FROM information_schema.columns c
                    WHERE table_schema = 'public' AND table_name = %s
                """, (table_name,))
                
                columns = []
                for col in cursor.fetchall():
                    columns.append({
                        'name': col[0],
                        'type': col[1],
                        'nullable': col[2] == 'YES',
                        'primary_key': col[3] > 0
                    })
                tables.append({
                    'name': table_name,
                    'columns': columns
                })
            
            cursor.close()
            conn.close()
            
            datasource.record_query()
            return tables, None
        except Exception as e:
            return None, str(e)
    
    def _get_mongodb_collections(self, datasource: DataSource) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """获取 MongoDB 集合列表"""
        try:
            from pymongo import MongoClient
            
            username = datasource.username
            password = datasource.get_password()
            
            if username and password:
                uri = f"mongodb://{username}:{password}@{datasource.host}:{datasource.port}/"
            else:
                uri = f"mongodb://{datasource.host}:{datasource.port}/"
            
            client = MongoClient(uri, serverSelectionTimeoutMS=10000)
            db = client[datasource.database]
            
            collections = []
            for coll_name in db.list_collection_names():
                # 获取一个示例文档来推断字段
                sample = db[coll_name].find_one()
                columns = []
                if sample:
                    for key, value in sample.items():
                        columns.append({
                            'name': key,
                            'type': type(value).__name__,
                            'nullable': True,
                            'primary_key': key == '_id'
                        })
                collections.append({
                    'name': coll_name,
                    'columns': columns
                })
            
            client.close()
            
            datasource.record_query()
            return collections, None
        except Exception as e:
            return None, str(e)


# 单例实例
datasource_service = DataSourceService()
