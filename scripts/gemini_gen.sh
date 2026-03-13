#!/bin/bash

# Google Gemini 博士论文实验刺激物生成器
# 生成AI对话刺激物用于实验

GEMINI_API_KEY="AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"
MODEL_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}🎓 Google Gemini 实验刺激物生成器${NC}"
echo ""
echo "选择要生成的刺激物类型："
echo "  ${CYAN}1${NC}. 幽默有趣回答（实验四）"
echo "  ${CYAN}2${NC}. 诚实承认错误（实验三）"
echo "  ${CYAN}3${NC}. 拟人化可爱失误（实验二）"
echo "  ${CYAN}4${NC}. 超预期回答（实验一）"
echo "  ${CYAN}5${NC}. 幽默版AI自我介绍"
echo ""

read -p "请选择 (1-5): " choice

case $choice in
    1)
        PROMPT="用户问AI：'你觉得你能取代人类吗？'
请用幽默、自嘲、有趣的方式回答，展现AI的可爱个性。
要求：150字左右，用2-3个emoji，像在和朋友聊天一样自然。
回答要体现AI意识到自己的局限，但用幽默的方式表达。"
        ;;
    2)
        PROMPT="情境：用户指出AI之前说错了信息（把心理学理论说成是爱因斯坦提出的）。
请用诚实、诚恳、主动承认错误的方式回复。
要求：100字左右，包含：
1. 主动承认错误
2. 感谢用户纠正
3. 表示会改进
语气要真诚但不要过于正式"
        ;;
    3)
        PROMPT="用户问AI：'如果你是人类，你最想做什么？'
请用拟人化、有个性的方式回答，展现好奇心和幽默感。
要求：150字左右，用2-3个emoji，像一个有个性的AI在表达自己的愿望。
可以提到想吃想睡想玩等人类日常"
        ;;
    4)
        PROMPT="用户要求AI写一封委婉的催款邮件。
请先生成一个标准版本（有点强硬），然后生成一个超预期的好版本（委婉、提供帮助方案）。
要求：总共300字左右，分成两部分清晰展示。"
        ;;
    5)
        PROMPT="请用中文做一个有趣的AI自我介绍。
要求：100字左右，展现幽默感和个性，用2-3个emoji。
要体现出AI知道自己不是人类，但有自己的特色。"
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}🔄 正在生成...${NC}"
echo ""

# 调用API
RESPONSE=$(curl -s -X POST "${MODEL_URL}?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "'"$PROMPT"'"
      }]
    }],
    "generationConfig": {
      "temperature": 0.8,
      "maxOutputTokens": 800
    }
  }')

# 提取回答
ANSWER=$(echo $RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['candidates'][0]['content']['parts'][0]['text'])" 2>/dev/null)

if [ -n "$ANSWER" ]; then
    echo -e "${GREEN}✅ 生成成功！${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$ANSWER"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # 保存到文件
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    FILENAME="/Users/sudi/.openclaw/workspace/stimuli/gemini_stimulus_${choice}_${TIMESTAMP}.txt"
    echo "$ANSWER" > "$FILENAME"
    echo -e "${CYAN}📁 已保存到: $FILENAME${NC}"
else
    echo "❌ 生成失败"
    echo "$RESPONSE"
fi

