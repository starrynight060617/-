import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

class MemeCalendarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("简中互联网大事件日历 🗓️")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="🗓️ 简中互联网大事件日历", 
            font=("微软雅黑", 24, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 30))
        
        # 副标题
        subtitle_label = ttk.Label(
            main_frame,
            text="记录、分析和可视化简中互联网的热点事件与历史大事",
            font=("微软雅黑", 12),
            foreground="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # 功能按钮框架
        self.create_function_buttons(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_function_buttons(self, parent):
        """创建功能按钮网格"""
        # 按钮配置 - 9个核心功能
        button_configs = [
            {
                "text": "📅 日历视图",
                "command": self.open_calendar_view,
                "description": "按日期浏览热点事件",
                "color": "#3498db"
            },
            {
                "text": "📅 同年今日", 
                "command": self.open_same_day_history,
                "description": "历史上的今天发生了什么",
                "color": "#e74c3c"
            },
            {
                "text": "🔍 事件搜索",
                "command": self.open_event_search,
                "description": "关键词搜索事件",
                "color": "#2ecc71"
            },
            {
                "text": "🏛️ 万神殿",
                "command": self.open_hall_of_fame,
                "description": "记录历史名人，永垂不朽", 
                "color": "#9b59b6"
            },
            {
                "text": "🎭 梗图生成",
                "command": self.open_meme_generator,
                "description": "生成抽象梗图",
                "color": "#f39c12"
            },
            {
                "text": "📋 数据管理",
                "command": self.open_data_management,
                "description": "管理事件数据库",
                "color": "#1abc9c"
            },
            {
                "text": "🌐 网络采集",
                "command": self.open_web_collection,
                "description": "自动采集热点事件",
                "color": "#d35400"
            },
            {
                "text": "📱 导出分享",
                "command": self.open_export_share,
                "description": "导出日历和报告",
                "color": "#27ae60"
            },
            {
                "text": "⚙️ 系统设置",
                "command": self.open_settings,
                "description": "配置系统参数",
                "color": "#95a5a6"
            }
        ]
        
        # 创建3x3按钮网格
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, config in enumerate(button_configs):
            row = i // 3
            col = i % 3
            
            # 按钮容器
            btn_container = ttk.Frame(button_frame, padding="10")
            btn_container.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # 功能按钮
            btn = tk.Button(
                btn_container,
                text=config["text"],
                command=config["command"],
                font=("微软雅黑", 14, "bold"),
                bg=config["color"],
                fg="white",
                width=12,
                height=2,
                cursor="hand2",
                relief="raised",
                bd=3
            )
            btn.pack(pady=(0, 8))
            
            # 功能描述
            desc_label = ttk.Label(
                btn_container,
                text=config["description"],
                font=("微软雅黑", 9),
                foreground="#666666",
                wraplength=120
            )
            desc_label.pack()
            
            # 配置网格权重
            button_frame.columnconfigure(col, weight=1)
            button_frame.rowconfigure(row, weight=1)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent, relief="sunken", padding="5")
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 事件统计
        event_count = self.get_event_count()
        status_text = f"📊 系统就绪 - 数据库连接: {'正常' if event_count >= 0 else '异常'}"
        
        self.status_label = ttk.Label(
            status_frame, 
            text=status_text,
            font=("微软雅黑", 9),
            foreground="#2c3e50"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 版本信息
        version_label = ttk.Label(
            status_frame,
            text="版本 2.2.0 | 简中互联网大事件日历",
            font=("微软雅黑", 9),
            foreground="#7f8c8d"
        )
        version_label.pack(side=tk.RIGHT)
    
    def get_event_count(self):
        """获取事件数量"""
        try:
            from core.database.database_manager import db_manager
            if db_manager.connect():
                events = db_manager.get_all_events(limit=10)
                db_manager.disconnect()
                return len(events)
        except:
            pass
        return -1
    
    # ==================== 功能方法 ====================
    
    def open_calendar_view(self):
        """打开日历视图"""
        try:
            # 修复：使用正确的导入路径
            from ui.desktop.ttk_app.calendar_view import CalendarView
            CalendarView(self.root)
        except ImportError as e:
            messagebox.showerror("错误", f"无法打开日历视图: {e}")
    
    def open_same_day_history(self):
        """打开同年今日"""
        messagebox.showinfo("功能提示", "📅 即将打开同年今日\n\n查看历史上的今天发生了哪些重要事件")
    
    def open_event_search(self):
        """打开事件搜索"""
        messagebox.showinfo("功能提示", "🔍 即将打开事件搜索\n\n支持按关键词、日期范围、分类等多种方式搜索事件")
    
    def open_hall_of_fame(self):
        """打开万神殿"""
        messagebox.showinfo("功能提示", "🏛️ 即将打开万神殿\n\n浏览历史名人记录，了解永垂不朽的人物事迹")
    
    def open_meme_generator(self):
        """打开梗图生成器"""
        messagebox.showinfo("功能提示", "🎭 即将打开梗图生成器\n\n根据热点事件自动生成抽象梗图和表情包")
    
    def open_data_management(self):
        """打开数据管理"""
        try:
            # 修复：使用正确的导入路径
            from ui.desktop.ttk_app.data_manager import DataManager
            DataManager(self.root)
        except ImportError as e:
            messagebox.showerror("错误", f"无法打开数据管理模块: {e}")
    
    def open_web_collection(self):
        """打开网络采集"""
        messagebox.showinfo("功能提示", "🌐 即将打开网络采集\n\n自动从各大平台采集热点事件和流行梗")
    
    def open_export_share(self):
        """打开导出分享"""
        messagebox.showinfo("功能提示", "📱 即将打开导出分享\n\n导出日历、生成报告、分享到社交媒体")
    
    def open_settings(self):
        """打开系统设置"""
        messagebox.showinfo("功能提示", "⚙️ 即将打开系统设置\n\n配置数据源、界面主题、更新设置等系统参数")
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    # 设置样式
    try:
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
    
    app = MemeCalendarApp()
    app.run()