"""
数据模型定义 - MySQL 适配版本 (扩展版)
"""

from sqlalchemy import create_engine, Column, String, Integer, Date, Text, JSON, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from config.settings import DATABASE_URL, SQLITE_URL, USE_MYSQL

Base = declarative_base()

class InternetEvent(Base):
    __tablename__ = "internet_events"
    
    id = Column(String(64), primary_key=True)  # 格式: 20251025001
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
    
    # 新增字段：是否有文献
    has_literature = Column(Boolean, default=False)
    # 新增字段：文献文件路径（相对路径）
    literature_path = Column(String(500))
    
    # 新增字段：事件梗图URL
    meme_image_url = Column(String(500))
    # 新增字段：事件详细概述
    detailed_overview = Column(Text)
    
    # 新增字段：关联的名人ID
    figure_id = Column(String(64), ForeignKey('pantheon_figures.id'))
    # 关联关系
    figure = relationship("PantheonFigure", back_populates="events")

    def get_literature_content(self):
        """获取文献内容"""
        if not self.has_literature or not self.literature_path:
            return None
        
        try:
            from config.settings import LITERATURE_BASE_DIR
            file_path = os.path.join(LITERATURE_BASE_DIR, self.literature_path)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"读取文献失败: {e}")
        
        return None

    def save_literature_content(self, content):
        """保存文献内容"""
        try:
            from config.settings import LITERATURE_BASE_DIR, LITERATURE_EXTENSION
            
            # 确保目录存在
            os.makedirs(LITERATURE_BASE_DIR, exist_ok=True)
            
            # 生成文献文件名
            filename = f"{self.id}{LITERATURE_EXTENSION}"
            file_path = os.path.join(LITERATURE_BASE_DIR, filename)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 更新数据库记录
            self.has_literature = True
            self.literature_path = filename
            return True
            
        except Exception as e:
            print(f"保存文献失败: {e}")
            return False


class PantheonFigure(Base):
    __tablename__ = "pantheon_figures"
    
    id = Column(String(64), primary_key=True)  # 格式: 20251025001
    name = Column(String(100), nullable=False, index=True)
    alias = Column(JSON)  # 别名/昵称列表
    birth_date = Column(Date)
    birth_place = Column(String(200))
    description = Column(Text)  # 人物简介
    bio = Column(Text)  # 详细生平
    
    # 分类标签
    categories = Column(JSON)  # ["互联网名人", "企业家", "网红", "学者"等]
    tags = Column(JSON)  # 个性化标签
    
    # 影响力指标
    influence_score = Column(Integer, default=0)  # 影响力评分
    popularity_level = Column(String(20))  # 知名度等级
    
    # 媒体资源
    avatar_url = Column(String(500))  # 头像URL
    media_urls = Column(JSON)  # 相关图片/视频链接
    
    # 元数据
    is_active = Column(Boolean, default=True)  # 是否活跃人物
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    events = relationship("InternetEvent", back_populates="figure")
    artifacts = relationship("HistoricalArtifact", back_populates="figure")
    timelines = relationship("FigureTimeline", back_populates="figure")


class HistoricalArtifact(Base):
    __tablename__ = "historical_artifacts"
    
    id = Column(String(64), primary_key=True)  # 格式: 20251025001
    figure_id = Column(String(64), ForeignKey('pantheon_figures.id'), nullable=False)
    
    name = Column(String(200), nullable=False)  # 物品名称
    artifact_type = Column(String(50))  # 物品类型：名言、作品、发明、事件等
    content = Column(Text)  # 内容（名言文本、作品描述等）
    
    # 时间信息
    occurrence_date = Column(Date)  # 发生/创作日期
    date_accuracy = Column(String(20))  # 日期准确性：exact, approximate, unknown
    
    # 来源和验证
    source = Column(String(500))  # 来源说明
    is_verified = Column(Boolean, default=False)  # 是否已验证
    
    # 影响力
    significance_level = Column(String(20))  # 重要性等级
    impact_description = Column(Text)  # 影响描述
    
    # 媒体资源
    media_urls = Column(JSON)  # 相关图片/视频/文档链接
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    figure = relationship("PantheonFigure", back_populates="artifacts")


class FigureTimeline(Base):
    __tablename__ = "figure_timelines"
    
    id = Column(String(64), primary_key=True)  # 格式: 20251025001
    figure_id = Column(String(64), ForeignKey('pantheon_figures.id'), nullable=False)
    
    year = Column(Integer, nullable=False)  # 年份
    event_title = Column(String(300), nullable=False)  # 事件标题
    event_description = Column(Text)  # 事件详细描述
    importance = Column(String(20))  # 重要性：major, minor
    
    # 分类
    event_type = Column(String(50))  # 事件类型：birth, career, achievement, controversy等
    
    # 来源
    source = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    figure = relationship("PantheonFigure", back_populates="timelines")


class HistoricalEvent(Base):
    __tablename__ = "historical_events"
    
    id = Column(String(64), primary_key=True)  # 格式: 20251025001
    date = Column(Date, nullable=False, index=True)  # 事件发生日期
    title = Column(String(300), nullable=False)  # 事件标题
    description = Column(Text)  # 事件描述
    
    # 分类信息
    event_type = Column(String(50))  # 事件类型：historical, cultural, political, scientific
    categories = Column(JSON)  # 分类标签
    importance_level = Column(String(20))  # 重要性等级
    
    # 地理位置
    location = Column(String(200))  # 发生地点
    
    # 来源和验证
    source = Column(String(500))
    is_verified = Column(Boolean, default=True)
    
    # 关联信息
    related_figure_ids = Column(JSON)  # 关联的名人ID列表
    related_event_ids = Column(JSON)  # 关联的其他事件ID列表
    
    # 媒体资源
    media_urls = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# 独立的数据库初始化函数
def init_database():
    """初始化数据库"""
    from config.settings import DATABASE_URL, SQLITE_URL, USE_MYSQL
    
    # 根据配置选择数据库
    if USE_MYSQL:
        database_url = DATABASE_URL
        print("🚀 使用 MySQL 数据库")
    else:
        database_url = SQLITE_URL
        print("💾 使用 SQLite 数据库")
    
    engine = create_engine(database_url)
    
    # 创建所有表
    try:
        Base.metadata.create_all(engine)
        print("✅ 数据库表创建成功")
        
        # 输出创建的表信息
        table_names = Base.metadata.tables.keys()
        print(f"📊 已创建表: {', '.join(table_names)}")
        
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
        # 如果 MySQL 失败，回退到 SQLite
        if USE_MYSQL:
            print("🔄 回退到 SQLite 数据库")
            engine = create_engine(SQLITE_URL)
            Base.metadata.create_all(engine)
    
    return engine

def get_db_session():
    """获取数据库会话"""
    engine = init_database()
    Session = sessionmaker(bind=engine)
    return Session()