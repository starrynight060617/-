"""
初始化文献存储目录脚本
"""

import os
import sys

def init_literature_directory():
    """初始化文献存储目录"""
    
    # 添加项目根目录到Python路径
    project_root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(project_root)
    
    try:
        from config.settings import LITERATURE_BASE_DIR
        
        # 创建文献目录
        os.makedirs(LITERATURE_BASE_DIR, exist_ok=True)
        
        # 创建示例文献文件
        sample_literature = {
            "20250115-001.txt": """AI公务员上岗引热议 - 文献详情

事件概述：
2025年1月15日，首个AI公务员在某市政务服务中心正式上岗，引发社会广泛关注。

背景信息：
随着人工智能技术的快速发展，政府部门开始尝试将AI技术应用于公共服务领域。
该AI公务员基于大语言模型开发，能够处理常见的政务咨询、文件办理等业务。

社会反响：
- 支持者认为AI公务员能提高效率，减少人为错误
- 质疑者担心数据安全和隐私保护问题
- 专家建议建立完善的监管机制

技术特点：
- 自然语言处理能力
- 24小时不间断服务
- 多轮对话理解
- 情感识别功能

未来展望：
AI技术在政务领域的应用将进一步深化，但需要平衡技术创新与人文关怀。""",
            
            "20250214-001.txt": """元宇宙情人节爆火 - 文献详情

事件概述：
2025年情人节期间，元宇宙虚拟礼物经济单日交易额突破亿元大关。

现象描述：
- 数字玫瑰成为最受欢迎的虚拟礼物
- 虚拟约会场景预订火爆
- 跨地域情侣通过元宇宙相聚

经济数据：
- 单日交易额：1.2亿元
- 参与用户：超过500万人次
- 平均消费：24元/人

技术支撑：
- VR/AR设备普及
- 区块链确权技术
- 实时渲染引擎

社会影响：
- 改变了传统节日消费模式
- 创造了新的就业机会
- 引发了关于虚拟与现实关系的讨论

行业展望：
虚拟经济将成为数字经济的重要组成部分，但需要规范发展。"""
        }
        
        # 写入示例文献文件
        created_count = 0
        for filename, content in sample_literature.items():
            file_path = os.path.join(LITERATURE_BASE_DIR, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created_count += 1
                print(f"创建示例文献: {filename}")
        
        print(f"\n✅ 文献目录初始化完成!")
        print(f"📁 目录位置: {LITERATURE_BASE_DIR}")
        print(f"📄 创建文件: {created_count} 个")
        
        # 检查目录权限
        test_file = os.path.join(LITERATURE_BASE_DIR, "test_permission.txt")
        try:
            with open(test_file, 'w') as f:
                f.write("权限测试")
            os.remove(test_file)
            print("🔒 目录读写权限: 正常")
        except Exception as e:
            print(f"❌ 目录读写权限异常: {e}")
            
    except ImportError as e:
        print(f"❌ 导入配置失败: {e}")
        print("请确保配置文件 settings.py 存在且配置正确")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")

if __name__ == "__main__":
    init_literature_directory()