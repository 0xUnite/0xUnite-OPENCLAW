#!/usr/bin/env python3
"""
测试 Kimi API 调用
"""

import requests
import json

# Kimi API 配置
KIMI_API_KEY = "sk-Keua0eN6DdE7kzyRUDrFxOVqRmWEkW1Pr9msiCKDp0uJIQMa"
BASE_URL = "https://api.moonshot.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {KIMI_API_KEY}",
    "Content-Type": "application/json"
}

# 测试对话
data = {
    "model": "moonshot-v1-8k",
    "messages": [
        {
            "role": "user",
            "content": "你好，请用中文介绍一下你自己，并回答这个问题：如果你是人类，你最想做什么？"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

print("🔄 正在调用 Kimi API...")

try:
    response = requests.post(
        BASE_URL,
        headers=headers,
        json=data,
        timeout=30
    )
    
    result = response.json()
    
    print("\n✅ API 调用成功！\n")
    print("📊 响应结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
except Exception as e:
    print(f"❌ API 调用失败：{e}")

