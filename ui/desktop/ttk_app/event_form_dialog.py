import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
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

class EventFormDialog:
    """事件表单对话框 - 用于添加和编辑事件"""
    
    def __init__(self, parent, event=None, mode="add"):
        """
        初始化事件表单对话框
        
        Args:
            parent: 父窗口
            event: 事件对象 (编辑模式时使用)
            mode: 模式 - "add" 或 "edit"
        """
        self.parent = parent
        self.event = event
        self.mode = mode
        self.result = None
        
        # 创建窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("➕ 添加事件" if mode == "add" else "✏️ 编辑事件")
        self.dialog.geometry("600x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        if mode == "edit" and event:
            self.load_event_data()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_text = "➕ 添加新事件" if self.mode == "add" else f"✏️ 编辑事件: {self.event.title}"
        title_label = ttk.Label(
            main_frame,
            text=title_text,
            font=("微软雅黑", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 创建滚动框架
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 表单内容
        self.create_form_fields(self.scrollable_frame)
        
        # 按钮区域
        self.create_buttons(main_frame)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_form_fields(self, parent):
        """创建表单字段"""
        # 事件标题
        ttk.Label(parent, text="事件标题 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.title_entry = ttk.Entry(parent, font=("微软雅黑", 10), width=60)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 日期
        ttk.Label(parent, text="发生日期 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(date_frame, text="年:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_spinbox = ttk.Spinbox(date_frame, from_=2000, to=2030, textvariable=self.year_var, width=8)
        year_spinbox.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(date_frame, text="月:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, textvariable=self.month_var, width=6)
        month_spinbox.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(date_frame, text="日:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        self.day_var = tk.StringVar(value=str(datetime.now().day))
        day_spinbox = ttk.Spinbox(date_frame, from_=1, to=31, textvariable=self.day_var, width=6)
        day_spinbox.pack(side=tk.LEFT, padx=(5, 0))
        
        # 事件类型
        ttk.Label(parent, text="事件类型 *", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.type_var = tk.StringVar(value="meme")
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        types = [
            ("热梗", "meme"),
            ("社会事件", "social_event"),
            ("科技趋势", "tech_trend"),
            ("政策法规", "policy"),
            ("娱乐文化", "entertainment"),
            ("其他", "other")
        ]
        
        for text, value in types:
            ttk.Radiobutton(
                type_frame, 
                text=text, 
                variable=self.type_var, 
                value=value
            ).pack(side=tk.LEFT, padx=(0, 15))
        
        # 分类标签
        ttk.Label(parent, text="分类标签 (用逗号分隔)", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.categories_entry = ttk.Entry(parent, font=("微软雅黑", 10), width=60)
        self.categories_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 热度评分
        ttk.Label(parent, text="热度评分 (0-100)", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        heat_frame = ttk.Frame(parent)
        heat_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.heat_var = tk.IntVar(value=50)
        heat_scale = ttk.Scale(heat_frame, from_=0, to=100, variable=self.heat_var, orient=tk.HORIZONTAL)
        heat_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.heat_label = ttk.Label(heat_frame, text="50%", font=("微软雅黑", 10), width=5)
        self.heat_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        heat_scale.configure(command=self.update_heat_label)
        
        # 描述
        ttk.Label(parent, text="事件描述", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.desc_text = tk.Text(parent, font=("微软雅黑", 10), width=60, height=6)
        self.desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # 文献内容
        ttk.Label(parent, text="详细文献内容", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.literature_text = tk.Text(parent, font=("微软雅黑", 10), width=60, height=10)
        self.literature_text.pack(fill=tk.X, pady=(0, 15))
        
        # 文献文件路径
        ttk.Label(parent, text="文献文件路径 (可选)", font=("微软雅黑", 11, "bold")).pack(anchor="w", pady=(10, 5))
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, font=("微软雅黑", 10))
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            file_frame, 
            text="浏览...", 
            command=self.browse_file,
            width=8
        ).pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_buttons(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        if self.mode == "add":
            ttk.Button(
                button_frame,
                text="➕ 添加事件",
                command=self.save_event,
                style="Accent.TButton"
            ).pack(side=tk.RIGHT, padx=(10, 0))
        else:
            ttk.Button(
                button_frame,
                text="💾 保存修改",
                command=self.save_event,
                style="Accent.TButton"
            ).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="取消",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT)
    
    def update_heat_label(self, value):
        """更新热度标签"""
        self.heat_label.config(text=f"{int(float(value))}%")
    
    def browse_file(self):
        """浏览文件"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="选择文献文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("Markdown文件", "*.md"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def load_event_data(self):
        """加载事件数据到表单"""
        if not self.event:
            return
            
        try:
            # 基本字段
            self.title_entry.insert(0, self.event.title)
            
            # 日期
            if self.event.date:
                self.year_var.set(str(self.event.date.year))
                self.month_var.set(str(self.event.date.month))
                self.day_var.set(str(self.event.date.day))
            
            # 类型
            self.type_var.set(self.event.event_type)
            
            # 分类
            if self.event.categories:
                categories_text = ", ".join(self.event.categories)
                self.categories_entry.insert(0, categories_text)
            
            # 热度
            if self.event.heat_score:
                self.heat_var.set(self.event.heat_score)
                self.heat_label.config(text=f"{self.event.heat_score}%")
            
            # 描述
            if self.event.description:
                self.desc_text.insert("1.0", self.event.description)
            
            # 文献内容
            if hasattr(self.event, 'literature_content') and self.event.literature_content:
                self.literature_text.insert("1.0", self.event.literature_content)
            
            # 文件路径
            if hasattr(self.event, 'literature_file_path') and self.event.literature_file_path:
                self.file_path_var.set(self.event.literature_file_path)
                
        except Exception as e:
            print(f"加载事件数据失败: {e}")
            messagebox.showerror("错误", f"加载事件数据失败: {e}")
    
    def validate_form(self):
        """验证表单数据"""
        # 检查必填字段
        if not self.title_entry.get().strip():
            messagebox.showwarning("验证错误", "请输入事件标题")
            self.title_entry.focus()
            return False
        
        # 验证日期
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            day = int(self.day_var.get())
            event_date = date(year, month, day)
            
            # 检查日期是否合理
            if event_date > date.today():
                messagebox.showwarning("验证错误", "事件日期不能晚于今天")
                return False
                
        except ValueError as e:
            messagebox.showwarning("验证错误", "请输入有效的日期")
            return False
        
        # 验证热度
        heat_score = self.heat_var.get()
        if not 0 <= heat_score <= 100:
            messagebox.showwarning("验证错误", "热度评分必须在 0-100 之间")
            return False
        
        return True
    
    def get_form_data(self):
        """获取表单数据"""
        # 日期
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        day = int(self.day_var.get())
        event_date = date(year, month, day)
        
        # 分类
        categories_text = self.categories_entry.get().strip()
        categories = [cat.strip() for cat in categories_text.split(",") if cat.strip()] if categories_text else []
        
        # 构建数据字典
        data = {
            'title': self.title_entry.get().strip(),
            'date': event_date,
            'event_type': self.type_var.get(),
            'categories': categories,
            'heat_score': self.heat_var.get(),
            'description': self.desc_text.get("1.0", tk.END).strip(),
            'literature_content': self.literature_text.get("1.0", tk.END).strip(),
            'literature_file_path': self.file_path_var.get().strip() or None
        }
        
        return data
    
    def save_event(self):
        """保存事件"""
        if not self.validate_form():
            return
        
        try:
            form_data = self.get_form_data()
            
            if self.mode == "add":
                # 添加新事件
                success, result = db_manager.add_event(**form_data)
                if success:
                    messagebox.showinfo("成功", "事件添加成功！")
                    self.result = result
                    self.dialog.destroy()
                else:
                    messagebox.showerror("错误", f"添加事件失败: {result}")
            
            else:
                # 编辑现有事件
                success, result = db_manager.update_event(self.event.id, **form_data)
                if success:
                    messagebox.showinfo("成功", "事件修改成功！")
                    self.result = result
                    self.dialog.destroy()
                else:
                    messagebox.showerror("错误", f"修改事件失败: {result}")
                    
        except Exception as e:
            messagebox.showerror("错误", f"保存事件时发生错误: {e}")
    
    def wait_for_result(self):
        """等待对话框结果"""
        self.parent.wait_window(self.dialog)
        return self.result