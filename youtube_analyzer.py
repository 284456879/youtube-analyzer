#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频热度分析工具
功能：自动分析YouTube视频数据，筛选高热度内容，导出Excel报表
"""

import os
import json
import re
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 确保控制台输出使用UTF-8，避免emoji打印报错
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="ignore")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="ignore")
except Exception:
    pass

class YouTubeAnalyzer:
    """YouTube视频分析器"""
    
    def __init__(self, api_key: str, cpm_low: float = 2.0, cpm_high: float = 4.0,
                 default_language: str = "en", default_region_code: str = "US"):
        """
        初始化分析器
        
        Args:
            api_key: YouTube Data API v3 密钥
            cpm_low: 预估每千次播放CPM下限（美元）
            cpm_high: 预估每千次播放CPM上限（美元）
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.videos_data = []
        self.cpm_low = cpm_low
        self.cpm_high = cpm_high
        self.hot_keywords = [
            'hack', 'hacks', 'diy', 'tips', 'trick', 'tricks', 'challenge', 'viral',
            'recipe', 'cook', 'cooking', 'air fryer', 'slime', 'asmr', 'shortcut',
            'easy', 'fast', 'quick', 'life', 'tiktok', 'shorts'
        ]
        self.trend_window_days = 14
        self.default_language = default_language
        self.default_region_code = default_region_code
        
    def search_videos(self, keyword: str, max_results: int = 50,
                      language: Optional[str] = None,
                      region: Optional[str] = None) -> List[str]:
        """
        根据关键词搜索视频（针对欧美地区热门内容）
        
        Args:
            keyword: 搜索关键词
            max_results: 返回结果数量（最多50）
            
        Returns:
            视频ID列表
        """
        try:
            # 搜索最近14天内的视频（更新鲜的内容）
            published_after = (datetime.now() - timedelta(days=14)).isoformat() + 'Z'
            
            params = {
                "part": "id",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "maxResults": max_results,
                "publishedAfter": published_after,
                "regionCode": (region or self.default_region_code),
                "videoDuration": "medium"
            }
            lang = language or self.default_language
            if lang:
                params["relevanceLanguage"] = lang
            request = self.youtube.search().list(**params)
            response = request.execute()
            
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]
            print(f"✅ 找到 {len(video_ids)} 个欧美地区相关视频")
            return video_ids
            
        except HttpError as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def get_channel_videos(self, channel_url: str, max_results: int = 50) -> List[str]:
        """
        获取频道的视频列表
        
        Args:
            channel_url: YouTube频道URL
            max_results: 返回结果数量
            
        Returns:
            视频ID列表
        """
        try:
            # 提取频道ID
            channel_id = self._extract_channel_id(channel_url)
            if not channel_id:
                print("❌ 无效的频道URL")
                return []
            
            # 获取频道的uploads播放列表
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            if not response.get('items'):
                print("❌ 找不到该频道")
                return []
            
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # 获取播放列表中的视频
            video_ids = []
            next_page_token = None
            
            while len(video_ids) < max_results:
                request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(video_ids)),
                    pageToken=next_page_token
                )
                response = request.execute()
                
                video_ids.extend([item['contentDetails']['videoId'] for item in response.get('items', [])])
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            print(f"✅ 从频道获取 {len(video_ids)} 个视频")
            return video_ids
            
        except HttpError as e:
            print(f"❌ 获取频道视频失败: {e}")
            return []
    
    def _extract_channel_id(self, channel_url: str) -> Optional[str]:
        """提取频道ID"""
        # 匹配 @username 格式
        if '@' in channel_url:
            username = channel_url.split('@')[-1].split('/')[0]
            try:
                request = self.youtube.channels().list(
                    part="id",
                    forHandle=username
                )
                response = request.execute()
                if response.get('items'):
                    return response['items'][0]['id']
            except:
                pass
        
        # 匹配 channel/ID 格式
        match = re.search(r'channel/([a-zA-Z0-9_-]+)', channel_url)
        if match:
            return match.group(1)
        
        # 直接是ID
        if re.match(r'^[a-zA-Z0-9_-]{24}$', channel_url):
            return channel_url
        
        return None
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        获取视频详细信息
        
        Args:
            video_ids: 视频ID列表
            
        Returns:
            视频详情列表
        """
        videos_details = []
        
        # YouTube API限制每次最多50个视频
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            
            try:
                request = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=','.join(batch_ids)
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    video_info = self._parse_video_data(item)
                    videos_details.append(video_info)
                    
            except HttpError as e:
                print(f"❌ 获取视频详情失败: {e}")
                continue
        
        print(f"✅ 成功获取 {len(videos_details)} 个视频的详细信息")
        return videos_details
    
    def _parse_video_data(self, item: Dict) -> Dict:
        """解析视频数据"""
        snippet = item['snippet']
        statistics = item['statistics']
        content_details = item['contentDetails']
        
        # 计算发布天数
        published_at = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_published = max(1, (datetime.now() - published_at).days)
        
        # 获取数据
        view_count = int(statistics.get('viewCount', 0))
        like_count = int(statistics.get('likeCount', 0))
        comment_count = int(statistics.get('commentCount', 0))
        
        # 计算互动率
        engagement_rate = 0
        if view_count > 0:
            engagement_rate = ((like_count + comment_count) / view_count) * 100
        
        # 计算热度指数
        heat_score = self._calculate_heat_score(
            view_count, like_count, comment_count, days_since_published
        )
        
        # 解析视频时长
        duration = self._parse_duration(content_details['duration'])
        duration_seconds = self._parse_duration_seconds(content_details['duration'])

        # 预估收益（美元）
        revenue_low, revenue_high, revenue_mid = self._estimate_revenue(view_count)
        hot_reasons = self._analyze_hot_reasons(
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count,
            engagement_rate=engagement_rate,
            days_since_published=days_since_published,
            duration_seconds=duration_seconds,
            title=snippet['title']
        )
        trend = self._analyze_trend(
            view_count=view_count,
            engagement_rate=engagement_rate,
            days_since_published=days_since_published,
            duration_seconds=duration_seconds
        )
        
        return {
            'video_id': item['id'],
            'title': snippet['title'],
            'channel_title': snippet['channelTitle'],
            'published_at': published_at.strftime('%Y-%m-%d'),
            'days_since_published': days_since_published,
            'duration': duration,
            'duration_seconds': duration_seconds,
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'engagement_rate': round(engagement_rate, 2),
            'heat_score': round(heat_score, 2),
            'revenue_low': revenue_low,
            'revenue_high': revenue_high,
            'revenue_mid': revenue_mid,
            'hot_reasons': hot_reasons,
            'hot_reasons_text': '; '.join(hot_reasons[:4]),
            'avg_daily_views': trend['avg_daily_views'],
            'trend_label': trend['label'],
            'trend_score': trend['score'],
            'trend_points': trend['points'],
            'url': f"https://www.youtube.com/watch?v={item['id']}",
            'thumbnail': snippet['thumbnails']['high']['url'],
            'description': snippet.get('description', '')[:200]  # 前200字符
        }
    
    def _calculate_heat_score(self, views: int, likes: int, comments: int, days: int) -> float:
        """
        计算热度指数（针对搬运优化：更注重互动率）
        
        公式：(播放量 × 0.3 + 点赞数 × 30 + 评论数 × 15) / 发布天数
        互动高的视频说明内容更有吸引力，适合搬运
        """
        score = (views * 0.3 + likes * 30 + comments * 15) / max(1, days)
        return score
    
    def _parse_duration(self, duration_str: str) -> str:
        """解析ISO 8601时长格式为可读格式"""
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return "00:00"
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def _parse_duration_seconds(self, duration_str: str) -> int:
        """解析ISO 8601时长格式为总秒数"""
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        return hours * 3600 + minutes * 60 + seconds

    def _estimate_revenue(self, views: int) -> tuple:
        """基于播放量和CPM范围预估收益（美元）"""
        if views <= 0:
            return 0.0, 0.0, 0.0

        low = round((views / 1000) * self.cpm_low, 2)
        high = round((views / 1000) * self.cpm_high, 2)
        mid = round((low + high) / 2, 2)
        return low, high, mid

    def _analyze_trend(self,
                       view_count: int,
                       engagement_rate: float,
                       days_since_published: int,
                       duration_seconds: int) -> dict:
        """简单趋势分析：日均播放、趋势评分、标签、曲线点"""
        days = max(1, min(days_since_published, 90))
        avg_daily = view_count / days

        score = avg_daily
        score += engagement_rate * 1500  # 互动加权
        if days_since_published <= 7:
            score *= 1.15  # 新视频轻微加成
        if duration_seconds <= 120:
            score *= 1.05  # 短快内容再加成

        # 标签
        if days_since_published <= 3 and avg_daily >= 50000:
            label = "爆发期"
        elif avg_daily >= 100000:
            label = "高速增长"
        elif avg_daily >= 30000:
            label = "稳定增长"
        elif avg_daily >= 10000:
            label = "平稳"
        else:
            label = "缓慢"

        points = self._build_trend_points(view_count, days_since_published)
        return {
            'avg_daily_views': round(avg_daily, 2),
            'score': round(score, 2),
            'label': label,
            'points': points
        }

    def _build_trend_points(self, view_count: int, days_since_published: int) -> list:
        """构造一个简单的趋势曲线（线性/近似），用于前端小型折线图"""
        days = max(1, days_since_published)
        window = max(3, min(self.trend_window_days, days))
        avg = view_count / days
        # 生成窗口内的累积曲线，假设前期较慢、后期加速（简单二次增长）
        pts = []
        for i in range(window):
            t = (i + 1) / window
            factor = 0.6 + 0.4 * (t ** 1.5)  # 末段稍加速
            pts.append(int(avg * days * factor / window))
        # 确保最后一点接近总播放
        pts[-1] = view_count
        return pts

    def _analyze_hot_reasons(self,
                             view_count: int,
                             like_count: int,
                             comment_count: int,
                             engagement_rate: float,
                             days_since_published: int,
                             duration_seconds: int,
                             title: str) -> list:
        """基于简单规则的爆红原因分析（无LLM，纯启发式）"""
        reasons = []

        # 互动和口碑
        like_rate = (like_count / view_count * 100) if view_count else 0
        comment_rate = (comment_count / view_count * 100) if view_count else 0
        if engagement_rate >= 4:
            reasons.append("high_engagement")
        elif engagement_rate >= 2.5:
            reasons.append("good_engagement")
        if like_rate >= 2.0:
            reasons.append("high_like_rate")
        if comment_rate >= 0.1:
            reasons.append("high_comment_rate")

        # 时长和完播潜力
        if 240 <= duration_seconds <= 600:
            reasons.append("optimal_duration")
        elif 60 <= duration_seconds < 240:
            reasons.append("short_duration")

        # 新鲜度
        if days_since_published <= 7:
            reasons.append("fresh_7d")
        elif days_since_published <= 14:
            reasons.append("fresh_14d")

        # 标题关键词
        tl = title.lower()
        if any(k in tl for k in self.hot_keywords):
            reasons.append("title_clickbait")

        # 基数与社交证明
        if view_count >= 500000:
            reasons.append("high_views")

        # 兜底
        if not reasons:
            reasons.append("general_good")

        return reasons
    
    def filter_videos(self, 
                     videos: List[Dict],
                     min_views: int = 50000,
                     min_engagement: float = 2.0,
                     max_days: int = 14,
                     min_duration: int = 60,
                     max_duration: int = 900) -> List[Dict]:
        """
        筛选适合搬运的欧美热门视频
        
        Args:
            videos: 视频列表
            min_views: 最低播放量（默认5万，证明有热度且容易搬运）
            min_engagement: 最低互动率(%)（默认2%）
            max_days: 最多发布天数（默认14天，保证内容新鲜）
            min_duration: 最短时长（秒，默认60秒）
            max_duration: 最长时长（秒，默认900秒=15分钟，适合短视频平台）
            
        Returns:
            筛选后的视频列表
        """
        filtered = [
            v for v in videos
            if v['view_count'] >= min_views
            and v['engagement_rate'] >= min_engagement
            and v['days_since_published'] <= max_days
            and min_duration <= v['duration_seconds'] <= max_duration
        ]
        
        # 按热度排序
        filtered.sort(key=lambda x: x['heat_score'], reverse=True)
        
        print(f"✅ 筛选出 {len(filtered)} 个适合搬运的视频")
        print(f"   (时长: {min_duration//60}-{max_duration//60}分钟, 播放量≥{min_views:,}, 互动率≥{min_engagement}%)")
        return filtered
    
    def export_to_excel(self, videos: List[Dict], filename: str = None):
        """
        导出到Excel
        
        Args:
            videos: 视频列表
            filename: 输出文件名
        """
        if not videos:
            print("⚠️ 没有数据可导出")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/youtube_analysis_{timestamp}.xlsx"
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else 'output', exist_ok=True)
        
        # 创建DataFrame
        df = pd.DataFrame(videos)
        
        # 重新排列列顺序
        column_order = [
            'heat_score', 'title', 'view_count', 'like_count', 'comment_count',
            'engagement_rate', 'revenue_mid', 'revenue_low', 'revenue_high',
            'hot_reasons_text',
            'avg_daily_views', 'trend_label',
            'channel_title', 'published_at', 'days_since_published',
            'duration', 'url', 'video_id'
        ]
        df = df[column_order]
        
        # 重命名列为中文
        df.columns = [
            '热度指数', '视频标题', '播放量', '点赞数', '评论数',
            '互动率(%)', '预估收益(中值$)', '预估收益(低$)', '预估收益(高$)',
            '爆红原因', '日均播放', '趋势标签',
            '频道名称', '发布日期', '发布天数',
            '时长', '视频链接', '视频ID'
        ]
        
        # 导出Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='视频分析', index=False)
            
            # 获取工作表
            worksheet = writer.sheets['视频分析']
            
            # 设置列宽
            column_widths = {
                'A': 12,  # 热度指数
                'B': 50,  # 视频标题
                'C': 12,  # 播放量
                'D': 10,  # 点赞数
                'E': 10,  # 评论数
                'F': 12,  # 互动率
                'G': 20,  # 频道名称
                'H': 12,  # 发布日期
                'I': 10,  # 发布天数
                'J': 10,  # 时长
                'K': 40,  # 视频链接
                'L': 15,  # 视频ID
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
        
        abs_path = os.path.abspath(filename)
        print(f"✅ 数据已导出到: {abs_path}")
        return abs_path
    
    def analyze(self, 
                input_type: str,
                input_value: str,
                max_results: int = 50,
                min_views: int = 50000,
                min_engagement: float = 2.0,
                export: bool = True,
                language: Optional[str] = None,
                region: Optional[str] = None) -> List[Dict]:
        """
        完整分析流程
        
        Args:
            input_type: 输入类型 ('keyword' 或 'channel')
            input_value: 搜索关键词或频道URL
            max_results: 最多分析视频数
            min_views: 最低播放量筛选
            min_engagement: 最低互动率筛选
            export: 是否导出Excel
            
        Returns:
            分析结果列表
        """
        print(f"\n{'='*60}")
        print(f"🎬 YouTube视频热度分析工具")
        print(f"{'='*60}\n")
        
        # 1. 获取视频ID
        print(f"📺 正在获取视频列表...")
        if input_type == 'keyword':
            video_ids = self.search_videos(input_value, max_results, language=language, region=region)
        elif input_type == 'channel':
            video_ids = self.get_channel_videos(input_value, max_results)
        else:
            print("❌ 无效的输入类型")
            return []
        
        if not video_ids:
            print("❌ 未找到视频")
            return []
        
        # 2. 获取视频详情
        print(f"\n📊 正在获取视频详细数据...")
        videos = self.get_video_details(video_ids)
        
        if not videos:
            print("❌ 获取视频详情失败")
            return []
        
        # 3. 筛选适合搬运的视频
        print(f"\n🔍 正在筛选适合搬运的视频...")
        print(f"   筛选条件: 播放量≥{min_views:,}, 互动率≥{min_engagement}%, 14天内发布, 时长1-15分钟")
        filtered_videos = self.filter_videos(videos, min_views, min_engagement)
        
        # 4. 显示Top 10
        print(f"\n🏆 Top 10 热门视频:")
        print(f"{'-'*60}")
        for i, video in enumerate(filtered_videos[:10], 1):
            print(f"{i}. [{video['heat_score']:.0f}分] {video['title'][:40]}...")
            print(f"   📈 {video['view_count']:,}播放 | 👍 {video['like_count']:,} | 💬 {video['comment_count']:,}")
            print(f"   💰 预估收益: ${video['revenue_mid']:,} (低:${video['revenue_low']:,} - 高:${video['revenue_high']:,})")
            print(f"   ⭐ 爆红原因: {', '.join(video.get('hot_reasons', [])[:3])}")
            print(f"   📊 趋势: {video.get('trend_label')} | 日均 {video.get('avg_daily_views'):,} 播放")
            print(f"   🔗 {video['url']}\n")
        
        # 5. 导出Excel
        if export and filtered_videos:
            print(f"\n💾 正在导出数据...")
            self.export_to_excel(filtered_videos)
        
        print(f"\n{'='*60}")
        print(f"✅ 分析完成! 共找到 {len(filtered_videos)} 个适合搬运的欧美热门视频")
        print(f"💡 提示: 这些视频在欧美地区受欢迎，时长适中，适合本地化后搬运到小红书/抖音")
        print(f"{'='*60}\n")
        
        return filtered_videos


def main():
    """主程序"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       YouTube欧美热门视频分析工具 v2.0                    ║
    ║    筛选适合搬运到小红书/抖音的欧美地区热门内容            ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 读取API密钥
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("\n⚠️ 请先设置YouTube API密钥!")
        print("\n获取API密钥步骤:")
        print("1. 访问 https://console.cloud.google.com/")
        print("2. 创建项目 → 启用YouTube Data API v3")
        print("3. 创建凭据 → API密钥")
        print("\n设置方法:")
        print("Windows: set YOUTUBE_API_KEY=你的密钥")
        print("或在config.json中配置")
        
        # 尝试从config.json读取
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('youtube_api_key')
        
        if not api_key:
            return
    
    analyzer = YouTubeAnalyzer(api_key)
    
    # 交互式选择
    print("\n请选择分析模式:")
    print("1. 按关键词搜索")
    print("2. 分析指定频道")
    
    choice = input("\n请输入选项 (1/2): ").strip()
    
    if choice == '1':
        keyword = input("请输入搜索关键词 (英文): ").strip()
        if keyword:
            analyzer.analyze('keyword', keyword, max_results=50)
    elif choice == '2':
        channel_url = input("请输入频道URL或ID: ").strip()
        if channel_url:
            analyzer.analyze('channel', channel_url, max_results=50)
    else:
        print("❌ 无效的选项")


if __name__ == "__main__":
    main()
