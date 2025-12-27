#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试YouTube分析工具"""

import os
import sys
import json
from youtube_analyzer import YouTubeAnalyzer

# 读取API密钥
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    api_key = config.get('youtube_api_key')

print('=== 测试YouTube欧美热门视频分析工具 ===\n')

# 创建分析器
analyzer = YouTubeAnalyzer(api_key)

# 先获取视频看看数据情况
print('📺 搜索: life hacks (生活技巧)')
video_ids = analyzer.search_videos('life hacks', 20)
videos = analyzer.get_video_details(video_ids)

print('\n📋 获取到的视频数据分析：')
print(f'总视频数: {len(videos)}\n')

# 统计数据
if videos:
    print('前5个视频详情：')
    for i, v in enumerate(videos[:5], 1):
        print(f'\n{i}. {v["title"][:60]}')
        print(f'   📈 播放: {v["view_count"]:,}')
        print(f'   👍 点赞: {v["like_count"]:,}')
        print(f'   💬 评论: {v["comment_count"]:,}')
        print(f'   📊 互动率: {v["engagement_rate"]}%')
        print(f'   ⏱️ 时长: {v["duration"]} ({v["duration_seconds"]}秒)')
        print(f'   📅 发布: {v["published_at"]} ({v["days_since_published"]}天前)')
        print(f'   🔥 热度: {v["heat_score"]:.0f}分')
    
    # 统计分析
    print('\n\n📊 数据统计分析：')
    views = [v['view_count'] for v in videos]
    durations = [v['duration_seconds'] for v in videos]
    engagement_rates = [v['engagement_rate'] for v in videos]
    days = [v['days_since_published'] for v in videos]
    
    print(f'播放量范围: {min(views):,} - {max(views):,}')
    print(f'时长范围: {min(durations)}秒 - {max(durations)}秒 ({min(durations)//60}-{max(durations)//60}分钟)')
    print(f'互动率范围: {min(engagement_rates):.2f}% - {max(engagement_rates):.2f}%')
    print(f'发布天数范围: {min(days)} - {max(days)}天')
    
    # 统计符合条件的数量
    count_10w = len([v for v in videos if v['view_count'] >= 100000])
    count_50w = len([v for v in videos if v['view_count'] >= 500000])
    count_100w = len([v for v in videos if v['view_count'] >= 1000000])
    count_duration = len([v for v in videos if 60 <= v['duration_seconds'] <= 600])
    count_engagement = len([v for v in videos if v['engagement_rate'] >= 2.5])
    
    print(f'\n符合各条件的视频数：')
    print(f'  播放量≥10万: {count_10w}/{len(videos)}')
    print(f'  播放量≥50万: {count_50w}/{len(videos)}')
    print(f'  播放量≥100万: {count_100w}/{len(videos)}')
    print(f'  时长1-10分钟: {count_duration}/{len(videos)}')
    print(f'  互动率≥2.5%: {count_engagement}/{len(videos)}')
    
    # 尝试不同的筛选条件
    print('\n\n🔍 测试筛选（降低要求）：')
    print('条件: 播放≥5万, 互动≥2%, 时长1-15分钟')
    
    filtered = analyzer.filter_videos(
        videos,
        min_views=50000,
        min_engagement=2.0,
        max_days=14,
        min_duration=60,
        max_duration=900  # 15分钟
    )
    
    if filtered:
        print(f'\n✅ 找到 {len(filtered)} 个视频！\n')
        print('Top 5:')
        for i, v in enumerate(filtered[:5], 1):
            print(f'\n{i}. [{v["heat_score"]:.0f}分] {v["title"][:60]}')
            print(f'   📈 {v["view_count"]:,}播放 | 👍 {v["like_count"]:,} | 💬 {v["comment_count"]:,} | ⏱️ {v["duration"]}')
            print(f'   🔗 {v["url"]}')
        
        # 导出Excel
        print('\n\n💾 导出Excel...')
        analyzer.export_to_excel(filtered)
    else:
        print('❌ 没有找到符合条件的视频')

print('\n\n✅ 测试完成！')
