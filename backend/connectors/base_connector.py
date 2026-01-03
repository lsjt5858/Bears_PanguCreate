"""
数据库连接器基类
定义通用接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple


class BaseConnector(ABC):
    """数据库连接器基类"""
    
    def __init__(
        self,
        host: str,
        port: int,
        database: str = None,
        username: str = None,
        password: str = None,
        **kwargs
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.options = kwargs
        self._connection = None
    
    @abstractmethod
    def connect(self) -> bool:
        """建立连接"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass
    
    @abstractmethod
    def test_connection(self) -> Tuple[bool, str, Optional[Dict]]:
        """测试连接"""
        pass
    
    @abstractmethod
    def get_tables(self) -> List[Dict[str, Any]]:
        """获取表/集合列表"""
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """获取表结构"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """执行查询"""
        pass
    
    @abstractmethod
    def insert_data(self, table_name: str, data: List[Dict]) -> Tuple[bool, int, Optional[str]]:
        """插入数据"""
        pass
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
