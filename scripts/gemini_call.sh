#!/bin/bash

# Google Gemini 高效调用脚本
# 用途：生成博士论文实验刺激物

# API 配置
GEMINI_API_KEY="AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"
BASE_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Google Gemini API 调用工具${NC}"
echo ""
echo "可用命令："
echo "  1. 幽默回答 - 生成有趣的AI对话"
echo "  2. 诚实承认 - 生成承认错误的对话"
echo "  3. 拟人化 - 生成拟人化的AI回答"
echo "  4. 超预期 - 生成超出预期的回答"
echo "  5. 定制问题 - 输入你自己的问题"
echo ""

# 读取用户输入
read -p "请选择功能 (1-5): " choice

case $choice in
    1)
        PROMPT="请用幽默、有趣、自嘲的方式回答这个问题：你觉得你能取代人类吗？回答要像在和朋友聊天，用emoji表情，展现出AI的可爱个性。200字左右。"
        ;;
    2)
        PROMPT="用户指出你之前说错了信息（把心理学理论说成是爱因斯坦提出的），请用诚实、诚恳的方式承认错误，感谢用户的纠正，并表示会改进。150字左右。"
        ;;
    3)
        PROMPT="请用拟人化的方式回答：如果你是人类，你最想做什么？要展现出好奇心和个性，像在和好朋友聊天一样。200字左右。"
        ;;
    4)
        PROMPT="用户请你写一封委婉的催款邮件。请先给出一个有点强硬的版本（失误），然后给出一个超出预期的好版本（委婉、提供帮助方案）。分别展示。300字左右。"
        ;;
    5)
        read -p "请输入你的问题: " PROMPT
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}🔄 正在调用 Gemini API...${NC}"
echo ""

# 构建请求
curl -X POST "${BASE_URL}?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "'"$PROMPT"'"
      }]
    }],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 1000,
      "topP": 0.95
    }
  }' \
  --silent | python3 -m json.tool 2>/dev/null | grep -A 50 "text" | tail -n +2 | sed 's/"text"://g' | sed 's/^[ \t]*//' | sed 's/"/ /g' | sed 's/\\n/\n/g'

echo ""
echo -e "${GREEN}✅ 调用完成${NC}"

