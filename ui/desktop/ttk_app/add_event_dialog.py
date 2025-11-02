import tkinter as tk
from tkinter import ttk
from event_form_dialog import EventFormDialog

class AddEventDialog:
    """添加事件对话框"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
    
    def show(self):
        """显示添加事件对话框"""
        dialog = EventFormDialog(self.parent, mode="add")
        self.result = dialog.wait_for_result()
        return self.result

# 简化调用接口
def add_event(parent):
    """添加事件 - 简化调用接口"""
    dialog = AddEventDialog(parent)
    return dialog.show()