"""
MongoDB 数据库连接器
"""
from typing import List, Dict, Any, Optional, Tuple
from .base_connector import BaseConnector


class MongoDBConnector(BaseConnector):
    """MongoDB 连接器"""
    
    def __init__(
        self,
        host: str,
        port: int = 27017,
        database: str = None,
        username: str = None,
        password: str = None,
        auth_source: str = 'admin',
        replica_set: str = None,
        **kwargs
    ):
        super().__init__(host, port, database, username, password, **kwargs)
        self.auth_source = auth_source
        self.replica_set = replica_set
        self._client = None
        self._db = None
    
    def connect(self) -> bool:
        """建立连接"""
        try:
            from pymongo import MongoClient
            
            # 构建连接 URI
            if self.username and self.password:
                uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
                uri += f"?authSource={self.auth_source}"
            else:
                uri = f"mongodb://{self.host}:{self.port}/"
            
            if self.replica_set:
                uri += f"&replicaSet={self.replica_set}"
            
            self._client = MongoClient(uri, serverSelectionTimeoutMS=10000)
            
            # 测试连接
            self._client.server_info()
            
            if self.database:
                self._db = self._client[self.database]
            
            return True
        except Exception as e:
            raise ConnectionError(f"MongoDB 连接失败: {str(e)}")
    
    def disconnect(self) -> None:
        """断开连接"""
        if self._client:
            try:
                self._client.close()
            except:
                pass
            self._client = None
            self._db = None
    
    def test_connection(self) -> Tuple[bool, str, Optional[Dict]]:
        """测试连接"""
        try:
            self.connect()
            
            server_info = self._client.server_info()
            version = server_info.get('version', 'unknown')
            
            # 获取集合数量
            if self._db:
                collection_count = len(self._db.list_collection_names())
            else:
                collection_count = 0
            
            self.disconnect()
            
            return True, f"连接成功 (MongoDB {version})", {
                'version': version,
                'collection_count': collection_count
            }
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def get_tables(self) -> List[Dict[str, Any]]:
        """获取集合列表"""
        if not self._client:
            self.connect()
        
        if not self._db:
            return []
        
        collections = []
        for name in self._db.list_collection_names():
            # 获取集合统计信息
            stats = self._db.command('collStats', name)
            collections.append({
                'name': name,
                'type': 'collection',
                'count': stats.get('count', 0),
                'size': stats.get('size', 0)
            })
        
        return collections
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """获取集合结构（通过采样推断）"""
        if not self._client:
            self.connect()
        
        if not self._db:
            return {'name': table_name, 'columns': [], 'row_count': 0}
        
        collection = self._db[table_name]
        
        # 采样文档来推断字段
        sample_size = 100
        samples = list(collection.find().limit(sample_size))
        
        # 统计字段
        field_stats = {}
        for doc in samples:
            self._analyze_document(doc, field_stats)
        
        # 转换为列信息
        columns = []
        for field_name, stats in field_stats.items():
            most_common_type = max(stats['types'], key=stats['types'].get)
            columns.append({
                'name': field_name,
                'type': most_common_type,
                'nullable': stats['null_count'] > 0,
                'primary_key': field_name == '_id',
                'sample_count': stats['count']
            })
        
        # 获取文档数量
        row_count = collection.count_documents({})
        
        # 获取索引信息
        indexes = []
        for index in collection.list_indexes():
            indexes.append({
                'name': index['name'],
                'keys': list(index['key'].keys()),
                'unique': index.get('unique', False)
            })
        
        return {
            'name': table_name,
            'columns': columns,
            'indexes': indexes,
            'row_count': row_count
        }
    
    def _analyze_document(self, doc: Dict, field_stats: Dict, prefix: str = ''):
        """分析文档结构"""
        for key, value in doc.items():
            field_name = f"{prefix}{key}" if prefix else key
            
            if field_name not in field_stats:
                field_stats[field_name] = {
                    'count': 0,
                    'null_count': 0,
                    'types': {}
                }
            
            stats = field_stats[field_name]
            stats['count'] += 1
            
            if value is None:
                stats['null_count'] += 1
                type_name = 'null'
            else:
                type_name = type(value).__name__
            
            stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
            
            # 递归处理嵌套文档
            if isinstance(value, dict):
                self._analyze_document(value, field_stats, f"{field_name}.")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """执行查询（MongoDB 使用 find）"""
        if not self._client:
            self.connect()
        
        if not self._db:
            return []
        
        # 解析简单的查询格式: collection_name:filter_json
        if ':' in query:
            parts = query.split(':', 1)
            collection_name = parts[0].strip()
            filter_str = parts[1].strip() if len(parts) > 1 else '{}'
        else:
            collection_name = query.strip()
            filter_str = '{}'
        
        import json
        try:
            filter_dict = json.loads(filter_str)
        except:
            filter_dict = {}
        
        collection = self._db[collection_name]
        results = list(collection.find(filter_dict).limit(1000))
        
        # 转换 ObjectId 为字符串
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        return results
    
    def insert_data(self, table_name: str, data: List[Dict]) -> Tuple[bool, int, Optional[str]]:
        """插入数据"""
        if not data:
            return True, 0, None
        
        if not self._client:
            self.connect()
        
        if not self._db:
            return False, 0, "未指定数据库"
        
        try:
            collection = self._db[table_name]
            
            # 移除 _id 字段（如果存在且为空）
            clean_data = []
            for doc in data:
                clean_doc = {k: v for k, v in doc.items() if k != '_id' or v}
                clean_data.append(clean_doc)
            
            result = collection.insert_many(clean_data)
            inserted = len(result.inserted_ids)
            
            return True, inserted, None
        except Exception as e:
            return False, 0, str(e)
    
    def create_collection(self, collection_name: str, options: Dict = None) -> Tuple[bool, Optional[str]]:
        """创建集合"""
        if not self._client:
            self.connect()
        
        if not self._db:
            return False, "未指定数据库"
        
        try:
            self._db.create_collection(collection_name, **(options or {}))
            return True, None
        except Exception as e:
            # 集合已存在不算错误
            if 'already exists' in str(e):
                return True, None
            return False, str(e)
    
    def create_index(self, collection_name: str, keys: List[str], unique: bool = False) -> Tuple[bool, Optional[str]]:
        """创建索引"""
        if not self._client:
            self.connect()
        
        if not self._db:
            return False, "未指定数据库"
        
        try:
            collection = self._db[collection_name]
            index_keys = [(key, 1) for key in keys]
            collection.create_index(index_keys, unique=unique)
            return True, None
        except Exception as e:
            return False, str(e)
