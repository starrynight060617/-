#!/usr/bin/env python3
"""
简中互联网抽象梗日历 - 主程序入口
版本 2.1.0 - 优化启动和错误处理
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def setup_environment():
    """设置运行环境"""
    # 添加项目根目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # 检查运行环境
    try:
        from scripts.startup_check import run_system_check
        print("🔍 进行系统检查...")
        if not run_system_check():
            print("⚠️ 系统检查未通过，可能影响部分功能")
        else:
            print("✅ 系统检查通过")
    except ImportError as e:
        print(f"⚠️ 启动检查不可用: {e}")

def check_dependencies():
    """检查必要依赖"""
    try:
        import sqlalchemy
        import tkinter
        return True
    except ImportError as e:
        print(f"❌ 缺少必要依赖: {e}")
        return False

def create_main_interface():
    """创建主界面"""
    try:
        # 尝试导入新版本的主界面
        from ui.desktop.ttk_app.main_interface import MemeCalendarApp
        app = MemeCalendarApp()
        return app
    except ImportError as e:
        print(f"❌ 导入主界面失败: {e}")
        # 尝试备用导入方式
        try:
            # 如果新的类名不可用，尝试旧的类名
            from ui.desktop.ttk_app.main_interface import MainInterface
            root = tk.Tk()
            app = MainInterface(root)
            return app
        except ImportError:
            return None

def show_welcome_message():
    """显示欢迎信息"""
    print("=" * 60)
    print("🎉 简中互联网抽象梗日历 v2.1.0")
    print("📅 基于事件热度的智能日历系统")
    print("📊 新增功能：文献管理系统、优化搜索界面")
    print("=" * 60)

def show_error_dialog(error_msg):
    """显示错误对话框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showerror(
        "启动失败 - 抽象梗日历",
        f"程序启动遇到问题：\n\n{error_msg}\n\n"
        "请检查：\n"
        "• Python版本是否为3.8+\n"
        "• 依赖包是否安装完整\n"
        "• 项目文件是否完整\n"
        "• 控制台查看详细错误信息"
    )
    root.destroy()

def main():
    """主函数"""
    try:
        # 显示欢迎信息
        show_welcome_message()
        
        # 设置环境
        setup_environment()
        
        # 检查依赖
        if not check_dependencies():
            show_error_dialog("缺少必要的Python依赖包")
            return
        
        # 创建主界面
        print("🎨 启动主界面...")
        app = create_main_interface()
        
        if app is None:
            show_error_dialog("无法加载主界面，请检查项目结构")
            return
        
        # 启动应用
        if hasattr(app, 'run'):
            app.run()
        else:
            # 如果应用没有run方法，启动Tkinter主循环
            if hasattr(app, 'root'):
                app.root.mainloop()
            else:
                # 最后尝试方式
                tk.mainloop()
                
    except KeyboardInterrupt:
        print("\n👋 用户中断程序")
    except Exception as e:
        error_msg = f"启动过程中发生未预期错误: {e}"
        print(f"❌ {error_msg}")
        show_error_dialog(error_msg)
    finally:
        print("🔚 程序退出")

if __name__ == "__main__":
    main()