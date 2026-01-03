"""
PostgreSQL 数据库连接器
"""
from typing import List, Dict, Any, Optional, Tuple
from .base_connector import BaseConnector


class PostgreSQLConnector(BaseConnector):
    """PostgreSQL 连接器"""
    
    def __init__(
        self,
        host: str,
        port: int = 5432,
        database: str = None,
        username: str = None,
        password: str = None,
        schema: str = 'public',
        use_ssl: bool = False,
        **kwargs
    ):
        super().__init__(host, port, database, username, password, **kwargs)
        self.schema = schema
        self.use_ssl = use_ssl
    
    def connect(self) -> bool:
        """建立连接"""
        try:
            import psycopg2
            import psycopg2.extras
            
            sslmode = 'require' if self.use_ssl else 'disable'
            
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password or '',
                dbname=self.database,
                connect_timeout=10,
                sslmode=sslmode,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            return True
        except Exception as e:
            raise ConnectionError(f"PostgreSQL 连接失败: {str(e)}")
    
    def disconnect(self) -> None:
        """断开连接"""
        if self._connection:
            try:
                self._connection.close()
            except:
                pass
            self._connection = None
    
    def test_connection(self) -> Tuple[bool, str, Optional[Dict]]:
        """测试连接"""
        try:
            self.connect()
            
            cursor = self._connection.cursor()
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
            version = result['version'] if result else 'unknown'
            
            # 获取表数量
            cursor.execute("""
                SELECT COUNT(*) as count FROM information_schema.tables 
                WHERE table_schema = %s
            """, (self.schema,))
            table_count = cursor.fetchone()['count']
            
            cursor.close()
            self.disconnect()
            
            return True, f"连接成功", {
                'version': version,
                'table_count': table_count
            }
        except Exception as e:
            return False, f"连接失败: {str(e)}", None
    
    def get_tables(self) -> List[Dict[str, Any]]:
        """获取表列表"""
        if not self._connection:
            self.connect()
        
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = %s
            ORDER BY table_name
        """, (self.schema,))
        
        tables = []
        for row in cursor.fetchall():
            tables.append({
                'name': row['table_name'],
                'type': 'view' if row['table_type'] == 'VIEW' else 'table'
            })
        
        cursor.close()
        return tables
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """获取表结构"""
        if not self._connection:
            self.connect()
        
        cursor = self._connection.cursor()
        
        # 获取列信息
        cursor.execute("""
            SELECT 
                column_name, data_type, is_nullable, column_default,
                character_maximum_length, numeric_precision, numeric_scale
            FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, (self.schema, table_name))
        
        columns = []
        for row in cursor.fetchall():
            col_type = row['data_type']
            if row['character_maximum_length']:
                col_type += f"({row['character_maximum_length']})"
            elif row['numeric_precision']:
                col_type += f"({row['numeric_precision']}"
                if row['numeric_scale']:
                    col_type += f",{row['numeric_scale']}"
                col_type += ")"
            
            columns.append({
                'name': row['column_name'],
                'type': col_type,
                'nullable': row['is_nullable'] == 'YES',
                'default': row['column_default'],
                'primary_key': False  # 后面更新
            })
        
        # 获取主键信息
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.key_column_usage 
            WHERE table_schema = %s AND table_name = %s 
            AND constraint_name LIKE '%%_pkey'
        """, (self.schema, table_name))
        
        pk_columns = [row['column_name'] for row in cursor.fetchall()]
        for col in columns:
            if col['name'] in pk_columns:
                col['primary_key'] = True
        
        # 获取索引信息
        cursor.execute("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE schemaname = %s AND tablename = %s
        """, (self.schema, table_name))
        
        indexes = []
        for row in cursor.fetchall():
            indexes.append({
                'name': row['indexname'],
                'definition': row['indexdef']
            })
        
        # 获取行数估计
        cursor.execute(f'SELECT COUNT(*) as count FROM "{self.schema}"."{table_name}"')
        row_count = cursor.fetchone()['count']
        
        cursor.close()
        
        return {
            'name': table_name,
            'columns': columns,
            'indexes': indexes,
            'row_count': row_count
        }
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """执行查询"""
        if not self._connection:
            self.connect()
        
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        
        return results
    
    def insert_data(self, table_name: str, data: List[Dict]) -> Tuple[bool, int, Optional[str]]:
        """插入数据"""
        if not data:
            return True, 0, None
        
        if not self._connection:
            self.connect()
        
        try:
            cursor = self._connection.cursor()
            
            # 获取列名
            columns = list(data[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f'"{col}"' for col in columns])
            
            sql = f'INSERT INTO "{self.schema}"."{table_name}" ({column_names}) VALUES ({placeholders})'
            
            # 批量插入
            inserted = 0
            for row in data:
                values = tuple(row.get(col) for col in columns)
                cursor.execute(sql, values)
                inserted += 1
            
            self._connection.commit()
            cursor.close()
            
            return True, inserted, None
        except Exception as e:
            self._connection.rollback()
            return False, 0, str(e)
    
    def create_table(self, table_name: str, columns: List[Dict]) -> Tuple[bool, Optional[str]]:
        """创建表"""
        if not self._connection:
            self.connect()
        
        try:
            cursor = self._connection.cursor()
            
            # 构建列定义
            col_defs = []
            primary_keys = []
            
            for col in columns:
                col_def = f'"{col["name"]}" {self._map_type(col["type"])}'
                if not col.get('nullable', True):
                    col_def += ' NOT NULL'
                if col.get('primary_key'):
                    primary_keys.append(col['name'])
                col_defs.append(col_def)
            
            if primary_keys:
                col_defs.append(f'PRIMARY KEY ({", ".join([f\'"{pk}\'' for pk in primary_keys])})')
            
            sql = f'CREATE TABLE IF NOT EXISTS "{self.schema}"."{table_name}" ({", ".join(col_defs)})'
            
            cursor.execute(sql)
            self._connection.commit()
            cursor.close()
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _map_type(self, field_type: str) -> str:
        """映射字段类型到 PostgreSQL 类型"""
        type_mapping = {
            'uuid': 'UUID',
            'string': 'VARCHAR(255)',
            'text': 'TEXT',
            'integer': 'INTEGER',
            'bigint': 'BIGINT',
            'float': 'REAL',
            'double': 'DOUBLE PRECISION',
            'decimal': 'NUMERIC(10,2)',
            'boolean': 'BOOLEAN',
            'date': 'DATE',
            'datetime': 'TIMESTAMP',
            'timestamp': 'TIMESTAMP WITH TIME ZONE',
            'json': 'JSONB',
            'email': 'VARCHAR(255)',
            'phone': 'VARCHAR(20)',
            'url': 'VARCHAR(500)',
            'ip': 'INET',
        }
        return type_mapping.get(field_type.lower(), 'VARCHAR(255)')
