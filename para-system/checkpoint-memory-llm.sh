#!/bin/bash
# ~/.openclaw/workspace/para-system/checkpoint-memory-llm.sh
# 检查点脚本 - 每6小时自动提取关键记忆
# 输出: 更新 MEMORY.md

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
OLLAMA_URL="http://127.0.0.1:11434/api/generate"
MODEL="qwen3:latest"

# 读取今日日志
TODAY=$(date +%Y-%m-%d)
DAILY_LOG="$WORKSPACE/memory/$TODAY.md"

if [ ! -f "$DAILY_LOG" ]; then
    echo "[$TODAY] 无今日日志，跳过检查点"
    exit 0
fi

# 获取最近100行日志
RECENT_CONTENT=$(tail -100 "$DAILY_LOG" 2>/dev/null || echo "")

if [ -z "$RECENT_CONTENT" ]; then
    echo "[$TODAY] 日志为空，跳过检查点"
    exit 0
fi

# 构建提示词
PROMPT="从以下OpenClaw工作日志中提取关键信息，格式化为Markdown：

1. 今日成就 (2-3条)
2. 学习收获 (1-2条)  
3. 重要决策 (1-2条)
4. 待改进项 (1-2条)

日志内容:
$RECENT_CONTENT

输出格式:
## 检查点 $(date '+%Y-%m-%d %H:%M')

### 成就
- ...

### 收获
- ...

### 决策
- ...

### 待改进
- ..."

# 调用LLM
ESCAPED_PROMPT=$(python3 -c "import json,sys; print(json.dumps('''$PROMPT'''))" 2>/dev/null || echo '""')

RESPONSE=$(curl -s "$OLLAMA_URL" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$MODEL\",\"prompt\":$ESCAPED_PROMPT,\"stream\":false}" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "[$TODAY] LLM调用失败，跳过检查点"
    exit 1
fi

SUMMARY=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("response",""))' 2>/dev/null || echo "")

if [ -n "$SUMMARY" ] && [ "$SUMMARY" != "null" ]; then
    # 追加到 MEMORY.md
    {
        echo ""
        echo "---"
        echo "## 检查点 $(date '+%Y-%m-%d %H:%M')"
        echo "$SUMMARY"
    } >> "$MEMORY_FILE"
    
    # 检查 MEMORY.md 大小，必要时归档
    SIZE=$(wc -c < "$MEMORY_FILE" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt 10000 ]; then
        # 归档到 archives
        ARCHIVE_FILE="$WORKSPACE/life/archives/weekly/checkpoint-$(date +%Y%m%d-%H%M%S).md"
        tail -c 5000 "$MEMORY_FILE" > "$ARCHIVE_FILE"
        # 保留精华部分
        head -c -5000 "$MEMORY_FILE" > "${MEMORY_FILE}.tmp" 2>/dev/null
        mv "${MEMORY_FILE}.tmp" "$MEMORY_FILE" 2>/dev/null || true
        echo "[$TODAY] MEMORY.md 已自动归档"
    fi
    
    echo "[$TODAY] ✅ 检查点完成"
else
    echo "[$TODAY] ❌ LLM返回为空"
fi
