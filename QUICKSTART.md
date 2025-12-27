# 🎯 YouTube视频热度分析工具 - 快速开始指南

## 🚀 5分钟快速上手

### 第一步：安装依赖包

打开PowerShell，执行：

```powershell
cd \workspace\youtube_analyzer
pip install -r requirements.txt
```

### 第二步：获取API密钥

1. 访问: https://console.cloud.google.com/
2. 创建项目 → 启用 "YouTube Data API v3"
3. 创建凭据 → API密钥
4. 复制密钥

### 第三步：配置密钥

**临时使用（当前会话）：**
```powershell
$env:YOUTUBE_API_KEY="粘贴你的密钥"
```

**永久使用：**
编辑 `config.json`，将密钥填入第2行

### 第四步：运行工具

```powershell
python youtube_analyzer.py
```

按提示选择：
- 输入 `1` → 搜索关键词（如：AI tutorial）
- 输入 `2` → 分析频道（粘贴频道URL）

### 第五步：查看结果

程序会：
1. 自动搜索和分析视频
2. 显示Top 10热门视频
3. 导出Excel到 `output/` 目录

打开Excel查看完整数据！

---

## 💡 实用技巧

### 技巧1：找爆款选题
```
搜索关键词: "productivity tips"
→ 查看热度最高的视频
→ 这些就是值得搬运的选题
```

### 技巧2：分析竞争对手
```
输入竞争对手的频道URL
→ 查看他们哪些视频最火
→ 学习他们的成功经验
```

### 技巧3：批量分析
```powershell
python batch_analyzer.py
```
自动分析多个关键词，一次性找到100+个优质视频

---

## 📊 看懂输出数据

Excel表格中重点关注：

| 指标 | 含义 | 建议 |
|------|------|------|
| **热度指数** | 综合评分 | >10000 值得搬运 |
| **播放量** | 观看人数 | >100万 基础热度好 |
| **互动率** | 粉丝活跃度 | >3% 内容质量高 |
| **发布天数** | 时效性 | <30天 正当红 |

---

## ⚡ 常见问题速查

**Q: 运行报错 "No module named 'googleapiclient'"？**
```powershell
pip install google-api-python-client
```

**Q: 提示 "请先设置API密钥"？**
```powershell
$env:YOUTUBE_API_KEY="你的密钥"
```

**Q: 搜索结果为0？**
→ 关键词太冷门，换个热门词试试（如 tutorial、tips、review）

**Q: 每天能分析多少次？**
→ 免费配额约100次/天，足够使用

---

## 🎬 下一步行动

1. ✅ 运行工具，分析你的领域关键词
2. ✅ 筛选出10-20个高热度视频
3. ✅ 开始制作第一个搬运视频
4. ✅ 发布到抖音/小红书/视频号
5. ✅ 追踪数据，优化策略

**现在就开始吧！** 🚀

---

需要帮助？查看完整文档：[README.md](README.md)
