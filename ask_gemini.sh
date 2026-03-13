#!/bin/bash

# 使用 curl 调用 Gemini API

GEMINI_API_KEY="AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"
MODEL_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

QUESTION='我是管理学博士生，研究题目是"AI服务失误对消费者信任的影响"，核心假设是：AI的某些"失误"可能产生意外积极的结果（如Serendipity、Pratfall Effect）。

我已经设计了5个情境实验：
A. 意外创意：AI失误→更好的创意
B. 幽默对话：AI幽默回答荒谬问题  
C. 诚实道歉：AI承认错误
D. 意外功能：AI给得比预期多
E. 对照组：无失误

请帮我：
1. 评估这些情境是否有效捕捉核心假设
2. 推荐成熟量表测量意外惊喜、拟人化、信任
3. 建议如何优化问卷题目
4. 指出实验设计的不足之处'

echo "🔄 正在调用 Gemini API..."
echo ""

# 构建请求（简化版）
curl -s -X POST "${MODEL_URL}?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "请用中文回答以下问题：请帮我评估这5个AI失误情境实验设计是否有效，并推荐测量意外惊喜、拟人化感知、信任修复的成熟量表，最后指出问卷的不足之处。情境包括：A.意外创意 B.幽默对话 C.诚实道歉 D.意外功能 E.对照组无失误"
      }]
    }],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 2000
    }
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
try:
    answer = data['candidates'][0]['content']['parts'][0]['text']
    print('='*70)
    print('✅ Gemini 回答：')
    print('='*70)
    print(answer)
    print('='*70)
    
    # 保存
    with open('/Users/sudi/.openclaw/workspace/gemini_advice.md', 'w', encoding='utf-8') as f:
        f.write('# Gemini 问卷优化建议\n\n')
        f.write('**时间**: 2026-02-08\n\n')
        f.write('## 完整回答\n\n')
        f.write(answer)
    print('\n✅ 已保存到 /Users/sudi/.openclaw/workspace/gemini_advice.md')
except Exception as e:
    print(f'解析错误: {e}')
    print('原始响应:')
    print(json.dumps(data, indent=2, ensure_ascii=False))
"