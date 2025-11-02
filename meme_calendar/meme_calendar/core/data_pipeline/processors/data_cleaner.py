"""
数据清洗器
"""

import re
from datetime import datetime

class DataCleaner:
    def __init__(self):
        pass
    
    def clean_text(self, text):
        """清洗文本"""
        if not text:
            return ""
        
        # 移除多余空格和特殊字符
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def normalize_date(self, date_str):
        """标准化日期"""
        try:
            if isinstance(date_str, str):
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            return date_str
        except:
            return datetime.now().date()
    
    def extract_keywords(self, text, max_keywords=5):
        """提取关键词（简化版）"""
        # 这里可以实现更复杂的关键词提取算法
        words = text.split()
        return words[:max_keywords]
