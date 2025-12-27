#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube分析工具 - 批量关键词分析示例
"""

from youtube_analyzer import YouTubeAnalyzer
import os

def batch_analyze_keywords():
    """批量分析多个关键词"""
    
    # API密钥
    api_key = os.getenv('YOUTUBE_API_KEY') or "你的API密钥"
    
    # 初始化分析器
    analyzer = YouTubeAnalyzer(api_key)
    
    # 关键词列表（根据你的领域调整）
    keywords = [
        # AI和科技类
        "AI tutorial",
        "ChatGPT tips",
        "productivity tools",
        
        # 生活技巧类
        "life hacks",
        "cooking tips",
        "fitness workout",
        
        # 赚钱类
        "make money online",
        "passive income",
        "side hustle",
        
        # 技能学习类
        "Python tutorial",
        "video editing",
        "digital marketing"
    ]
    
    print(f"\n{'='*60}")
    print(f"🚀 批量关键词分析工具")
    print(f"📝 共 {len(keywords)} 个关键词待分析")
    print(f"{'='*60}\n")
    
    all_results = {}
    
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] 正在分析: {keyword}")
        print("-" * 60)
        
        try:
            # 分析该关键词
            results = analyzer.analyze(
                input_type='keyword',
                input_value=keyword,
                max_results=30,  # 每个关键词分析30个视频
                min_views=500000,  # 降低到50万，找更多候选
                min_engagement=2.5,
                export=True
            )
            
            all_results[keyword] = results
            
            # 显示该关键词的Top 3
            if results:
                print(f"\n✅ {keyword} - Top 3:")
                for j, video in enumerate(results[:3], 1):
                    print(f"  {j}. {video['title'][:50]}...")
                    print(f"     热度: {video['heat_score']:.0f} | 播放: {video['view_count']:,}\n")
            else:
                print(f"⚠️ {keyword} - 未找到符合条件的视频\n")
                
        except Exception as e:
            print(f"❌ 分析失败: {e}\n")
            continue
    
    # 汇总报告
    print(f"\n{'='*60}")
    print(f"📊 分析汇总报告")
    print(f"{'='*60}\n")
    
    for keyword, results in all_results.items():
        print(f"• {keyword}: {len(results)} 个优质视频")
    
    total_videos = sum(len(v) for v in all_results.values())
    print(f"\n✅ 总计发现 {total_videos} 个可搬运的优质视频!")
    print(f"💾 所有数据已保存到 output/ 目录\n")


if __name__ == "__main__":
    batch_analyze_keywords()
