#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 展示如何使用YouTube分析工具
"""

from youtube_analyzer import YouTubeAnalyzer
import os

# ============================================================
# 示例1: 简单的关键词搜索
# ============================================================
def example_1_simple_search():
    """最简单的使用方式 - 搜索关键词"""
    print("\n" + "="*60)
    print("示例1: 简单关键词搜索")
    print("="*60)
    
    # 初始化（从环境变量或config.json读取API密钥）
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 分析关键词 "AI tutorial"
    results = analyzer.analyze(
        input_type='keyword',
        input_value='AI tutorial',
        max_results=30
    )
    
    # 打印前5个结果
    print("\n前5个热门视频:")
    for i, video in enumerate(results[:5], 1):
        print(f"{i}. {video['title']}")
        print(f"   热度: {video['heat_score']:.0f} | 播放: {video['view_count']:,}")


# ============================================================
# 示例2: 分析YouTube频道
# ============================================================
def example_2_channel_analysis():
    """分析指定频道的所有视频"""
    print("\n" + "="*60)
    print("示例2: 频道分析")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 分析频道（替换为实际频道URL）
    results = analyzer.analyze(
        input_type='channel',
        input_value='https://www.youtube.com/@TEDEd',  # TED-Ed频道示例
        max_results=50
    )


# ============================================================
# 示例3: 自定义筛选条件
# ============================================================
def example_3_custom_filters():
    """使用自定义筛选条件"""
    print("\n" + "="*60)
    print("示例3: 自定义筛选")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 降低门槛，找更多候选视频
    results = analyzer.analyze(
        input_type='keyword',
        input_value='productivity hacks',
        max_results=50,
        min_views=500000,      # 50万播放量（更宽松）
        min_engagement=2.0,    # 2%互动率（更宽松）
        export=True
    )


# ============================================================
# 示例4: 批量分析多个关键词
# ============================================================
def example_4_batch_analysis():
    """批量分析多个关键词"""
    print("\n" + "="*60)
    print("示例4: 批量分析")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 定义关键词列表
    keywords = [
        'AI tutorial',
        'Python programming',
        'productivity tips',
        'make money online'
    ]
    
    all_results = {}
    
    for keyword in keywords:
        print(f"\n分析关键词: {keyword}")
        results = analyzer.analyze(
            input_type='keyword',
            input_value=keyword,
            max_results=20,
            export=True
        )
        all_results[keyword] = results
    
    # 汇总
    print("\n汇总结果:")
    for keyword, videos in all_results.items():
        print(f"• {keyword}: {len(videos)} 个优质视频")


# ============================================================
# 示例5: 编程式使用（不导出Excel）
# ============================================================
def example_5_programmatic_use():
    """编程式使用，处理返回的数据"""
    print("\n" + "="*60)
    print("示例5: 编程式使用")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 搜索视频（不自动导出）
    video_ids = analyzer.search_videos('cooking tutorial', max_results=20)
    
    # 获取详情
    videos = analyzer.get_video_details(video_ids)
    
    # 筛选
    filtered = analyzer.filter_videos(
        videos,
        min_views=1000000,
        min_engagement=3.0
    )
    
    # 自定义处理
    print("\n找到的优质视频:")
    for video in filtered[:10]:
        print(f"\n标题: {video['title']}")
        print(f"链接: {video['url']}")
        print(f"播放量: {video['view_count']:,}")
        print(f"热度指数: {video['heat_score']:.0f}")
        print(f"频道: {video['channel_title']}")
    
    # 手动导出
    if filtered:
        analyzer.export_to_excel(filtered, 'output/custom_analysis.xlsx')


# ============================================================
# 示例6: 找特定类型的视频
# ============================================================
def example_6_specific_content():
    """找特定类型的内容"""
    print("\n" + "="*60)
    print("示例6: 找特定类型视频")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 找短视频（适合抖音）
    print("\n找短视频（1-3分钟）...")
    video_ids = analyzer.search_videos('quick tips', max_results=50)
    videos = analyzer.get_video_details(video_ids)
    
    # 筛选1-3分钟的视频
    short_videos = [
        v for v in videos
        if '01:' in v['duration'] or '02:' in v['duration'] or '00:' in v['duration']
    ]
    
    print(f"找到 {len(short_videos)} 个短视频")
    
    # 按热度排序
    short_videos.sort(key=lambda x: x['heat_score'], reverse=True)
    
    for i, video in enumerate(short_videos[:5], 1):
        print(f"\n{i}. {video['title'][:50]}...")
        print(f"   时长: {video['duration']} | 热度: {video['heat_score']:.0f}")


# ============================================================
# 示例7: 竞品分析
# ============================================================
def example_7_competitor_analysis():
    """分析竞争对手的内容策略"""
    print("\n" + "="*60)
    print("示例7: 竞品分析")
    print("="*60)
    
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    analyzer = YouTubeAnalyzer(api_key)
    
    # 分析多个竞争对手频道
    competitors = [
        'https://www.youtube.com/@TEDEd',
        # 添加更多竞争对手频道
    ]
    
    for channel in competitors:
        print(f"\n分析频道: {channel}")
        results = analyzer.analyze(
            input_type='channel',
            input_value=channel,
            max_results=30,
            export=False  # 不导出，只看数据
        )
        
        if results:
            # 分析内容策略
            avg_heat = sum(v['heat_score'] for v in results) / len(results)
            avg_duration = sum(
                int(v['duration'].split(':')[0]) * 60 + int(v['duration'].split(':')[1])
                for v in results
            ) / len(results)
            
            print(f"平均热度: {avg_heat:.0f}")
            print(f"平均时长: {avg_duration/60:.1f} 分钟")
            print(f"最热视频: {results[0]['title'][:50]}...")


# ============================================================
# 主函数 - 运行示例
# ============================================================
def main():
    """运行所有示例"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        YouTube分析工具 - 使用示例集合                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\n选择要运行的示例:")
    print("1. 简单关键词搜索")
    print("2. 分析YouTube频道")
    print("3. 自定义筛选条件")
    print("4. 批量分析多个关键词")
    print("5. 编程式使用")
    print("6. 找特定类型视频")
    print("7. 竞品分析")
    print("0. 运行所有示例")
    
    choice = input("\n请选择 (0-7): ").strip()
    
    examples = {
        '1': example_1_simple_search,
        '2': example_2_channel_analysis,
        '3': example_3_custom_filters,
        '4': example_4_batch_analysis,
        '5': example_5_programmatic_use,
        '6': example_6_specific_content,
        '7': example_7_competitor_analysis,
    }
    
    if choice == '0':
        # 运行所有示例
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"示例运行失败: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"示例运行失败: {e}")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()
