#!/usr/bin/env python3
"""
简中互联网抽象梗日历 - 主程序入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.desktop.ttk_app.main_interface import MemeCalendarApp

def main():
    """主函数"""
    print("🚀 启动抽象梗日历系统...")
    print("📁 项目结构加载完成")
    print("🎨 启动主界面...")
    
    app = MemeCalendarApp()
    app.run()

if __name__ == "__main__":
    main()
