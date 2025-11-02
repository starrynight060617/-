"""
简单的桌面日历应用
"""

import tkinter as tk
from tkinter import ttk

class SimpleCalendar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("抽象梗日历")
        self.root.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_label = ttk.Label(self.root, text="简中互联网抽象梗日历", font=("Arial", 16))
        title_label.pack(pady=20)
        
        # 事件列表
        self.tree = ttk.Treeview(self.root, columns=("date", "title"), show="headings")
        self.tree.heading("date", text="日期")
        self.tree.heading("title", text="事件标题")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 添加事件显示功能
    def load_events(self):
        events = load_sample_data()
        for event in events:
            self.tree.insert("", "end", values=(event['date'], event['title']))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleCalendar()
    app.run()
