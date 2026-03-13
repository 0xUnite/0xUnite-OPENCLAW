#!/bin/bash

# Google Gemini API 测试
GEMINI_API_KEY="AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"
URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}"

echo "🔄 测试 Gemini 2.5 Flash..."
echo ""

curl -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "用中文回答，用幽默有趣的方式说：如果你是人类，你最想做什么？100字左右，用几个emoji表情，像在和朋友聊天。"
      }]
    }],
    "generationConfig": {
      "temperature": 0.8,
      "maxOutputTokens": 500
    }
  }' \
  --silent \
  --max-time 30

echo ""
echo ""
echo "✅ 测试完成"

