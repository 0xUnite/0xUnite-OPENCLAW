#!/bin/bash

# Kimi API 测试脚本
KIMI_API_KEY="sk-Keua0eN6DdE7kzyRUDrFxOVqRmWEkW1Pr9msiCKDp0uJIQMa"
URL="https://api.moonshot.cn/v1/chat/completions"

echo "🔄 正在调用 Kimi API..."

curl -X POST "$URL" \
  -H "Authorization: Bearer $KIMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "moonshot-v1-8k",
    "messages": [
      {
        "role": "user",
        "content": "你好，请用中文介绍一下你自己，并回答这个问题：如果你是人类，你最想做什么？用幽默有趣的方式回答。"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }' \
  --silent \
  --max-time 30

echo ""
echo "✅ 测试完成"

