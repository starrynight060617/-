# scripts/check_data.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.database.models import get_db_session, InternetEvent

def check_data():
    """检查数据库中的数据"""
    session = get_db_session()
    
    try:
        # 检查事件数量
        event_count = session.query(InternetEvent).count()
        print(f"📊 数据库中的事件总数: {event_count}")
        
        # 检查具体事件
        events = session.query(InternetEvent).all()
        for event in events:
            print(f"📅 事件: {event.title} | 日期: {event.date} | ID: {event.id}")
            
        # 检查表结构
        from sqlalchemy import inspect
        inspector = inspect(session.bind)
        columns = inspector.get_columns('internet_events')
        print("🔍 internet_events 表字段:")
        for column in columns:
            print(f"   - {column['name']} ({column['type']})")
            
    except Exception as e:
        print(f"❌ 检查数据失败: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_data()