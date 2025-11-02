import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from core.database.database_manager import db_manager
    from event_form_dialog import EventFormDialog
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"数据库导入错误: {e}")
    DATABASE_AVAILABLE = False

class EditEventDialog:
    """编辑事件对话框"""
    
    def __init__(self, parent, event):
        """
        初始化编辑事件对话框
        
        Args:
            parent: 父窗口
            event: 要编辑的事件对象
        """
        self.parent = parent
        self.event = event
        self.result = None
        
        # 验证事件对象
        if not event or not hasattr(event, 'id'):
            messagebox.showerror("错误", "无效的事件对象")
            return
    
    def show(self):
        """显示编辑事件对话框"""
        if not self.event:
            messagebox.showwarning("警告", "没有选择要编辑的事件")
            return False
        
        if not DATABASE_AVAILABLE:
            messagebox.showerror("错误", "数据库不可用，无法编辑事件")
            return False
        
        try:
            # 使用事件表单对话框进行编辑
            dialog = EventFormDialog(self.parent, event=self.event, mode="edit")
            self.result = dialog.wait_for_result()
            
            if self.result:
                print(f"✅ 事件编辑成功: {self.result.title}")
                return True
            else:
                print("❌ 事件编辑取消或失败")
                return False
                
        except Exception as e:
            print(f"编辑事件对话框错误: {e}")
            messagebox.showerror("错误", f"打开编辑对话框失败: {e}")
            return False
    
    def get_result(self):
        """获取编辑结果"""
        return self.result

# 简化调用接口
def edit_event(parent, event):
    """
    编辑事件 - 简化调用接口
    
    Args:
        parent: 父窗口
        event: 要编辑的事件对象
        
    Returns:
        bool: 是否编辑成功
    """
    dialog = EditEventDialog(parent, event)
    success = dialog.show()
    return success, dialog.get_result()

# 测试代码
if __name__ == "__main__":
    # 测试编辑对话框
    root = tk.Tk()
    root.withdraw()
    
    # 创建一个模拟事件对象进行测试
    class MockEvent:
        def __init__(self):
            self.id = 1
            self.title = "测试事件"
            self.date = "2024-01-01"
            self.event_type = "meme"
            self.categories = ["测试"]
            self.heat_score = 75
            self.description = "这是一个测试事件"
    
    mock_event = MockEvent()
    
    # 测试编辑功能
    success, result = edit_event(root, mock_event)
    print(f"编辑结果: success={success}, result={result}")
    
    root.destroy()