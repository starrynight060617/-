import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from core.database.database_manager import db_manager
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"数据库导入错误: {e}")
    DATABASE_AVAILABLE = False

class DeleteEventDialog:
    """删除事件对话框"""
    
    def __init__(self, parent, event):
        """
        初始化删除事件对话框
        
        Args:
            parent: 父窗口
            event: 要删除的事件对象
        """
        self.parent = parent
        self.event = event
        self.result = False  # 是否成功删除
        
        # 验证事件对象
        if not event or not hasattr(event, 'id'):
            messagebox.showerror("错误", "无效的事件对象")
            return
    
    def show(self):
        """显示删除确认对话框"""
        if not self.event:
            messagebox.showwarning("警告", "没有选择要删除的事件")
            return False
        
        if not DATABASE_AVAILABLE:
            messagebox.showerror("错误", "数据库不可用，无法删除事件")
            return False
        
        # 获取事件类型显示文本
        event_type_display = self.get_event_type_display(self.event.event_type)
        
        # 获取分类显示文本
        categories_display = ""
        if hasattr(self.event, 'categories') and self.event.categories:
            if isinstance(self.event.categories, list):
                categories_display = ", ".join(self.event.categories)
            else:
                categories_display = str(self.event.categories)
        
        # 构建详细信息
        details = f"📅 事件: {self.event.title}\n"
        details += f"📅 日期: {self.event.date}\n"
        details += f"🔖 类型: {event_type_display}\n"
        
        if categories_display:
            details += f"🏷️  分类: {categories_display}\n"
        
        if hasattr(self.event, 'heat_score') and self.event.heat_score:
            details += f"🔥 热度: {self.event.heat_score}%\n"
        
        # 显示确认对话框
        response = messagebox.askyesno(
            "🗑️ 确认删除事件",
            f"您确定要删除以下事件吗？\n\n{details}\n"
            f"⚠️  此操作不可撤销！删除后数据将无法恢复。",
            icon="warning",
            default="no"  # 默认选择"否"以防误操作
        )
        
        if response:
            return self.execute_delete()
        
        return False
    
    def get_event_type_display(self, event_type):
        """获取事件类型显示文本"""
        type_map = {
            "meme": "🎭 热梗",
            "social_event": "👥 社会事件", 
            "tech_trend": "💻 科技趋势",
            "policy": "📜 政策法规",
            "entertainment": "🎬 娱乐文化",
            "other": "📌 其他"
        }
        return type_map.get(event_type, event_type)
    
    def execute_delete(self):
        """执行删除操作"""
        try:
            # 显示进度对话框
            progress_window = tk.Toplevel(self.parent)
            progress_window.title("删除中...")
            progress_window.geometry("300x100")
            progress_window.transient(self.parent)
            progress_window.grab_set()
            
            # 居中显示
            progress_window.geometry("+%d+%d" % (
                self.parent.winfo_rootx() + 100,
                self.parent.winfo_rooty() + 100
            ))
            
            # 进度标签
            progress_label = ttk.Label(
                progress_window,
                text="正在删除事件...",
                font=("微软雅黑", 10)
            )
            progress_label.pack(pady=20)
            
            progress_window.update()
            
            # 执行删除
            success, message = db_manager.delete_event(self.event.id)
            
            # 关闭进度窗口
            progress_window.destroy()
            
            if success:
                messagebox.showinfo(
                    "✅ 删除成功", 
                    f"事件删除成功！\n\n"
                    f"已删除事件: {self.event.title}\n"
                    f"{message}"
                )
                self.result = True
                return True
            else:
                messagebox.showerror(
                    "❌ 删除失败", 
                    f"删除事件失败:\n{message}\n\n"
                    f"请检查数据库连接或事件状态。"
                )
                return False
                
        except Exception as e:
            # 确保进度窗口关闭
            try:
                progress_window.destroy()
            except:
                pass
            
            error_msg = f"删除事件时发生错误:\n{str(e)}"
            print(f"删除事件错误: {e}")
            messagebox.showerror("❌ 系统错误", error_msg)
            return False
    
    def get_result(self):
        """获取删除结果"""
        return self.result

# 简化调用接口
def delete_event(parent, event):
    """
    删除事件 - 简化调用接口
    
    Args:
        parent: 父窗口
        event: 要删除的事件对象
        
    Returns:
        bool: 是否删除成功
    """
    dialog = DeleteEventDialog(parent, event)
    success = dialog.show()
    return success

# 测试代码
if __name__ == "__main__":
    # 测试删除对话框
    root = tk.Tk()
    root.withdraw()
    
    # 创建一个模拟事件对象进行测试
    class MockEvent:
        def __init__(self):
            self.id = 1
            self.title = "测试删除事件"
            self.date = "2024-01-01"
            self.event_type = "meme"
            self.categories = ["测试", "示例"]
            self.heat_score = 75
            self.description = "这是一个测试删除的事件"
    
    mock_event = MockEvent()
    
    # 测试删除功能
    success = delete_event(root, mock_event)
    print(f"删除结果: {success}")
    
    root.destroy()