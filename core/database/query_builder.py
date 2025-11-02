"""
查询构建器 - 构建复杂的数据库查询
"""

from sqlalchemy import and_, or_

class QueryBuilder:
    """查询构建器类"""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self.filters = []
        self.order_by = None
        self.limit_value = None
    
    def filter_by_date_range(self, start_date, end_date):
        """按日期范围过滤"""
        if start_date and end_date:
            self.filters.append(self.model_class.date.between(start_date, end_date))
        return self
    
    def filter_by_keyword(self, keyword):
        """按关键词过滤"""
        if keyword and keyword.strip():
            self.filters.append(
                or_(
                    self.model_class.title.contains(keyword),
                    self.model_class.description.contains(keyword)
                )
            )
        return self
    
    def filter_by_category(self, category):
        """按分类过滤"""
        if category and category.strip():
            self.filters.append(self.model_class.categories.contains([category]))
        return self
    
    def filter_by_event_type(self, event_type):
        """按事件类型过滤"""
        if event_type and event_type.strip():
            self.filters.append(self.model_class.event_type == event_type)
        return self
    
    def filter_by_heat_score(self, min_score=None, max_score=None):
        """按热度分数过滤"""
        if min_score is not None:
            self.filters.append(self.model_class.heat_score >= min_score)
        if max_score is not None:
            self.filters.append(self.model_class.heat_score <= max_score)
        return self
    
    def order_by_date(self, descending=True):
        """按日期排序"""
        if descending:
            self.order_by = self.model_class.date.desc()
        else:
            self.order_by = self.model_class.date.asc()
        return self
    
    def order_by_heat_score(self, descending=True):
        """按热度排序"""
        if descending:
            self.order_by = self.model_class.heat_score.desc()
        else:
            self.order_by = self.model_class.heat_score.asc()
        return self
    
    def limit(self, limit_value):
        """限制结果数量"""
        self.limit_value = limit_value
        return self
    
    def build(self, session):
        """构建查询"""
        query = session.query(self.model_class)
        
        # 应用过滤器
        if self.filters:
            query = query.filter(and_(*self.filters))
        
        # 应用排序
        if self.order_by:
            query = query.order_by(self.order_by)
        
        # 应用限制
        if self.limit_value:
            query = query.limit(self.limit_value)
        
        return query
    
    def build_search_query(self, keyword=None, category=None, start_date=None, end_date=None, 
                          event_type=None, min_heat=None, max_heat=None, limit=100):
        """构建完整的搜索查询"""
        self.filter_by_keyword(keyword)
        self.filter_by_category(category)
        self.filter_by_date_range(start_date, end_date)
        self.filter_by_event_type(event_type)
        self.filter_by_heat_score(min_heat, max_heat)
        self.order_by_date(descending=True)
        self.limit(limit)
        return self

# 便捷函数
def create_event_query_builder():
    """创建事件查询构建器"""
    from .models import InternetEvent
    return QueryBuilder(InternetEvent)

def build_advanced_search(session, keyword=None, category=None, start_date=None, 
                         end_date=None, event_type=None, min_heat=None, max_heat=None, 
                         limit=100, order_by='date', descending=True):
    """构建高级搜索查询"""
    from .models import InternetEvent
    
    query_builder = QueryBuilder(InternetEvent)
    query_builder.filter_by_keyword(keyword)
    query_builder.filter_by_category(category)
    query_builder.filter_by_date_range(start_date, end_date)
    query_builder.filter_by_event_type(event_type)
    query_builder.filter_by_heat_score(min_heat, max_heat)
    
    # 设置排序
    if order_by == 'date':
        query_builder.order_by_date(descending)
    elif order_by == 'heat':
        query_builder.order_by_heat_score(descending)
    
    query_builder.limit(limit)
    
    return query_builder.build(session)