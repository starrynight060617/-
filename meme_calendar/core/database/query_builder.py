"""
查询构建器
"""

from sqlalchemy import and_, or_
from datetime import datetime

class EventQueryBuilder:
    @staticmethod
    def build_query(session, start_date=None, end_date=None, event_type=None, 
                   category=None, keyword=None, min_heat=None, max_heat=None):
        """构建查询"""
        from .models import InternetEvent
        
        query = session.query(InternetEvent)
        
        # 日期范围筛选
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(InternetEvent.date >= start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(InternetEvent.date <= end_date)
        
        # 事件类型筛选
        if event_type:
            query = query.filter(InternetEvent.event_type == event_type)
        
        # 分类筛选
        if category:
            query = query.filter(InternetEvent.categories.contains([category]))
        
        # 关键词筛选
        if keyword:
            query = query.filter(
                or_(
                    InternetEvent.title.contains(keyword),
                    InternetEvent.description.contains(keyword),
                    InternetEvent.keywords.contains([keyword])
                )
            )
        
        # 热度筛选
        if min_heat is not None:
            query = query.filter(InternetEvent.heat_score >= min_heat)
        if max_heat is not None:
            query = query.filter(InternetEvent.heat_score <= max_heat)
        
        # 按日期降序排列
        query = query.order_by(InternetEvent.date.desc(), InternetEvent.heat_score.desc())
        
        return query
