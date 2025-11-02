"""
数据模型定义
"""

from sqlalchemy import create_engine, Column, String, Integer, Date, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class InternetEvent(Base):
    __tablename__ = "internet_events"
    
    id = Column(String(64), primary_key=True)
    date = Column(Date, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_type = Column(String(20), default="meme")
    categories = Column(JSON)
    keywords = Column(JSON)
    heat_level = Column(String(20))
    heat_score = Column(Integer, default=0)
    sources = Column(JSON)
    media_urls = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'categories': self.categories or [],
            'keywords': self.keywords or [],
            'heat_level': self.heat_level,
            'heat_score': self.heat_score,
            'sources': self.sources or [],
            'media_urls': self.media_urls or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def init_database():
    """初始化数据库"""
    from config.settings import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

def get_db_session():
    """获取数据库会话"""
    return init_database()()
