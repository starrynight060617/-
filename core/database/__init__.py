"""
数据库模块初始化文件
导出主要的数据库类和函数
"""

from .models import (
    Base, 
    InternetEvent, 
    init_database, 
    get_db_session
)

from .database_manager import DatabaseManager, db_manager
from .query_builder import QueryBuilder

__all__ = [
    'Base',
    'InternetEvent', 
    'init_database',
    'get_db_session',
    'DatabaseManager',
    'db_manager',
    'QueryBuilder'
]

# 模块版本信息
__version__ = '2.1.1'
__author__ = '简中互联网抽象梗日历团队'
__description__ = '数据库操作模块 - 提供事件数据的持久化存储和管理'