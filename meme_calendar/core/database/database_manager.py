"""
数据库管理器 - MySQL 适配版本
"""

from .models import InternetEvent, get_db_session
from datetime import datetime
import os
from tkinter import messagebox
from sqlalchemy import text, inspect
from config.settings import USE_MYSQL

class DatabaseManager:
    def get_events_by_date_range(self, start_date, end_date):
        """按日期范围获取事件"""
        if not self.session and not self.connect():
            return []
        
        try:
            events = self.session.query(InternetEvent).filter(
                InternetEvent.date.between(start_date, end_date)
            ).order_by(InternetEvent.date.desc()).all()
            print(f"📅 按日期范围查询: {start_date} 到 {end_date}, 找到 {len(events)} 个事件")
            return events
        except Exception as e:
            print(f"按日期范围获取事件失败: {e}")
            # 回退到获取所有事件然后过滤
            all_events = self.get_all_events()
            filtered_events = [
                event for event in all_events 
                if hasattr(event, 'date') and event.date and start_date <= event.date <= end_date
            ]
            return filtered_events

    def __init__(self):
        self.session = None
        # 自动检查并更新数据库表结构
        self.update_database_schema()
    
    def update_database_schema(self):
        """更新数据库表结构 - 添加所有缺失的列"""
        try:
            # 先连接数据库
            if not self.connect():
                print("❌ 无法连接数据库，跳过表结构更新")
                return False
            
            # 使用 SQLAlchemy 的 Inspector 来检查表结构
            inspector = inspect(self.session.get_bind())
            columns = [col['name'] for col in inspector.get_columns('internet_events')]
            print(f"📋 当前表结构: {columns}")
            
            # 定义所有需要的列
            expected_columns = {
                'event_type': "ALTER TABLE internet_events ADD COLUMN event_type VARCHAR(20) DEFAULT 'meme'",
                'sources': "ALTER TABLE internet_events ADD COLUMN sources JSON",
                'media_urls': "ALTER TABLE internet_events ADD COLUMN media_urls JSON",
                'heat_level': "ALTER TABLE internet_events ADD COLUMN heat_level VARCHAR(20)",
                'has_literature': "ALTER TABLE internet_events ADD COLUMN has_literature BOOLEAN DEFAULT FALSE",
                'literature_path': "ALTER TABLE internet_events ADD COLUMN literature_path VARCHAR(500)",
                'created_at': "ALTER TABLE internet_events ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
                'updated_at': "ALTER TABLE internet_events ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
            }
            
            # 检查并添加缺失的列
            added_columns = []
            for col_name, sql in expected_columns.items():
                if col_name not in columns:
                    try:
                        print(f"➕ 添加缺失列: {col_name}")
                        self.session.execute(text(sql))
                        added_columns.append(col_name)
                    except Exception as e:
                        print(f"⚠️ 添加列 {col_name} 失败: {e}")
            
            if added_columns:
                self.session.commit()
                print(f"✅ 成功添加列: {added_columns}")
                
                # 重新连接以确保新的表结构生效
                self.disconnect()
                self.connect()
                
                # 验证最终表结构
                inspector = inspect(self.session.get_bind())
                final_columns = [col['name'] for col in inspector.get_columns('internet_events')]
                print(f"📊 最终表结构: {final_columns}")
            else:
                print("✅ 表结构完整，无需更新")
            
            return True
            
        except Exception as e:
            print(f"❌ 更新表结构失败: {e}")
            return False
    
    def connect(self):
        """连接数据库"""
        try:
            self.session = get_db_session()
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.session:
            self.session.close()
            self.session = None
    
    # 其他方法保持不变...
    def get_all_events(self, limit=100):
        """获取所有事件"""
        if not self.session and not self.connect():
            return []
        
        try:
            events = self.session.query(InternetEvent).order_by(
                InternetEvent.date.desc()
            ).limit(limit).all()
            return events
        except Exception as e:
            print(f"获取所有事件失败: {e}")
            return self._get_events_safe()
    
    def get_events_by_date_range(self, start_date, end_date):
        """按日期范围获取事件"""
        if not self.session and not self.connect():
            return []
        
        try:
            events = self.session.query(InternetEvent).filter(
                InternetEvent.date.between(start_date, end_date)
            ).order_by(InternetEvent.date.desc()).all()
            return events
        except Exception as e:
            print(f"按日期范围获取事件失败: {e}")
            return self._get_events_by_date_range_safe(start_date, end_date)
    
    def _get_events_safe(self):
        """安全的事件查询 - 使用原始 SQL 只查询基本字段"""
        try:
            if USE_MYSQL:
                sql = text("""
                    SELECT id, date, title, description, heat_score, 
                           COALESCE(categories, '[]') as categories, 
                           COALESCE(keywords, '[]') as keywords
                    FROM internet_events 
                    ORDER BY date DESC 
                    LIMIT 100
                """)
            else:
                sql = text("""
                    SELECT id, date, title, description, heat_score, 
                           COALESCE(categories, '[]') as categories, 
                           COALESCE(keywords, '[]') as keywords
                    FROM internet_events 
                    ORDER BY date DESC 
                    LIMIT 100
                """)
            
            result = self.session.execute(sql)
            
            events = []
            for row in result:
                event = self._create_safe_event(row)
                events.append(event)
            
            return events
        except Exception as e:
            print(f"安全查询失败: {e}")
            return []
    
    def _get_events_by_date_range_safe(self, start_date, end_date):
        """安全的日期范围查询 - 使用原始 SQL"""
        try:
            if USE_MYSQL:
                sql = text("""
                    SELECT id, date, title, description, heat_score, 
                           COALESCE(categories, '[]') as categories, 
                           COALESCE(keywords, '[]') as keywords
                    FROM internet_events 
                    WHERE date BETWEEN :start_date AND :end_date
                    ORDER BY date DESC
                """)
            else:
                sql = text("""
                    SELECT id, date, title, description, heat_score, 
                           COALESCE(categories, '[]') as categories, 
                           COALESCE(keywords, '[]') as keywords
                    FROM internet_events 
                    WHERE date BETWEEN :start_date AND :end_date
                    ORDER BY date DESC
                """)
            
            result = self.session.execute(sql, {
                'start_date': start_date, 
                'end_date': end_date
            })
            
            events = []
            for row in result:
                event = self._create_safe_event(row)
                events.append(event)
            
            return events
        except Exception as e:
            print(f"安全日期范围查询失败: {e}")
            return []
    
    def _create_safe_event(self, row):
        """创建安全事件对象"""
        event = type('SafeEvent', (), {})()
        event.id = row[0]
        event.date = row[1]
        event.title = row[2]
        event.description = row[3] or ""
        event.heat_score = row[4] if row[4] is not None else 50
        
        # 处理 JSON 字段
        try:
            import json
            event.categories = json.loads(row[5]) if row[5] else []
            event.keywords = json.loads(row[6]) if row[6] else []
        except:
            event.categories = []
            event.keywords = []
        
        # 设置默认值
        event.event_type = "meme"
        event.sources = []
        event.media_urls = []
        event.heat_level = "medium"
        event.has_literature = False
        event.literature_path = None
        
        return event
    
    def search_events(self, keyword=None, category=None):
        """搜索事件"""
        if not self.session and not self.connect():
            return []
        
        try:
            query = self.session.query(InternetEvent)
            
            if keyword and keyword.strip():
                keyword = keyword.strip()
                query = query.filter(
                    InternetEvent.title.contains(keyword) |
                    InternetEvent.description.contains(keyword)
                )
            
            if category and category.strip() and category != "全部":
                category = category.strip()
                query = query.filter(InternetEvent.categories.contains([category]))
            
            results = query.order_by(InternetEvent.date.desc()).all()
            return results
            
        except Exception as e:
            print(f"搜索事件失败: {e}")
            return self._search_events_safe(keyword, category)
    
    def _search_events_safe(self, keyword=None, category=None):
        """安全搜索 - 使用原始 SQL"""
        try:
            sql = """
                SELECT id, date, title, description, heat_score, 
                       COALESCE(categories, '[]') as categories, 
                       COALESCE(keywords, '[]') as keywords
                FROM internet_events WHERE 1=1
            """
            params = {}
            
            if keyword and keyword.strip():
                sql += " AND (title LIKE :keyword OR description LIKE :keyword)"
                params['keyword'] = f'%{keyword}%'
            
            sql += " ORDER BY date DESC"
            
            results = self.session.execute(text(sql), params)
            
            events = []
            for row in results:
                event = self._create_safe_event(row)
                events.append(event)
            
            return events
        except Exception as e:
            print(f"安全搜索失败: {e}")
            return []
    
    def search_events_safe(self, keyword=None, category=None):
        """安全的搜索方法"""
        try:
            return self.search_events(keyword, category)
        except Exception as e:
            print(f"搜索过程中发生错误: {e}")
            return []
    
    def get_event_with_literature(self, event_id):
        """获取事件及其文献内容"""
        if not self.session and not self.connect():
            return None, None
        
        try:
            event = self.session.query(InternetEvent).get(event_id)
            if event and getattr(event, 'has_literature', False):
                literature_content = event.get_literature_content()
                return event, literature_content
            return event, None
        except Exception as e:
            print(f"获取事件文献失败: {e}")
            return None, None
    
    def add_event(self, event_data):
        """添加新事件"""
        if not self.session and not self.connect():
            return False, "数据库连接失败"
        
        try:
            from uuid import uuid4
            event_id = f"event_{uuid4().hex[:8]}"
            
            new_event = InternetEvent(
                id=event_id,
                date=event_data['date'],
                title=event_data['title'],
                description=event_data.get('description', ''),
                event_type=event_data.get('event_type', 'meme'),
                categories=event_data.get('categories', []),
                keywords=event_data.get('keywords', []),
                heat_level=event_data.get('heat_level', 'medium'),
                heat_score=event_data.get('heat_score', 50),
                sources=event_data.get('sources', ['手动添加']),
                media_urls=event_data.get('media_urls', []),
                has_literature=event_data.get('has_literature', False),
                literature_path=event_data.get('literature_path')
            )
            
            self.session.add(new_event)
            self.session.commit()
            print(f"✅ 成功添加事件: {event_data['title']}")
            return True, "添加成功"
        except Exception as e:
            error_msg = f"添加事件失败: {str(e)}"
            print(error_msg)
            if self.session:
                self.session.rollback()
            return False, error_msg
    
    def update_event(self, event_id, event_data):
        """更新事件"""
        if not self.session and not self.connect():
            return False
        
        try:
            event = self.session.query(InternetEvent).get(event_id)
            if not event:
                return False
            
            for key, value in event_data.items():
                if hasattr(event, key):
                    setattr(event, key, value)
            
            event.updated_at = datetime.now()
            self.session.commit()
            print(f"✅ 成功更新事件: {event_id}")
            return True
        except Exception as e:
            print(f"更新事件失败: {e}")
            if self.session:
                self.session.rollback()
            return False
    
    def delete_event(self, event_id):
        """删除事件"""
        if not self.session and not self.connect():
            return False
        
        try:
            event = self.session.query(InternetEvent).get(event_id)
            if event:
                if getattr(event, 'has_literature', False) and getattr(event, 'literature_path', None):
                    try:
                        from config.settings import LITERATURE_BASE_DIR
                        file_path = os.path.join(LITERATURE_BASE_DIR, event.literature_path)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"✅ 已删除文献文件: {event.literature_path}")
                    except Exception as e:
                        print(f"删除文献文件失败: {e}")
                
                self.session.delete(event)
                self.session.commit()
                print(f"✅ 成功删除事件: {event_id}")
                return True
            return False
        except Exception as e:
            print(f"删除事件失败: {e}")
            if self.session:
                self.session.rollback()
            return False
    
    def check_database_health(self):
        """检查数据库健康状态"""
        try:
            if not self.session and not self.connect():
                return False, "无法连接数据库"
            
            # 使用 SQLAlchemy 的 Inspector 检查表是否存在
            inspector = inspect(self.session.get_bind())
            table_exists = 'internet_events' in inspector.get_table_names()
            
            if not table_exists:
                return False, "表不存在"
            
            result = self.session.execute(text("SELECT COUNT(*) FROM internet_events"))
            count = result.scalar()
            
            return True, f"数据库正常，共有 {count} 条记录"
            
        except Exception as e:
            return False, f"数据库检查失败: {e}"

# 全局数据库管理器实例
db_manager = DatabaseManager()