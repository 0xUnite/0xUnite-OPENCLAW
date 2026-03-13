#!/bin/bash
# 语义搜索记忆文件

QUERY="$1"
MEMORY_DIR="/Users/sudi/.openclaw/workspace/memory"

if [ -z "$QUERY" ]; then
    echo "用法: semantic-search.sh \"查询内容\""
    exit 1
fi

echo "搜索: $QUERY"
echo "---"

# 搜索memory目录
for file in "$MEMORY_DIR"/*.md; do
    if [ -f "$file" ] && [ "$(basename "$file")" != "lessons-learned.md" ]; then
        matches=$(grep -i "$QUERY" "$file" 2>/dev/null | head -3)
        if [ -n "$matches" ]; then
            echo "📄 $(basename "$file"):"
            echo "$matches"
            echo ""
        fi
    fi
done
