# scripts/update_database.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.database.models import Base, init_database
from config.settings import DATABASE_URL, SQLITE_URL, USE_MYSQL
from sqlalchemy import create_engine, text

def update_database():
    """更新数据库表结构"""
    
    # 根据配置选择数据库
    if USE_MYSQL:
        database_url = DATABASE_URL
        print("🚀 使用 MySQL 数据库")
    else:
        database_url = SQLITE_URL
        print("💾 使用 SQLite 数据库")
    
    engine = create_engine(database_url)
    
    try:
        # 删除所有表（注意：这会清空所有数据！）
        Base.metadata.drop_all(engine)
        print("🗑️ 旧表删除完成")
        
        # 重新创建所有表（使用新的表结构）
        Base.metadata.create_all(engine)
        print("✅ 新表创建成功")
        
        # 输出创建的表信息
        table_names = Base.metadata.tables.keys()
        print(f"📊 当前表结构: {', '.join(table_names)}")
        
        # 显示 internet_events 表的字段
        with engine.connect() as conn:
            result = conn.execute(text("DESCRIBE internet_events"))
            columns = [row[0] for row in result]
            print(f"📋 internet_events 表字段: {columns}")
            
    except Exception as e:
        print(f"❌ 数据库更新失败: {e}")

if __name__ == "__main__":
    print("🔄 开始更新数据库表结构...")
    update_database()
    print("🎉 数据库更新完成！现在可以重新运行 init_sample_data.py 来初始化数据")