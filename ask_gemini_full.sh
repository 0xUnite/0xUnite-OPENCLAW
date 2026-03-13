#!/bin/bash

GEMINI_API_KEY="AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"

echo "🔄 正在问 Gemini（完整版）..."

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "请用中文详细回答：1.评估5个AI情境实验是否有效：意外创意、幽默对话、诚实道歉、意外功能、对照组。2.推荐测量意外惊喜、拟人化感知、信任修复的成熟量表，每个至少2个，带作者年份。3.指出问卷设计的3个主要不足。4.如何优化。"}]}],
    "generationConfig": {"maxOutputTokens": 3000, "temperature": 0.7}
  }' > /tmp/gemini_response.json 2>/dev/null

echo "✅ 完成！回答已保存"
