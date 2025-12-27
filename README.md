# 🎬 YouTube视频热度分析工具

> 自动分析YouTube视频数据，筛选高热度内容，一键导出Excel分析报表

## ✨ 核心功能

- ✅ **关键词搜索**: 输入关键词，自动搜索相关高热度视频
- ✅ **频道分析**: 输入频道URL，分析该频道所有视频
- ✅ **智能筛选**: 自动筛选播放量>100万、互动率>3%的优质内容
- ✅ **热度计算**: 独家热度指数算法，精准评估视频潜力
- ✅ **Excel导出**: 一键导出格式化报表，包含所有关键数据
- ✅ **数据全面**: 播放量、点赞数、评论数、互动率、发布时间等

## 📊 热度指数算法

```
热度指数 = (播放量 × 0.5 + 点赞数 × 20 + 评论数 × 10) / 发布天数
```

这个算法综合考虑：
- **播放量**: 基础热度
- **点赞数**: 内容质量（权重×20）
- **评论数**: 互动程度（权重×10）
- **发布天数**: 时间衰减因子

## 🚀 快速开始

### 1. 安装依赖

```bash
cd \workspace\youtube_analyzer
pip install -r requirements.txt
```

### 2. 获取YouTube API密钥

#### 方法一：Google Cloud Console（推荐）

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **YouTube Data API v3**
   - 左侧菜单 → API和服务 → 库
   - 搜索 "YouTube Data API v3"
   - 点击 "启用"
4. 创建API密钥
   - 左侧菜单 → API和服务 → 凭据
   - 点击 "创建凭据" → "API密钥"
   - 复制生成的密钥

#### 免费额度
- 每日配额: **10,000** 单位
- 一次搜索: 约100单位
- 可分析约 **100次/天**（足够使用）

### 3. 配置API密钥

#### 方法A：环境变量（推荐）

**Windows PowerShell:**
```powershell
$env:YOUTUBE_API_KEY="你的API密钥"
```

**Windows CMD:**
```cmd
set YOUTUBE_API_KEY=你的API密钥
```

#### 方法B：配置文件

编辑 `config.json`:
```json
{
  "youtube_api_key": "你的实际API密钥",
  ...
}
```

### 4. 运行工具

```bash
python youtube_analyzer.py
```

## 💡 使用示例

### 示例1：按关键词搜索

```
请选择分析模式:
1. 按关键词搜索
2. 分析指定频道

请输入选项 (1/2): 1
请输入搜索关键词 (英文): AI tutorial

📺 正在获取视频列表...
✅ 找到 50 个相关视频

📊 正在获取视频详细数据...
✅ 成功获取 50 个视频的详细信息

🔍 正在筛选高质量视频...
✅ 筛选出 15 个高质量视频

🏆 Top 10 热门视频:
1. [45231分] How to Use ChatGPT for Beginners...
   📈 3,500,000播放 | 👍 85,000 | 💬 2,300
   🔗 https://www.youtube.com/watch?v=xxxxx

💾 正在导出数据...
✅ 数据已导出到: \workspace\youtube_analyzer\output\youtube_analysis_20251227_143025.xlsx
```

### 示例2：分析频道

```
请输入选项 (1/2): 2
请输入频道URL或ID: https://www.youtube.com/@TechChannel

📺 正在获取视频列表...
✅ 从频道获取 50 个视频

📊 正在获取视频详细数据...
✅ 成功获取 50 个视频的详细信息
...
```

## 📁 输出文件说明

导出的Excel文件包含以下列：

| 列名 | 说明 |
|------|------|
| 热度指数 | 综合热度评分（越高越好）|
| 视频标题 | 完整标题 |
| 播放量 | 总播放次数 |
| 点赞数 | 点赞数量 |
| 评论数 | 评论数量 |
| 互动率(%) | (点赞+评论)/播放量×100 |
| 频道名称 | 发布者频道 |
| 发布日期 | 视频发布日期 |
| 发布天数 | 距今天数 |
| 时长 | 视频时长 |
| 视频链接 | YouTube观看链接 |
| 视频ID | YouTube视频ID |

## 🎯 筛选标准（可自定义）

默认筛选条件：
- ✅ 播放量 ≥ **1,000,000**（100万）
- ✅ 互动率 ≥ **3.0%**
- ✅ 发布时间 ≤ **30天**

在 `config.json` 中修改：
```json
{
  "analysis_settings": {
    "min_views": 500000,        // 改为50万
    "min_engagement_rate": 2.0,  // 改为2%
    "max_days_since_published": 60  // 改为60天
  }
}
```

## 🔧 高级用法

### 编程方式调用

```python
from youtube_analyzer import YouTubeAnalyzer

# 初始化
analyzer = YouTubeAnalyzer(api_key="你的密钥")

# 分析关键词
results = analyzer.analyze(
    input_type='keyword',
    input_value='AI tools',
    max_results=50,
    min_views=1000000,
    min_engagement=3.0,
    export=True
)

# 打印结果
for video in results[:10]:
    print(f"{video['title']}: {video['heat_score']}分")
```

### 批量分析多个关键词

```python
keywords = ['AI tutorial', 'Python programming', 'productivity tips']

for keyword in keywords:
    print(f"\n分析关键词: {keyword}")
    analyzer.analyze('keyword', keyword)
```

## 📈 实际应用场景

### 1. 内容选品（最重要！）
在制作视频前，先分析哪些主题最受欢迎，避免浪费时间

### 2. 竞品分析
研究同行频道的热门内容，学习成功经验

### 3. 趋势追踪
定期分析，发现新兴热点话题

### 4. 频道优化
分析自己频道的视频表现，找出优化方向

## ⚠️ 注意事项

### API配额管理
- 每日10,000配额，请合理使用
- 一次分析50个视频约消耗150-200配额
- 建议：每天分析不超过50次

### 最佳实践
1. **先小范围测试**: 第一次用先搜索10-20个视频
2. **保存API密钥**: 不要泄露到公开代码库
3. **定期备份数据**: Excel文件保存在 `output/` 目录
4. **关注版权**: 筛选出的视频需要自行确认版权状态

## 🐛 常见问题

### Q1: 提示"请先设置YouTube API密钥"？
**A**: 按照上面的步骤获取API密钥，并通过环境变量或config.json配置

### Q2: 提示"超出配额"？
**A**: 每日配额10,000已用完，明天再试或创建新的API项目

### Q3: 搜索结果为0？
**A**: 可能关键词太冷门，尝试更热门的关键词（如"tutorial"、"review"）

### Q4: 筛选后没有视频？
**A**: 筛选条件太严格，可以降低 `min_views` 或 `min_engagement_rate`

### Q5: 能分析中文视频吗？
**A**: 可以！只需在搜索时输入中文关键词，或分析中文频道

## 🚀 下一步计划

- [ ] 添加yt-dlp备选方案（无需API key）
- [ ] 支持批量关键词分析
- [ ] 添加数据可视化图表
- [ ] 支持定时任务自动分析
- [ ] 集成抖音/B站竞品对比

## 📞 技术支持

- 项目路径: `\workspace\youtube_analyzer\`
- 输出目录: `\workspace\youtube_analyzer\output\`
- 配置文件: `\workspace\youtube_analyzer\config.json`

## 🌐 部署上线指南 (Deployment)

如果你想把这个工具发布到公网，推荐使用 **Render.com** (免费且简单)。

### 1. 准备工作
- 注册 [GitHub](https://github.com/) 账号
- 注册 [Render](https://render.com/) 账号
- 购买一个域名 (推荐 Namecheap)

### 2. 上传代码
1. 在 GitHub 创建新仓库 `youtube-analyzer`
2. 将本地代码上传到 GitHub (注意：`.gitignore` 会自动忽略 `config.json`，保护你的密钥)

### 3. 在 Render 部署
1. 点击 **New +** -> **Web Service**
2. 连接你的 GitHub 仓库
3. 配置如下：
   - **Name**: `youtube-analyzer`
   - **Region**: `US West (Oregon)` (离 YouTube 服务器近)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
4. **关键步骤**：在 "Environment" 标签页添加环境变量：
   - Key: `YOUTUBE_API_KEY`
   - Value: `你的API密钥`

### 4. 绑定域名
1. 在 Render 的 Settings -> Custom Domains 添加你的域名 (如 `www.tubetrends.io`)
2. 按照提示在域名注册商处添加 CNAME 记录

## 📄 许可证

MIT License - 自由使用和修改

---

**现在就开始使用，发现下一个爆款视频！** 🎉
