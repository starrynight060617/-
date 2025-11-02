"""
项目配置
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据库配置
DATABASE_URL = f"sqlite:///{BASE_DIR}/storage/databases/events.db"

# 数据源配置
DATA_SOURCES = {
    "weibo": {
        "enabled": True,
        "api_key": os.getenv("WEIBO_API_KEY", ""),
        "update_interval": 3600
    },
    "zhihu": {
        "enabled": True, 
        "api_key": os.getenv("ZHIHU_API_KEY", ""),
        "update_interval": 1800
    }
}

# 应用配置
APP_CONFIG = {
    "name": "简中互联网抽象梗日历",
    "version": "1.0.0",
    "debug": True,
    "host": "0.0.0.0",
    "port": 8000
}

# UI配置
UI_CONFIG = {
    "theme": "default",
    "language": "zh-CN",
    "page_size": 20
}
