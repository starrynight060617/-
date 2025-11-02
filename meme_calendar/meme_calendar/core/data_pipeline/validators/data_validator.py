"""
数据验证器
"""

class DataValidator:
    def __init__(self):
        pass
    
    def validate_event(self, event_data):
        """验证事件数据"""
        errors = []
        
        if not event_data.get('title'):
            errors.append('标题不能为空')
        
        if not event_data.get('date'):
            errors.append('日期不能为空')
        
        if len(event_data.get('title', '')) > 200:
            errors.append('标题长度不能超过200字符')
        
        return len(errors) == 0, errors
    
    def validate_heat_score(self, heat_score):
        """验证热度分数"""
        return 0 <= heat_score <= 100
