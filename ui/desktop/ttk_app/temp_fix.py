import tkinter as tk 
from tkinter import ttk, messagebox, scrolledtext, filedialog 
from datetime import datetime, date 
import os 
import sys 
 
# 添加项目根目录到Python路径 
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')) 
 
try: 
    from core.database.database_manager import db_manager 
    from core.database.models import InternetEvent  
    DATABASE_AVAILABLE = True 
except ImportError as e: 
    print(f"数据库导入错误: {e}") 
    DATABASE_AVAILABLE = False 
