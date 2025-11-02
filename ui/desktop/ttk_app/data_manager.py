import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
import os
import sys

# 添加正确的项目根目录路径
project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
sys.path.insert(0, project_root)

try:
    from core.database.database_manager import db_manager
    from core.database.models import InternetEvent
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"数据库导入错误: {e}")
    DATABASE_AVAILABLE = False

class DataManager:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("📋 数据管理 - 简中互联网大事件日历")
        self.window.geometry("1000x700")
        
        # 连接数据库
        self.db_connected = False
        if DATABASE_AVAILABLE:
            self.db_connected = db_manager.connect()
        
        # 当前选中的事件
        self.selected_event = None
        
        self.setup_ui()
        self.load_events()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题栏
        self.create_title_bar(main_frame)
        
        # 搜索和筛选区域
        self.create_search_area(main_frame)
        
        # 数据表格区域
        self.create_data_table(main_frame)
        
        # 操作按钮区域
        self.create_action_buttons(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_title_bar(self, parent):
        """创建标题栏"""
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="📋 事件数据管理",
            font=("微软雅黑", 18, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(side=tk.LEFT)
        
        # 统计信息
        self.stats_label = ttk.Label(
            title_frame,
            text="加载中...",
            font=("微软雅黑", 10),
            foreground="#7f8c8d"
        )
        self.stats_label.pack(side=tk.RIGHT)
    
    def create_search_area(self, parent):
        """创建搜索和筛选区域"""
        search_frame = ttk.LabelFrame(parent, text="🔍 搜索和筛选", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 第一行：关键词搜索
        keyword_row = ttk.Frame(search_frame)
        keyword_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(keyword_row, text="关键词:", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(keyword_row, width=30, font=("微软雅黑", 10))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.search_entry.bind('<Return>', lambda e: self.search_events())
        
        ttk.Button(
            keyword_row, 
            text="🔍 搜索", 
            command=self.search_events,
            width=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            keyword_row,
            text="🔄 重置",
            command=self.reset_keyword_search,
            width=8
        ).pack(side=tk.LEFT)
        
        # 第二行：分类搜索
        category_row = ttk.Frame(search_frame)
        category_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(category_row, text="分类:", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.category_entry = ttk.Entry(category_row, width=30, font=("微软雅黑", 10))
        self.category_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.category_entry.bind('<Return>', lambda e: self.search_events())
        
        ttk.Button(
            category_row, 
            text="🔍 搜索", 
            command=self.search_events,
            width=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            category_row,
            text="🔄 重置",
            command=self.reset_category_search,
            width=8
        ).pack(side=tk.LEFT)

    def create_data_table(self, parent):
        """创建数据表格"""
        table_frame = ttk.LabelFrame(parent, text="📊 事件列表", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 创建树形视图
        columns = ("date", "title", "type", "categories", "heat_score", "has_literature")
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns,
            show="headings",
            height=15
        )
        
        # 设置列标题
        self.tree.heading("date", text="日期")
        self.tree.heading("title", text="事件标题")
        self.tree.heading("type", text="类型")
        self.tree.heading("categories", text="分类")
        self.tree.heading("heat_score", text="热度")
        self.tree.heading("has_literature", text="文献")
        
        # 设置列宽度
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("title", width=350, anchor="w")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("categories", width=120, anchor="center")
        self.tree.column("heat_score", width=80, anchor="center")
        self.tree.column("has_literature", width=60, anchor="center")
        
        # 滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.tree.bind('<Double-1>', self.on_item_double_click)
    
    def create_action_buttons(self, parent):
        """创建操作按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [
            ("➕ 添加事件", self.add_event, "#27ae60"),
            ("✏️ 编辑事件", self.edit_event, "#3498db"),
            ("🗑️ 删除事件", self.delete_event, "#e74c3c"),
            ("📖 查看文献", self.view_literature, "#9b59b6"),
            ("📥 导入数据", self.import_data, "#f39c12"),
            ("📤 导出数据", self.export_data, "#95a5a6"),
            ("🔄 刷新数据", self.refresh_data, "#1abc9c")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("微软雅黑", 10),
                bg=color,
                fg="white",
                width=12,
                height=1,
                cursor="hand2",
                relief="raised",
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent, relief="sunken", padding="5")
        status_frame.pack(fill=tk.X)
        
        status_text = "数据库连接正常" if self.db_connected else "数据库连接失败 - 使用示例数据"
        self.status_label = ttk.Label(
            status_frame,
            text=status_text,
            font=("微软雅黑", 9),
            foreground="#2c3e50"
        )
        self.status_label.pack(side=tk.LEFT)
    
    def load_events(self, events=None):
        """加载事件到表格"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 如果没有传入events参数，从数据库加载
        if events is None:
            if not self.db_connected:
                self.load_sample_data()
                return
            
            try:
                events = db_manager.get_all_events(limit=100)
            except Exception as e:
                print(f"从数据库加载事件失败: {e}")
                self.load_sample_data()
                return
        
        try:
            # 填充数据
            for event in events:
                has_lit = "✅" if getattr(event, 'has_literature', False) else "❌"
                
                # 处理分类显示
                categories = getattr(event, 'categories', [])
                if isinstance(categories, list):
                    categories_display = ", ".join(categories)
                else:
                    categories_display = str(categories)
                
                self.tree.insert("", "end", values=(
                    event.date.strftime("%Y-%m-%d") if hasattr(event, 'date') and event.date else "",
                    event.title,
                    self.get_event_type_display(getattr(event, 'event_type', 'meme')),
                    categories_display,
                    f"{getattr(event, 'heat_score', 0)}%",
                    has_lit
                ), tags=(str(event.id),))  # 确保ID是字符串
                
            # 更新统计信息
            self.update_stats(len(events))
            
        except Exception as e:
            print(f"加载数据到表格失败: {e}")
            self.load_sample_data()

    def load_sample_data(self):
        """加载示例数据 - 返回空数据"""
        # 不插入任何示例数据
        sample_events = []
        
        for event in sample_events:
            self.tree.insert("", "end", values=event[:6], tags=(event[6],))
        
        self.update_stats(0)  # 更新统计为0

    def get_event_type_display(self, event_type):
        """获取事件类型显示文本"""
        type_map = {
            "meme": "热梗",
            "social_event": "社会事件",
            "tech_trend": "科技趋势",
            "policy": "政策",
            "entertainment": "娱乐"
        }
        return type_map.get(event_type, event_type)
    
    def update_stats(self, count):
        """更新统计信息"""
        self.stats_label.config(text=f"共 {count} 个事件")
    
    def search_events(self):
        """搜索事件 - 优化错误处理"""
        if not self.db_connected:
            messagebox.showinfo("提示", "数据库不可用，搜索功能受限")
            return
        
        keyword = self.search_entry.get().strip()
        category = self.category_entry.get().strip()
        
        try:
            # 使用安全的搜索方法
            events = db_manager.search_events_safe(keyword=keyword, category=category)
            
            if events:
                self.load_events(events)
                self.status_label.config(text=f"搜索完成，找到 {len(events)} 个事件")
            else:
                self.load_events([])
                self.status_label.config(text="未找到匹配的事件")
                
        except Exception as e:
            print(f"搜索错误: {e}")
            self.status_label.config(text="搜索过程中发生错误")

    def reset_keyword_search(self):
        """重置关键词搜索"""
        self.search_entry.delete(0, tk.END)
        self.search_events()
    
    def reset_category_search(self):
        """重置分类搜索"""
        self.category_entry.delete(0, tk.END)
        self.search_events()
    
    def reset_search(self):
        """重置所有搜索条件"""
        self.search_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.load_events()
        self.status_label.config(text="搜索条件已重置")
    
    def on_item_select(self, event):
        """选中事件"""
        if not self.db_connected:
            return
            
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            event_id = self.tree.item(item)['tags'][0]
            # 修复：检查是否为字符串类型，避免 startswith 错误
            if isinstance(event_id, str) and not event_id.startswith('sample_'):
                try:
                    self.selected_event = db_manager.session.query(InternetEvent).get(event_id)
                    print(f"DEBUG: 选中事件 ID: {event_id}, 标题: {self.selected_event.title if self.selected_event else 'None'}")
                except Exception as e:
                    print(f"获取事件失败: {e}")
                    self.selected_event = None
    
    def on_item_double_click(self, event):
        """双击事件 - 显示文献详情"""
        if not self.db_connected:
            messagebox.showinfo("提示", "数据库不可用，无法查看详情")
            return
        
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        event_id = self.tree.item(item)['tags'][0]
        
        if isinstance(event_id, str) and event_id.startswith('sample_'):
            messagebox.showinfo("示例数据", "这是示例数据，无法查看详细文献")
            return
        
        # 获取事件和文献内容
        event, literature_content = db_manager.get_event_with_literature(event_id)
        
        if not event:
            messagebox.showwarning("警告", "未找到该事件的详细信息")
            return
        
        # 显示文献详情窗口
        self.show_literature_detail(event, literature_content)
    
    def show_literature_detail(self, event, literature_content):
        """显示文献详情窗口"""
        detail_window = tk.Toplevel(self.window)
        detail_window.title(f"📖 文献详情 - {event.title}")
        detail_window.geometry("800x600")
        detail_window.transient(self.window)
        detail_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(detail_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text=event.title,
            font=("微软雅黑", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # 基本信息
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = f"日期: {event.date} | 热度: {event.heat_score}% | 分类: {', '.join(event.categories) if event.categories else '无'}"
        ttk.Label(info_frame, text=info_text, font=("微软雅黑", 10)).pack(anchor="w")
        
        # 文献内容区域
        ttk.Label(main_frame, text="文献内容:", font=("微软雅黑", 12, "bold")).pack(anchor="w", pady=(10, 5))
        
        # 滚动文本框
        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("微软雅黑", 10)
        )
        text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 填充内容
        if literature_content:
            text_area.insert(tk.END, literature_content)
        else:
            text_area.insert(tk.END, "该事件暂无文献内容。\n\n描述信息:\n" + (event.description or "无描述"))
        
        text_area.config(state=tk.DISABLED)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="关闭",
            command=detail_window.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def view_literature(self):
        """查看文献"""
        self.on_item_double_click(None)
    
    def add_event(self):
        """添加新事件"""
        print(f"DEBUG: 点击添加事件，db_connected={self.db_connected}")
        if not self.db_connected:
            messagebox.showinfo("提示", "数据库不可用，无法添加事件")
            return
        
        # 创建添加事件对话框
        self.show_event_form_dialog(mode="add")

    def show_event_form_dialog(self, mode="add", event=None):
        """显示事件表单对话框"""
        dialog = tk.Toplevel(self.window)
        dialog.title("➕ 添加事件" if mode == "add" else "✏️ 编辑事件")
        dialog.geometry("600x700")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (
            self.window.winfo_rootx() + 50,
            self.window.winfo_rooty() + 50
        ))
        
        # 创建表单框架
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_text = "➕ 添加新事件" if mode == "add" else f"✏️ 编辑事件: {event.title if event else ''}"
        title_label = ttk.Label(
            form_frame,
            text=title_text,
            font=("微软雅黑", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 创建滚动区域
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 表单字段
        fields = self.create_form_fields(scrollable_frame, event, mode)
        
        # 按钮区域
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save_event():
            form_data = self.get_form_data(fields)
            if form_data and self.validate_form_data(form_data):
                if mode == "add":
                    self.save_new_event(form_data, dialog)
                else:
                    self.update_existing_event(event.id, form_data, dialog)
        
        ttk.Button(
            button_frame,
            text="💾 保存" if mode == "add" else "💾 更新",
            command=save_event
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy
        ).pack(side=tk.RIGHT)
        
        # 布局
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_form_fields(self, parent, event=None, mode="add"):
        """创建表单字段"""
        fields = {}
        
        # 事件标题
        ttk.Label(parent, text="事件标题 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        fields['title'] = ttk.Entry(parent, font=("微软雅黑", 10), width=60)
        fields['title'].pack(fill=tk.X, pady=(0, 15))
        if event and mode == "edit":
            fields['title'].insert(0, event.title)
        
        # 日期
        ttk.Label(parent, text="发生日期 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        from datetime import datetime
        now = datetime.now()
        
        ttk.Label(date_frame, text="年:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        fields['year'] = ttk.Spinbox(date_frame, from_=2000, to=2030, width=8)
        fields['year'].pack(side=tk.LEFT, padx=(5, 15))
        fields['year'].set(now.year if mode == "add" else event.date.year)
        
        ttk.Label(date_frame, text="月:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        fields['month'] = ttk.Spinbox(date_frame, from_=1, to=12, width=6)
        fields['month'].pack(side=tk.LEFT, padx=(5, 15))
        fields['month'].set(now.month if mode == "add" else event.date.month)
        
        ttk.Label(date_frame, text="日:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        fields['day'] = ttk.Spinbox(date_frame, from_=1, to=31, width=6)
        fields['day'].pack(side=tk.LEFT, padx=(5, 0))
        fields['day'].set(now.day if mode == "add" else event.date.day)
        
        # 事件类型
        ttk.Label(parent, text="事件类型 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        fields['type'] = tk.StringVar(value="meme" if mode == "add" else event.event_type)
        types = [
            ("热梗", "meme"),
            ("社会事件", "social_event"),
            ("科技趋势", "tech_trend"),
            ("政策法规", "policy"),
            ("娱乐文化", "entertainment")
        ]
        
        for text, value in types:
            ttk.Radiobutton(
                type_frame, 
                text=text, 
                variable=fields['type'], 
                value=value
            ).pack(side=tk.LEFT, padx=(0, 15))
        
        # 分类标签
        ttk.Label(parent, text="分类标签 (用逗号分隔)", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        fields['categories'] = ttk.Entry(parent, font=("微软雅黑", 10), width=60)
        fields['categories'].pack(fill=tk.X, pady=(0, 15))
        if event and mode == "edit" and event.categories:
            categories_text = ", ".join(event.categories)
            fields['categories'].insert(0, categories_text)
        
        # 热度评分
        ttk.Label(parent, text="热度评分 (0-100)", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        heat_frame = ttk.Frame(parent)
        heat_frame.pack(fill=tk.X, pady=(0, 15))
        
        fields['heat'] = tk.IntVar(value=50 if mode == "add" else event.heat_score)
        heat_scale = ttk.Scale(heat_frame, from_=0, to=100, variable=fields['heat'], orient=tk.HORIZONTAL)
        heat_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        fields['heat_label'] = ttk.Label(heat_frame, text=f"{fields['heat'].get()}%", font=("微软雅黑", 10), width=5)
        fields['heat_label'].pack(side=tk.RIGHT, padx=(10, 0))
        
        def update_heat_label(*args):
            fields['heat_label'].config(text=f"{fields['heat'].get()}%")
        
        fields['heat'].trace('w', update_heat_label)
        
        # 描述
        ttk.Label(parent, text="事件描述", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        fields['description'] = tk.Text(parent, font=("微软雅黑", 10), width=60, height=4)
        fields['description'].pack(fill=tk.X, pady=(0, 15))
        if event and mode == "edit" and event.description:
            fields['description'].insert("1.0", event.description)
        
        return fields

    def get_form_data(self, fields):
        """从表单字段获取数据"""
        from datetime import date
        
        try:
            # 基本验证
            title = fields['title'].get().strip()
            if not title:
                messagebox.showwarning("错误", "请输入事件标题")
                return None
            
            # 日期
            year = int(fields['year'].get())
            month = int(fields['month'].get())
            day = int(fields['day'].get())
            event_date = date(year, month, day)
            
            # 分类
            categories_text = fields['categories'].get().strip()
            categories = [cat.strip() for cat in categories_text.split(",") if cat.strip()] if categories_text else []
            
            # 描述
            description = fields['description'].get("1.0", tk.END).strip()
            
            return {
                'title': title,
                'date': event_date,
                'event_type': fields['type'].get(),
                'categories': categories,
                'heat_score': fields['heat'].get(),
                'description': description if description else None
            }
            
        except ValueError as e:
            messagebox.showerror("错误", "请输入有效的日期")
            return None

    def validate_form_data(self, form_data):
        """验证表单数据"""
        from datetime import date
        
        # 检查日期是否合理
        if form_data['date'] > date.today():
            messagebox.showwarning("错误", "事件日期不能晚于今天")
            return False
        
        # 检查热度评分
        if not 0 <= form_data['heat_score'] <= 100:
            messagebox.showwarning("错误", "热度评分必须在 0-100 之间")
            return False
        
        return True

    def save_new_event(self, form_data, dialog):
        """保存新事件"""
        try:
            # 修复：只接收一个返回值
            success = db_manager.add_event(form_data)
            if success:
                messagebox.showinfo("成功", "事件添加成功！")
                dialog.destroy()
                self.refresh_data()
                self.status_label.config(text="新事件添加成功")
            else:
                messagebox.showerror("错误", "添加事件失败，请检查数据库连接")
        except Exception as e:
            messagebox.showerror("错误", f"添加事件时发生错误: {e}")

    def update_existing_event(self, event_id, form_data, dialog):
        """更新现有事件"""
        try:
            # 修复：只接收一个返回值
            success = db_manager.update_event(event_id, form_data)
            if success:
                messagebox.showinfo("成功", "事件修改成功！")
                dialog.destroy()
                self.refresh_data()
                self.status_label.config(text="事件修改成功")
            else:
                messagebox.showerror("错误", "修改事件失败，请检查数据库连接")
        except Exception as e:
            messagebox.showerror("错误", f"修改事件时发生错误: {e}")

    def edit_event(self):
        """编辑事件"""
        print(f"DEBUG: 点击编辑事件，db_connected={self.db_connected}, selected_event={self.selected_event}")
        if not self.db_connected:
            messagebox.showinfo("提示", "数据库不可用，无法编辑事件")
            return
            
        if not self.selected_event:
            messagebox.showwarning("警告", "请先选择一个事件")
            return
        
        # 显示编辑事件对话框
        self.show_event_form_dialog(mode="edit", event=self.selected_event)

    def delete_event(self):
        """删除事件 - 修复反馈误导问题"""
        print(f"DEBUG: 点击删除事件，db_connected={self.db_connected}, selected_event={self.selected_event}")
        if not self.db_connected:
            messagebox.showinfo("提示", "数据库不可用，无法删除事件")
            return
            
        if not self.selected_event:
            messagebox.showwarning("警告", "请先选择一个事件")
            return

        # 确认删除
        response = messagebox.askyesno(
            "确认删除",
            f"您确定要删除以下事件吗？\n\n"
            f"📅 事件: {self.selected_event.title}\n"
            f"📅 日期: {self.selected_event.date}\n"
            f"🔖 类型: {self.get_event_type_display(self.selected_event.event_type)}\n\n"
            f"⚠️ 此操作不可撤销！",
            icon="warning"
        )

        if not response:
            return

        try:
            result = db_manager.delete_event(self.selected_event.id)
            # 兼容不同返回类型
            if isinstance(result, tuple):
                success, message = result
            else:
                success, message = (bool(result), "操作完成")

            if success:
                messagebox.showinfo("✅ 删除成功", f"事件已成功删除！\n\n{message}")
                self.refresh_data()
                self.status_label.config(text="事件删除成功")
                self.selected_event = None
            else:
                messagebox.showerror("❌ 删除失败", f"删除失败：{message}")
        except Exception as e:
            messagebox.showerror("系统错误", f"删除事件时发生异常:\n{e}")

    def import_data(self):
        """导入数据"""
        messagebox.showinfo("导入数据", "数据导入功能开发中...")
    
    def export_data(self):
        """导出数据"""
        messagebox.showinfo("导出数据", "数据导出功能开发中...")
    
    def refresh_data(self):
        """刷新数据"""
        self.load_events()
        self.status_label.config(text="数据已刷新")
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if DATABASE_AVAILABLE:
            db_manager.disconnect()

# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    app = DataManager(root)
    root.mainloop()