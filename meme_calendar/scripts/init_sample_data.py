# scripts/init_sample_data.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import date, datetime
from core.database.models import get_db_session, InternetEvent, PantheonFigure, HistoricalArtifact, FigureTimeline, HistoricalEvent

def generate_id(prefix="", sequence=1):
    """生成ID: 年月日 + 三位序列号"""
    today = datetime.now().strftime("%Y%m%d")
    return f"{prefix}{today}{sequence:03d}"

def init_sample_data():
    """初始化示例数据"""
    session = get_db_session()
    
    try:
        # 1. 创建万神殿人物 - 哈基米相关人物
        print("🏛️ 创建万神殿人物...")
        
        # 东海帝王 (赛马娘角色)
        figure1 = PantheonFigure(
            id=generate_id("figure_", 1),
            name="东海帝王",
            alias=["Tokai Teio", "帝宝"],
            birth_date=date(1992, 3, 20),
            birth_place="日本",
            description="《赛马娘》中的角色，哈基米梗的起源",
            bio="日本著名赛马东海帝王的拟人化角色，因在动画中哼唱蜂蜜水之歌而催生了哈基米梗",
            categories=["二次元", "虚拟偶像", "赛马娘"],
            tags=["蜂蜜水", "哈基米起源", "魔性哼唱"],
            influence_score=85,
            popularity_level="high",
            avatar_url="https://example.com/tokai_teio.jpg",
            media_urls=["https://example.com/hachimi_original.mp4"]
        )
        session.add(figure1)
        
        # 京桥刹那 (B站UP主)
        figure2 = PantheonFigure(
            id=generate_id("figure_", 2),
            name="京桥刹那",
            alias=["B站UP主", "鬼畜创作者"],
            description="将哈基米梗二次创作的B站UP主",
            bio="B站知名UP主，通过将东海帝王的哼唱与《CLANNAD》BGM混合，创作出鬼畜洗脑曲《哈基米哈基米我那类撸多》",
            categories=["UP主", "鬼畜创作者"],
            tags=["二次创作", "鬼畜", "B站"],
            influence_score=75,
            popularity_level="medium",
            avatar_url="https://example.com/kyobashi.jpg"
        )
        session.add(figure2)
        
        session.commit()
        
        # 2. 创建哈基米事件
        print("📅 创建互联网事件...")
        
        event1 = InternetEvent(
            id=generate_id("event_", 1),
            date=date(2021, 2, 15),
            title="哈基米起源：赛马娘蜂蜜水之歌",
            description="日本动画《赛马娘》中角色东海帝王哼唱蜂蜜水的魔性片段",
            event_type="meme",
            categories=["二次元", "动画", "音乐"],
            keywords=["哈基米", "赛马娘", "蜂蜜水", "东海帝王"],
            heat_level="high",
            heat_score=90,
            sources=["B站", "Niconico"],
            media_urls=["https://example.com/hachimi_original.mp4"],
            meme_image_url="https://example.com/hachimi_meme1.jpg",
            detailed_overview="""起源：日本动画中的蜂蜜水之歌
"哈基米"（日语空耳写作 hachimi）最初源自日本二次元企划《赛马娘》中角色东海帝王的一段魔性哼唱，原意是指蜂蜜水。在《赛马娘》第二季第12话中，角色哼唱了对蜂蜜饮料的喜爱之歌，其中"はちみ"（蜂蜜）因发音可爱而被中国观众音译成"哈基米"。

这一阶段，"哈基米"严格对应其字面含义——蜂蜜水。它带有日本动画的语境和鬼畜二创的魔性趣味，属于二次元圈层内部自娱性质的梗。""",
            figure_id=figure1.id
        )
        session.add(event1)
        
        event2 = InternetEvent(
            id=generate_id("event_", 2),
            date=date(2022, 5, 10),
            title="哈基米鬼畜神曲诞生",
            description="B站UP主京桥刹那将哈基米旋律二次创作成鬼畜洗脑曲",
            event_type="meme",
            categories=["鬼畜", "二次创作", "音乐"],
            keywords=["哈基米", "鬼畜", "二次创作", "B站"],
            heat_level="high",
            heat_score=95,
            sources=["B站"],
            media_urls=["https://example.com/hachimi_remix.mp4"],
            meme_image_url="https://example.com/hachimi_meme2.jpg",
            detailed_overview="""这一片段在日本网络上走红后，被B站UP主"京桥刹那"二次创作：他将东海帝王的哼唱旋律与动画《CLANNAD》的背景音乐《两个笨蛋》混合，制作出鬼畜洗脑曲《哈基米哈基米我那类撸多》。

由此，"哈基米"开始作为一个网络梗进入中国的亚文化视野，从二次元圈层逐渐向外扩散。""",
            figure_id=figure2.id
        )
        session.add(event2)
        
        event3 = InternetEvent(
            id=generate_id("event_", 3),
            date=date(2023, 3, 20),
            title="哈基米萌宠视频走红",
            description="哈基米神曲在抖音等平台成为萌宠视频标配BGM",
            event_type="meme",
            categories=["萌宠", "短视频", "音乐"],
            keywords=["哈基米", "猫咪", "萌宠", "抖音"],
            heat_level="very_high",
            heat_score=98,
            sources=["抖音", "B站"],
            media_urls=["https://example.com/hachimi_cats.mp4"],
            meme_image_url="https://example.com/hachimi_cat_meme.jpg",
            detailed_overview="""萌宠视频走红：等同"小猫咪"的语义转移
随着鬼畜神曲的出现，"哈基米"开始出圈传播，并在抖音等短视频平台上爆火。大量UP主和博主将这首节奏欢快、洗脑的歌曲用作萌宠（尤其是猫咪）视频的背景音乐：画面中小猫憨态可掬的卖萌动作与BGM中"哈基米哈基米~"的俏皮旋律踩点契合，形成了让人会心一笑的可爱效果。

通过此类宠物内容的二次创作，"哈基米"这个词逐渐脱离原本蜂蜜水的字面义，转而被网友直接用来指代可爱的猫咪，甚至泛指一切萌宠和卖萌行为。""",
            figure_id=figure1.id
        )
        session.add(event3)
        
        event4 = InternetEvent(
            id=generate_id("event_", 4),
            date=date(2023, 6, 15),
            title="哈基米现充误用与圈层冲突",
            description="非二次元用户误用哈基米引发原教旨粉丝不满",
            event_type="meme",
            categories=["网络文化", "圈层冲突", "语义演变"],
            keywords=["哈基米", "现充", "误用", "圈层冲突", "烂梗"],
            heat_level="high",
            heat_score=88,
            sources=["贴吧", "微博", "B站"],
            media_urls=["https://example.com/hachimi_conflict.mp4"],
            meme_image_url="https://example.com/hachimi_conflict_meme.jpg",
            detailed_overview="""误用与圈层冲突：现充误读引发定义权之争
由于"哈基米"在萌宠圈的流行，不少非原始圈层的网友（所谓"现充"，即非二次元宅文化的普通用户）误以为"哈基米"是日语中"小猫咪"的意思，并在各种语境中滥用。这种误读引发了原本梗参与者（《赛马娘》粉丝和鬼畜区用户）的强烈不满。

他们看到自己圈内的梗被大规模误用，认为这是"烂梗入侵"，担心亚文化空间被挤占，纷纷出面指正"哈基米"原本只是蜂蜜水。由此，围绕"哈基米"含义的话语权争夺战打响。""",
            figure_id=figure1.id
        )
        session.add(event4)
        
        # 3. 创建历史文物/物品
        print("🏺 创建历史文物...")
        
        artifact1 = HistoricalArtifact(
            id=generate_id("artifact_", 1),
            figure_id=figure1.id,
            name="蜂蜜水之歌原片",
            artifact_type="视频作品",
            content="《赛马娘》第二季第12话中东海帝王哼唱蜂蜜水的原始片段",
            occurrence_date=date(2021, 2, 15),
            date_accuracy="exact",
            source="《赛马娘》动画",
            is_verified=True,
            significance_level="high",
            impact_description="哈基米梗的文化起源，影响了后续整个网络迷因的发展",
            media_urls=["https://example.com/original_clip.mp4"]
        )
        session.add(artifact1)
        
        artifact2 = HistoricalArtifact(
            id=generate_id("artifact_", 2),
            figure_id=figure2.id,
            name="《哈基米哈基米我那类撸多》鬼畜作品",
            artifact_type="二次创作",
            content="京桥刹那创作的鬼畜洗脑曲，混合了东海帝王哼唱和CLANNAD BGM",
            occurrence_date=date(2022, 5, 10),
            date_accuracy="exact",
            source="B站",
            is_verified=True,
            significance_level="high",
            impact_description="让哈基米梗真正出圈的关键作品，推动了梗的广泛传播",
            media_urls=["https://example.com/remix_video.mp4"]
        )
        session.add(artifact2)
        
        # 4. 创建人物时间线
        print("📜 创建人物时间线...")
        
        timeline1 = FigureTimeline(
            id=generate_id("timeline_", 1),
            figure_id=figure1.id,
            year=1992,
            event_title="东海帝王出生",
            event_description="现实中的赛马东海帝王在日本出生",
            importance="major",
            event_type="birth",
            source="赛马历史记录"
        )
        session.add(timeline1)
        
        timeline2 = FigureTimeline(
            id=generate_id("timeline_", 2),
            figure_id=figure1.id,
            year=2021,
            event_title="赛马娘动画播出",
            event_description="《赛马娘》第二季播出，东海帝王角色登场并演唱蜂蜜水之歌",
            importance="major",
            event_type="career",
            source="动画播出记录"
        )
        session.add(timeline2)
        
        # 5. 创建历史事件（同年今日用）
        print("📚 创建历史事件...")
        
        historical1 = HistoricalEvent(
            id=generate_id("history_", 1),
            date=date(2021, 2, 15),
            title="哈基米文化现象诞生",
            description="《赛马娘》动画中东海帝王哼唱蜂蜜水，标志着哈基米梗的起源",
            event_type="cultural",
            categories=["互联网文化", "二次元"],
            importance_level="high",
            location="日本",
            source="动画播出记录",
            related_figure_ids=[figure1.id],
            related_event_ids=[event1.id],
            media_urls=["https://example.com/hachimi_origin.jpg"]
        )
        session.add(historical1)
        
        session.commit()
        print("✅ 示例数据初始化完成！")
        print(f"   🏛️ 创建了 {session.query(PantheonFigure).count()} 个人物")
        print(f"   📅 创建了 {session.query(InternetEvent).count()} 个互联网事件")
        print(f"   🏺 创建了 {session.query(HistoricalArtifact).count()} 个历史文物")
        print(f"   📜 创建了 {session.query(FigureTimeline).count()} 条时间线")
        print(f"   📚 创建了 {session.query(HistoricalEvent).count()} 个历史事件")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 数据初始化失败: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_sample_data()