#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简易网页版入口 (Flask)
运行: python web_app.py
访问: http://localhost:5000
"""
import json
import os
from typing import Any, Dict
from flask import Flask, jsonify, render_template, request

from youtube_analyzer import YouTubeAnalyzer

app = Flask(__name__, template_folder="templates", static_folder="static")


def _load_config() -> Dict[str, Any]:
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


CONFIG = _load_config()
ANALYSIS_SETTINGS = CONFIG.get("analysis_settings", {})
SUGGESTIONS = CONFIG.get("search_keywords_suggestions", [
    "life hacks", "cooking tips", "DIY crafts", "quick recipes",
    "home workout", "cleaning tips", "food hacks", "tech review",
    "makeup tutorial", "pet care"
])


def _get_api_key() -> str:
    env_key = os.getenv("YOUTUBE_API_KEY")
    if env_key:
        return env_key
    return CONFIG.get("youtube_api_key", "")


# 打印启动信息
print("-" * 40)
if os.getenv("YOUTUBE_API_KEY"):
    print("✅ Using API Key from Environment Variable")
elif CONFIG.get("youtube_api_key"):
    print("✅ Using API Key from config.json")
else:
    print("⚠️  No API Key found! Please set YOUTUBE_API_KEY or check config.json")
print("-" * 40)


def _get_setting(name: str, default: Any):
    return ANALYSIS_SETTINGS.get(name, default)


def _parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["GET"])
def api_analyze():
    api_key = _get_api_key()
    if not api_key:
        return jsonify({"error": "Missing API key. Set YOUTUBE_API_KEY or config.json"}), 400

    input_type = request.args.get("input_type", "keyword")
    input_value = request.args.get("value", "").strip()
    if not input_value:
        return jsonify({"error": "参数 value 不能为空"}), 400

    max_results = _parse_int(request.args.get("max_results"), _get_setting("default_max_results", 30))
    min_views = _parse_int(request.args.get("min_views"), _get_setting("min_views", 50000))
    min_engagement = _parse_float(request.args.get("min_engagement"), _get_setting("min_engagement_rate", 2.0))
    max_days = _parse_int(request.args.get("max_days"), _get_setting("max_days_since_published", 14))
    min_duration = _parse_int(request.args.get("min_duration"), _get_setting("min_duration_seconds", 60))
    max_duration = _parse_int(request.args.get("max_duration"), _get_setting("max_duration_seconds", 900))
    cpm_low = _parse_float(request.args.get("cpm_low"), _get_setting("cpm_low", 2.0))
    cpm_high = _parse_float(request.args.get("cpm_high"), _get_setting("cpm_high", 4.0))

    analyzer = YouTubeAnalyzer(
        api_key,
        cpm_low=cpm_low,
        cpm_high=cpm_high,
        default_language=_get_setting("language", "en"),
        default_region_code=_get_setting("region_code", "US")
    )

    # 这里禁止导出Excel，保持响应快速
    # 输入类型与合规性校验
    if input_type == "channel":
        v = input_value
        is_valid = (v.startswith("http") and ("/channel/" in v or "/@" in v)) or (
            len(v) == 24 and all(ch.isalnum() or ch in "-_" for ch in v)
        )
        if not is_valid:
            return jsonify({"error": "请输入有效的频道URL或ID（例如 https://www.youtube.com/@xxxx 或 https://www.youtube.com/channel/UC... 或 24位频道ID）"}), 400

    results = analyzer.analyze(
        input_type=input_type,
        input_value=input_value,
        max_results=max_results,
        min_views=min_views,
        min_engagement=min_engagement,
        export=False,
        language=request.args.get("language") or _get_setting("language", "en"),
        region=request.args.get("region") or _get_setting("region_code", "US")
    )

    # 再次按前端参数过滤时长范围（analyze内部已按默认值过滤，但这里尊重前端传入覆盖）
    filtered = [
        v for v in results
        if min_duration <= v.get("duration_seconds", 0) <= max_duration
        and v.get("days_since_published", 9999) <= max_days
    ]

    return jsonify({
        "count": len(filtered),
        "items": filtered,
        "params": {
            "input_type": input_type,
            "input_value": input_value,
            "max_results": max_results,
            "min_views": min_views,
            "min_engagement": min_engagement,
            "max_days": max_days,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "cpm_low": cpm_low,
            "cpm_high": cpm_high
        }
    })


@app.route("/api/suggestions", methods=["GET"])
def api_suggestions():
    """返回关键词建议列表"""
    return jsonify({
        "suggestions": SUGGESTIONS
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
