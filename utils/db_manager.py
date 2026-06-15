import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_pool()
        return cls._instance
    
    def init_pool(self):
        """初始化数据库连接参数"""
        self.config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'db': 'py_ryp',
            'charset': 'utf8',
            'cursorclass': DictCursor
        }
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = pymysql.connect(**self.config)
            yield conn
        finally:
            if conn:
                conn.close()

db = DatabaseManager() 