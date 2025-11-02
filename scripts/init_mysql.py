"""
MySQL 数据库初始化脚本
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import pymysql
from config.settings import MYSQL_CONFIG

def init_mysql_database():
    """初始化 MySQL 数据库和表"""
    try:
        print("🔧 开始初始化 MySQL 数据库...")
        
        # 连接 MySQL 服务器（不指定数据库）
        connection = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset=MYSQL_CONFIG['charset']
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 {MYSQL_CONFIG['database']} 创建成功")
            
        connection.close()
        
        print("📊 开始创建数据表...")
        # 现在连接新创建的数据库并创建表
        from core.database.models import init_database
        init_database()
        
        print("🎉 MySQL 数据库初始化完成")
        
    except pymysql.Error as e:
        print(f"❌ MySQL 连接失败: {e}")
        print("💡 请确保：")
        print("   1. MySQL 服务正在运行")
        print("   2. 数据库配置信息正确")
        print("   3. 用户有创建数据库的权限")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")

if __name__ == "__main__":
    init_mysql_database()