"""
趋势分析器
"""

from datetime import datetime, timedelta
from collections import Counter

class TrendAnalyzer:
    def __init__(self, db_session):
        self.db_session = db_session
    
    def get_daily_trends(self, days=7):
        """获取每日趋势"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        from core.database.models import InternetEvent
        events = self.db_session.query(InternetEvent).filter(
            InternetEvent.date.between(start_date, end_date)
        ).all()
        
        # 分析关键词频率
        all_keywords = []
        for event in events:
            all_keywords.extend(event.keywords or [])
        
        keyword_counts = Counter(all_keywords)
        return keyword_counts.most_common(10)
    
    def get_heat_trend(self, start_date, end_date):
        """获取热度趋势"""
        from core.database.models import InternetEvent
        
        events = self.db_session.query(InternetEvent).filter(
            InternetEvent.date.between(start_date, end_date)
        ).order_by(InternetEvent.date).all()
        
        trend_data = []
        for event in events:
            trend_data.append({
                'date': event.date.isoformat(),
                'heat_score': event.heat_score,
                'title': event.title
            })
        
        return trend_data
