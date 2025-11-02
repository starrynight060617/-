'''
✅ 完整日期显示 - 使用 monthdatescalendar 显示整个月的所有日期，包括相邻月份
✅ 高亮选中功能 - 点击日期时高亮显示选中状态
✅ 年历缩略图 - 支持从2000年开始的年份选择
✅ 未来日期标灰 - 未来日期显示为灰色
✅ 数据范围扩展 - 加载2000年至今的事件数据
✅ 自动选中今天 - 启动时自动选中当前日期
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import calendar
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from core.database.database_manager import db_manager
    from core.database.models import InternetEvent
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"数据库导入错误: {e}")
    DATABASE_AVAILABLE = False

class CalendarView:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("📅 日历视图 - 简中互联网大事件日历")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f8f9fa')
        
        # 当前显示的日期
        self.current_date = date.today()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        
        # 选中的日期
        self.selected_date = None
        self.selected_cell = None
        
        # 数据库连接
        self.db_connected = False
        if DATABASE_AVAILABLE:
            self.db_connected = db_manager.connect()
        
        # 事件数据缓存
        self.events_data = {}
        
        self.setup_ui()
        self.load_events_data()
        self.update_calendar()
        self.go_to_today()  # 自动选中今天
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题和导航栏
        self.create_header(main_frame)
        
        # 日历主体区域
        self.create_calendar_area(main_frame)
        
        # 事件详情区域
        self.create_event_details(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """创建标题和导航栏"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 标题
        title_label = ttk.Label(
            header_frame,
            text="📅 日历视图",
            font=("微软雅黑", 20, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(side=tk.LEFT)
        
        # 导航控件
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        # 当前月份显示
        self.month_label = ttk.Label(
            nav_frame,
            text=f"{self.current_year}年{self.current_month}月",
            font=("微软雅黑", 12, "bold"),
            foreground="#e74c3c"
        )
        self.month_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # 年历缩略图按钮
        ttk.Button(
            nav_frame,
            text="📅 年历视图",
            command=self.show_year_view
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 导航按钮
        ttk.Button(
            nav_frame,
            text="◀ 上月",
            command=self.previous_month
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            nav_frame,
            text="今天",
            command=self.go_to_today
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            nav_frame,
            text="下月 ▶",
            command=self.next_month
        ).pack(side=tk.LEFT)

    def create_calendar_area(self, parent):
        """创建日历显示区域"""
        calendar_frame = ttk.LabelFrame(parent, text="🗓️ 月历视图", padding="15")
        calendar_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 创建日历网格容器
        self.calendar_container = ttk.Frame(calendar_frame)
        self.calendar_container.pack(fill=tk.BOTH, expand=True)
        
        # 初始化日历网格
        self.setup_calendar_grid()
    
    def setup_calendar_grid(self):
        """设置日历网格布局"""
        # 清空现有网格
        for widget in self.calendar_container.winfo_children():
            widget.destroy()
        
        # 创建新的网格框架
        self.calendar_grid = ttk.Frame(self.calendar_container)
        self.calendar_grid.pack(fill=tk.BOTH, expand=True)
        
        # 星期标题
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i, day in enumerate(weekdays):
            label = tk.Label(
                self.calendar_grid,
                text=day,
                font=("微软雅黑", 10, "bold"),
                foreground="#34495e",
                background="#ecf0f1",
                anchor="center",
                relief="raised",
                bd=1
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # 配置网格权重
        for i in range(7):
            self.calendar_grid.columnconfigure(i, weight=1)
        for i in range(7):  # 6行（标题+最多6周）
            self.calendar_grid.rowconfigure(i, weight=1)
    
    def create_event_details(self, parent):
        """创建事件详情区域"""
        details_frame = ttk.LabelFrame(parent, text="📋 事件详情", padding="10")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 选中日期显示
        self.selected_date_label = ttk.Label(
            details_frame,
            text="请点击日历中的日期查看事件",
            font=("微软雅黑", 11, "bold"),
            foreground="#e74c3c"
        )
        self.selected_date_label.pack(anchor="w", pady=(0, 10))
        
        # 事件列表
        event_list_frame = ttk.Frame(details_frame)
        event_list_frame.pack(fill=tk.X)
        
        # 创建树形视图显示事件
        columns = ("time", "title", "heat", "type")
        self.event_tree = ttk.Treeview(
            event_list_frame,
            columns=columns,
            show="headings",
            height=6
        )
        
        # 设置列标题
        self.event_tree.heading("time", text="时间")
        self.event_tree.heading("title", text="事件标题")
        self.event_tree.heading("heat", text="热度")
        self.event_tree.heading("type", text="类型")
        
        # 设置列宽度
        self.event_tree.column("time", width=80, anchor="center")
        self.event_tree.column("title", width=400, anchor="w")
        self.event_tree.column("heat", width=60, anchor="center")
        self.event_tree.column("type", width=80, anchor="center")
        
        # 滚动条
        event_scrollbar = ttk.Scrollbar(event_list_frame, orient=tk.VERTICAL, command=self.event_tree.yview)
        self.event_tree.configure(yscrollcommand=event_scrollbar.set)
        
        # 布局
        self.event_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        event_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件
        self.event_tree.bind('<Double-1>', self.on_event_double_click)

    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent, relief="sunken", padding="5")
        status_frame.pack(fill=tk.X)
        
        status_text = "就绪" if self.db_connected else "数据库连接失败 - 使用示例数据"
        self.status_label = ttk.Label(
            status_frame,
            text=status_text,
            font=("微软雅黑", 9),
            foreground="#2c3e50"
        )
        self.status_label.pack(side=tk.LEFT)
    
    def load_events_data(self):
        """只加载当前月的事件数据（显著节省内存）"""
        if not self.db_connected:
            self.load_sample_events()
            return

        try:
            # 计算当前月的起止日期
            start_date = date(self.current_year, self.current_month, 1)
            # 下月1号减一天得到本月末
            if self.current_month == 12:
                end_date = date(self.current_year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(self.current_year, self.current_month + 1, 1) - timedelta(days=1)

            # 从数据库获取本月事件
            events = db_manager.get_events_by_date_range(start_date, end_date)

            # 按日期组织数据
            self.events_data = {}
            for event in events:
                if hasattr(event, 'date') and event.date:
                    event_date = event.date.strftime("%Y-%m-%d")
                    if event_date not in self.events_data:
                        self.events_data[event_date] = []
                    self.events_data[event_date].append(event)

            print(f"📊 成功加载 {len(events)} 个事件，范围：{start_date} ~ {end_date}")

        except Exception as e:
            print(f"加载事件数据失败: {e}")
            self.load_sample_events()

    
    def load_sample_events(self):
        """加载示例事件数据 - 返回空数据"""
        # 直接返回空字典，不创建任何示例事件
        self.events_data = {}

    def create_sample_event(self, event_date, title, heat_score, event_type, description):
        """创建示例事件对象"""
        event = type('Event', (), {})()
        event.date = event_date
        event.title = title
        event.heat_score = heat_score
        event.event_type = event_type
        event.description = description
        event.id = f"sample_{event_date.strftime('%Y%m%d')}"
        return event

    def update_calendar(self):
        """更新日历显示 - 完整显示所有日期"""
        # 更新月份标签
        self.month_label.config(text=f"{self.current_year}年{self.current_month}月")
        
        # 清空现有日期单元格
        for widget in self.calendar_grid.winfo_children():
            if hasattr(widget, 'is_day_cell') or isinstance(widget, tk.Frame):
                grid_info = widget.grid_info()
                if grid_info and grid_info['row'] > 0:
                    widget.destroy()
        
        # 使用monthdatescalendar获取完整日期（包含相邻月份）
        cal = calendar.Calendar(firstweekday=0)  # 0=Monday
        month_weeks = cal.monthdatescalendar(self.current_year, self.current_month)
        
        # 填充日期单元格
        for week_num, week_dates in enumerate(month_weeks, 1):
            for day_num, cell_date in enumerate(week_dates):
                self.create_day_cell(week_num, day_num, cell_date)
    
    def create_day_cell(self, week_row, week_col, cell_date):
        """创建日期单元格"""
        try:
            date_str = cell_date.strftime("%Y-%m-%d")
            today = date.today()
            
            # 检查是否属于当前月份
            is_current_month = (cell_date.month == self.current_month)
            is_future_date = (cell_date > today)
            
            # 创建日期单元格框架
            cell_frame = tk.Frame(
                self.calendar_grid,
                bg='white',
                relief='raised',
                bd=1
            )
            cell_frame.grid(row=week_row, column=week_col, sticky="nsew", padx=1, pady=1)
            cell_frame.is_day_cell = True
            cell_frame.cell_date = cell_date
            
            # 日期标签
            day_label = tk.Label(
                cell_frame,
                text=str(cell_date.day),
                font=("微软雅黑", 12, "bold"),
                bg='white',
                fg='#2c3e50'
            )
            day_label.pack(anchor="nw", padx=5, pady=5)
            
            # 处理非当前月份日期
            if not is_current_month:
                cell_frame.configure(bg='#f8f9fa')
                day_label.configure(bg='#f8f9fa', fg='#bdbdbd')
            
            # 处理未来日期
            elif is_future_date:
                cell_frame.configure(bg='#f5f5f5')
                day_label.configure(bg='#f5f5f5', fg='#9e9e9e')
                
                future_info = tk.Label(
                    cell_frame,
                    text="未来",
                    font=("微软雅黑", 8),
                    bg='#f5f5f5',
                    fg='#757575'
                )
                future_info.pack(side=tk.BOTTOM, anchor="sw", padx=5, pady=2)
            
            # 处理当前月份且有事件的日期
            elif is_current_month and not is_future_date:
                events_today = self.events_data.get(date_str, [])
                
                if events_today:
                    max_heat = max(event.heat_score for event in events_today)
                    
                    # 根据热度设置颜色
                    if max_heat >= 80:
                        cell_color = "#ffebee"
                        text_color = "#c62828"
                    elif max_heat >= 60:
                        cell_color = "#fff3e0" 
                        text_color = "#ef6c00"
                    else:
                        cell_color = "#f3e5f5"
                        text_color = "#7b1fa2"
                    
                    cell_frame.configure(bg=cell_color)
                    day_label.configure(bg=cell_color, fg=text_color)
                    
                    # 显示事件信息
                    event_count = len(events_today)
                    event_info = tk.Label(
                        cell_frame,
                        text=f"📅{event_count} 🔥{max_heat}",
                        font=("微软雅黑", 8),
                        bg=cell_color,
                        fg=text_color
                    )
                    event_info.pack(side=tk.BOTTOM, anchor="sw", padx=5, pady=2)
            
            # 标记今天
            if cell_date == today:
                cell_frame.configure(relief='solid', bd=2, bg='#e3f2fd')
                day_label.configure(bg='#e3f2fd', fg='#1976d2')
            
            # 标记选中日期
            if self.selected_date and cell_date == self.selected_date:
                cell_frame.configure(relief='solid', bd=3, bg='#fff9c4')
                day_label.configure(bg='#fff9c4', fg='#f57c00')
                self.selected_cell = cell_frame
            
            # 绑定点击事件
            cell_frame.bind('<Button-1>', lambda e, d=cell_date: self.on_date_click(d))
            day_label.bind('<Button-1>', lambda e, d=cell_date: self.on_date_click(d))
            
        except ValueError as e:
            print(f"创建日期单元格错误: {e}")

    def on_date_click(self, clicked_date):
        """日期点击事件 - 支持跨月点击与安全选中"""
        # 跨月点击：若点击非当前月日期，则自动跳转月份
        if clicked_date.month != self.current_month or clicked_date.year != self.current_year:
            self.current_year = clicked_date.year
            self.current_month = clicked_date.month
            self.load_events_data()   # ⚡ 如果改成只加载当月数据，这里也要改
            self.update_calendar()
            self.status_label.config(text=f"已切换到 {self.current_year}年{self.current_month}月")
            return

        # 清除之前选中的高亮（防止 invalid command）
        if self.selected_cell and self.selected_cell.winfo_exists():
            try:
                self.selected_cell.configure(relief='raised', bd=1, bg='white')
                for child in self.selected_cell.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg='white')
            except tk.TclError:
                pass  # 安全忽略已销毁组件

        # 设置新的选中日期
        self.selected_date = clicked_date
        date_str = clicked_date.strftime("%Y年%m月%d日")
        self.selected_date_label.config(text=f"📅 {date_str} 的事件")

        # 高亮显示选中的日期
        self.highlight_selected_date(clicked_date)

        # 显示该日期的事件
        self.show_date_events(clicked_date)


    
    def highlight_selected_date(self, selected_date):
        """高亮显示选中的日期"""
        for widget in self.calendar_grid.winfo_children():
            if hasattr(widget, 'is_day_cell') and hasattr(widget, 'cell_date'):
                if widget.cell_date == selected_date:
                    widget.configure(relief='solid', bd=3, bg='#fff9c4')
                    self.selected_cell = widget
                    # 更新内部标签的背景色
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg='#fff9c4')
    
    def show_date_events(self, target_date):
        """显示指定日期的事件 - 修复显示问题"""
        # 清空现有事件
        for item in self.event_tree.get_children():
            self.event_tree.delete(item)
        
        date_str = target_date.strftime("%Y-%m-%d")
        events = self.events_data.get(date_str, [])
        
        if not events:
            self.event_tree.insert("", "end", values=("全天", "该日期暂无事件", "0%", "无"))
            return
        
        # 按热度排序
        sorted_events = sorted(events, key=lambda x: getattr(x, 'heat_score', 0), reverse=True)
        
        for event in sorted_events:
            event_time = "全天"  # 简化处理
            event_type = self.get_event_type_display(getattr(event, 'event_type', 'meme'))
            heat_score = getattr(event, 'heat_score', 0)
            
            self.event_tree.insert("", "end", values=(
                event_time,
                event.title,
                f"{heat_score}%",
                event_type
            ), tags=(getattr(event, 'id', 'sample'),))
    
    def get_event_type_display(self, event_type):
        """获取事件类型显示文本"""
        type_map = {
            "meme": "热梗",
            "social_event": "社会",
            "tech_trend": "科技",
            "policy": "政策",
            "entertainment": "娱乐"
        }
        return type_map.get(event_type, event_type)
    
    def on_event_double_click(self, event):
        """事件双击事件"""
        selection = self.event_tree.selection()
        if selection:
            item = selection[0]
            event_id = self.event_tree.item(item)['tags'][0]
            if not event_id.startswith('sample'):
                self.show_event_details(event_id)
    
    def show_event_details(self, event_id):
        """显示事件详情"""
        if not self.db_connected:
            messagebox.showinfo("事件详情", "数据库不可用，无法显示详细事件信息")
            return
        
        try:
            event = db_manager.session.query(InternetEvent).get(event_id)
            if event:
                details = f"""
📅 事件详情:

🗓️ 日期: {event.date.strftime('%Y年%m月%d日')}
📝 标题: {event.title}
🔥 热度: {event.heat_score}%
📊 类型: {self.get_event_type_display(event.event_type)}
🏷️ 分类: {', '.join(event.categories) if event.categories else '无'}
🔑 关键词: {', '.join(event.keywords) if event.keywords else '无'}

📖 描述:
{event.description}

📎 来源: {', '.join(event.sources) if event.sources else '未知'}
                """
                messagebox.showinfo("事件详情", details)
        except Exception as e:
            messagebox.showerror("错误", f"获取事件详情失败: {e}")

    def show_year_view(self):
        """显示年历缩略图快速选择窗口"""
        year_window = tk.Toplevel(self.window)
        year_window.title("📅 年历视图 - 快速选择")
        year_window.geometry("600x400")
        year_window.transient(self.window)
        year_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(year_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="📅 年历快速选择",
            font=("微软雅黑", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # 年份选择
        year_frame = ttk.Frame(main_frame)
        year_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(year_frame, text="选择年份:", font=("微软雅黑", 11)).pack(side=tk.LEFT)
        
        current_year = date.today().year
        # 生成从2000年到当前年份+1的列表
        year_range = list(range(2000, current_year + 2))
        year_var = tk.StringVar(value=str(current_year))
        year_combo = ttk.Combobox(
            year_frame,
            textvariable=year_var,
            values=[str(year) for year in year_range],
            state="readonly",
            width=10
        )
        year_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 月份网格
        month_frame = ttk.Frame(main_frame)
        month_frame.pack(fill=tk.BOTH, expand=True)
        
        months = [
            ("1月", 1), ("2月", 2), ("3月", 3),
            ("4月", 4), ("5月", 5), ("6月", 6),
            ("7月", 7), ("8月", 8), ("9月", 9),
            ("10月", 10), ("11月", 11), ("12月", 12)
        ]
        
        for i, (month_name, month_num) in enumerate(months):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                month_frame,
                text=month_name,
                font=("微软雅黑", 11),
                bg="#3498db",
                fg="white",
                width=8,
                height=2,
                cursor="hand2",
                command=lambda m=month_num: self.select_month_from_year_view(
                    int(year_var.get()), m, year_window
                )
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            month_frame.columnconfigure(col, weight=1)
            month_frame.rowconfigure(row, weight=1)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="关闭",
            command=year_window.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def select_month_from_year_view(self, year, month, year_window):
        """从年历视图选择月份"""
        self.current_year = year
        self.current_month = month
        year_window.destroy()
        
        self.load_events_data()
        self.update_calendar()
        self.status_label.config(text=f"已切换到 {year}年{month}月")
    
    def previous_month(self):
        """切换到上个月"""
        if self.current_month == 1:
            self.current_year -= 1
            self.current_month = 12
        else:
            self.current_month -= 1
        
        self.load_events_data()
        self.update_calendar()
        self.status_label.config(text=f"已切换到 {self.current_year}年{self.current_month}月")
    
    def next_month(self):
        """切换到下个月"""
        if self.current_month == 12:
            self.current_year += 1
            self.current_month = 1
        else:
            self.current_month += 1
        
        self.load_events_data()
        self.update_calendar()
        self.status_label.config(text=f"已切换到 {self.current_year}年{self.current_month}月")
    
    def go_to_today(self):
        """回到今天"""
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        
        self.load_events_data()
        self.update_calendar()
        self.status_label.config(text="已回到今天")
        
        # 自动选中今天
        self.on_date_click(today)

    def __del__(self):
        """析构函数，关闭数据库连接"""
        if DATABASE_AVAILABLE and self.db_connected:
            db_manager.disconnect()

# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    app = CalendarView(root)
    root.mainloop()