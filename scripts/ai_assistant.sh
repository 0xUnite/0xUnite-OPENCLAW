#!/bin/bash

# AI助手管理工具
# 用途：快速启动AI应用，或让AI帮你生成更好的回答

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🤖 AI助手管理工具${NC}"
echo ""
echo "选择操作："
echo "  1. 启动 ChatGPT"
echo "  2. 启动 Claude"
echo "  3. 让 AI 帮你生成更好的回答（高级功能）"
echo "  4. 查看我的 AI 能力"
echo "  5. 退出"
echo ""

read -p "请选择 (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 启动 ChatGPT...${NC}"
        open -a "ChatGPT"
        echo "✅ ChatGPT 已启动"
        ;;
    2)
        echo -e "${GREEN}🚀 启动 Claude...${NC}"
        open -a "Claude"
        echo "✅ Claude 已启动"
        ;;
    3)
        echo -e "${YELLOW}💡 高级功能：将你的问题交给 AI 分析${NC}"
        echo ""
        echo "请输入你想问的问题："
        read -p "> " user_question
        
        echo ""
        echo "🔄 正在分析你的问题..."
        echo ""
        
        # 分析问题类型并给出优化建议
        if echo "$user_question" | grep -qi "翻译\|翻译成"; then
            echo -e "${GREEN}📝 检测到翻译需求${NC}"
            echo "优化建议："
            echo "  • 提供源语言和目标语言"
            echo "  • 说明是正式/口语翻译"
            echo "  • 给出具体例子"
            echo ""
            echo "优化后的提问示例："
            echo "  '请将以下中文句子翻译成地道的美式英语：'"
            echo "  '客户：我想退货。'"
            echo "  '请用口语化的方式，不要太正式。'"
        elif echo "$user_question" | grep -qi "代码\|编程\|code\|program"; then
            echo -e "${GREEN}💻 检测到编程需求${NC}"
            echo "优化建议："
            echo "  • 说明编程语言"
            echo "  • 提供上下文/代码片段"
            echo "  • 说明预期结果和实际结果"
            echo ""
            echo "优化后的提问示例："
            echo "  '我在用 Python 3.9 写一个函数，'"
            echo "  '目标是计算列表平均值但排除空值。'"
            echo "  '我的代码总是报错 IndexError，请帮我看看。'"
        elif echo "$user_question" | grep -qi "总结\|摘要\|summarize"; then
            echo -e "${GREEN}📊 检测到总结需求${NC}"
            echo "优化建议："
            echo "  • 提供要总结的内容"
            echo "  • 说明总结长度（简短/详细）"
            echo "  • 指出重点关注的方面"
            echo ""
            echo "优化后的提问示例："
            echo "  '请用3句话总结以下文章的核心观点：'"
            echo "  '重点关注 AI 对就业市场的影响。'"
        else
            echo -e "${GREEN}💡 通用优化建议${NC}"
            echo "  • 提供具体背景信息"
            echo "  • 说明你需要的答案格式"
            echo "  • 给出约束条件或偏好"
            echo ""
            echo "优化后的提问示例："
            echo "  '在以下场景下：_______'"
            echo "  '我想达到：_______'"
            echo "  '请给出具体建议，最好有例子。'"
        fi
        
        echo ""
        echo "---"
        echo ""
        echo "💡 提示：你也可以直接复制上面的优化示例到 ChatGPT/Claude 中提问！"
        ;;
    4)
        echo -e "${GREEN}🎯 我的 AI 能力${NC}"
        echo ""
        echo "我可以帮你："
        echo "  ✅ 分析问题并优化提问方式"
        echo "  ✅ 搜索和收集信息"
        echo "  ✅ 整理和分析数据"
        echo "  ✅ 写代码和调试"
        echo "  ✅ 回答学术研究问题"
        echo "  ✅ 管理你的 AI 应用（ChatGPT、Claude）"
        echo ""
        echo "在某些复杂问题上，ChatGPT/Claude 可能更擅长，"
        echo "我可以帮你启动它们并优化你的提问方式！"
        ;;
    5)
        echo "再见！👋"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac

echo ""
echo "按回车键返回菜单..."
read

# 重新运行脚本
bash "$0"

