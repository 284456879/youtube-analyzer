#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证工具安装
"""

def test_imports():
    """测试依赖包是否正确安装"""
    print("🔍 检查依赖包...")
    
    try:
        import pandas
        print("✅ pandas 安装成功")
    except ImportError:
        print("❌ pandas 未安装")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl 安装成功")
    except ImportError:
        print("❌ openpyxl 未安装")
        return False
    
    try:
        from googleapiclient.discovery import build
        print("✅ google-api-python-client 安装成功")
    except ImportError:
        print("❌ google-api-python-client 未安装")
        return False
    
    return True


def test_config():
    """测试配置文件"""
    print("\n🔍 检查配置...")
    
    import os
    import json
    
    # 检查环境变量
    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key:
        print(f"✅ 环境变量 YOUTUBE_API_KEY 已设置 (长度: {len(api_key)})")
        return True
    else:
        print("⚠️ 环境变量 YOUTUBE_API_KEY 未设置")
    
    # 检查配置文件
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            api_key = config.get('youtube_api_key')
            if api_key and api_key != "你的YouTube_API_密钥":
                print("✅ config.json 中已配置API密钥")
                return True
            else:
                print("⚠️ config.json 中API密钥未配置")
    
    return False


def test_analyzer():
    """测试分析器类"""
    print("\n🔍 测试分析器类...")
    
    try:
        from youtube_analyzer import YouTubeAnalyzer
        print("✅ YouTubeAnalyzer 类导入成功")
        
        # 测试初始化（使用假密钥）
        analyzer = YouTubeAnalyzer("TEST_KEY")
        print("✅ YouTubeAnalyzer 初始化成功")
        
        # 测试方法存在
        assert hasattr(analyzer, 'search_videos'), "缺少 search_videos 方法"
        assert hasattr(analyzer, 'get_video_details'), "缺少 get_video_details 方法"
        assert hasattr(analyzer, 'filter_videos'), "缺少 filter_videos 方法"
        assert hasattr(analyzer, 'export_to_excel'), "缺少 export_to_excel 方法"
        print("✅ 所有核心方法都存在")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("📋 YouTube分析工具 - 安装测试")
    print("=" * 60)
    
    results = []
    
    # 测试1：依赖包
    results.append(("依赖包安装", test_imports()))
    
    # 测试2：配置
    results.append(("API密钥配置", test_config()))
    
    # 测试3：分析器
    results.append(("分析器类", test_analyzer()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n通过率: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！工具已准备就绪！")
        print("\n下一步：")
        print("1. 如果还未配置API密钥，请参考 QUICKSTART.md")
        print("2. 运行: python youtube_analyzer.py")
    else:
        print("\n⚠️ 部分测试失败，请检查：")
        if not results[0][1]:
            print("- 运行: pip install -r requirements.txt")
        if not results[1][1]:
            print("- 配置API密钥（参考 QUICKSTART.md）")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
