#!/bin/bash

# ChatGPT 一键提问脚本

echo "🚀 开始向 ChatGPT 提问..."
echo ""

# 1. 打开 ChatGPT
echo "📂 打开 ChatGPT..."
open -a "ChatGPT"

# 2. 提示用户
echo ""
echo "✅ ChatGPT 已打开！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 请手动操作："
echo ""
echo "   1. 确保 ChatGPT 输入框已激活"
echo "   2. 按 Command+V 粘贴以下问题："
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
cat << 'EOF'
我是管理学博士生，研究题目是'AI服务失误对消费者信任的影响'，核心假设是：AI的某些'失误'可能产生意外积极的结果（如Serendipity、Pratfall Effect）。

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
4. 指出实验设计的不足之处
EOF
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   3. 按回车发送"
echo ""
echo "💬 ChatGPT 回答后，把答案复制发给我"
echo "   我会自动整理到问卷中！"

