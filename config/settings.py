"""
项目配置
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MySQL 数据库配置
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root", 
    "password": "",  # ⚠️ 密码！
    "database": "meme_calendar",
    "charset": "utf8mb4"
}

# 构建 MySQL 连接 URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}?charset={MYSQL_CONFIG['charset']}"

# SQLite 备用配置（开发环境使用）
SQLITE_URL = f"sqlite:///{BASE_DIR}/storage/databases/events.db"

# 文献存储配置
LITERATURE_BASE_DIR = os.path.join(BASE_DIR, "storage", "databases", "data")
LITERATURE_EXTENSION = ".txt"

# 数据源配置
DATA_SOURCES = {
    "weibo": {"enabled": True},
    "zhihu": {"enabled": True}
}

# 界面配置
UI_CONFIG = {
    "default_window_size": "1000x700",
    "theme": "default"
}

# 数据库类型配置
USE_MYSQL = True  # 设置为 False 则使用 SQLite