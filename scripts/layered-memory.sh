#!/bin/bash
# OpenViking风格的层级记忆系统
# L0: 当前会话 - 完整上下文
# L1: 近期记忆 - 压缩后的关键信息
# L2: 长期记忆 - 精选的核心记忆

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
L0_DIR="$MEMORY_DIR/layer0_current"   # 当前会话
L1_DIR="$MEMORY_DIR/layer1_recent"    # 近期(最近7天)
L2_DIR="$MEMORY_DIR/layer2_longterm"   # 长期(精选)

mkdir -p "$L0_DIR" "$L1_DIR" "$L2_DIR"

echo "📚 层级记忆系统初始化"
echo "L0: $L0_DIR (当前会话)"
echo "L1: $L1_DIR (近期7天)"  
echo "L2: $L2_DIR (长期精选)"

# ========== L0: 当前会话管理 ==========
update_l0() {
    local session_context="$1"
    echo "$session_context" > "$L0_DIR/current_session.md"
    echo "✅ L0更新: 当前会话"
}

# ========== L1: 近期记忆压缩 ==========
compress_l1() {
    echo "🔄 压缩L1近期记忆..."
    
    # 合并最近7天的日记
    local recent_files=$(find "$MEMORY_DIR" -name "2026-*.md" -mtime -7 | head -7)
    
    if [ -z "$recent_files" ]; then
        echo "无最近文件"
        return
    fi
    
    # 提取关键信息: 决策、任务、要点
    cat $recent_files | grep -E "^##|^- \[|^\*\*" | head -50 > "$L1_DIR/compressed_week.md"
    
    # 更新索引
    echo "# L1 近期记忆索引" > "$L1_DIR/index.md"
    echo "最后更新: $(date)" >> "$L1_DIR/index.md"
    echo "" >> "$L1_DIR/index.md"
    echo "## 最近7天关键内容" >> "$L1_DIR/index.md"
    ls -t "$MEMORY_DIR"/2026-*.md | head -7 | while read f; do
        echo "- $(basename $f)" >> "$L1_DIR/index.md"
    done
    
    echo "✅ L1压缩完成"
}

# ========== L2: 长期记忆提取 ==========
extract_l2() {
    echo "🎯 提取L2长期记忆..."
    
    # 从MEMORY.md提取核心要点
    if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
        grep -E "^##|^- |^###" "$MEMORY_DIR/MEMORY.md" | head -30 > "$L2_DIR/core_memories.md"
    fi
    
    # 从重要日记中提取
    for f in "$MEMORY_DIR"/2026-02-{08,10,12,14,16}.md; do
        if [ -f "$f" ]; then
            basename "$f" >> "$L2_DIR/archived_days.md"
        fi
    done
    
    echo "✅ L2长期记忆已更新"
}

# ========== 按需加载 ==========
load_context() {
    local layer="$1"  # L0, L1, or L2
    
    case $layer in
        L0)
            cat "$L0_DIR/current_session.md" 2>/dev/null
            ;;
        L1)
            cat "$L1_DIR/compressed_week.md" 2>/dev/null
            ;;
        L2)
            cat "$L2_DIR/core_memories.md" 2>/dev/null
            ;;
        all)
            echo "=== L2 长期记忆 ==="
            cat "$L2_DIR/core_memories.md" 2>/dev/null
            echo ""
            echo "=== L1 近期记忆 ==="
            cat "$L1_DIR/compressed_week.md" 2>/dev/null
            echo ""
            echo "=== L0 当前会话 ==="
            cat "$L0_DIR/current_session.md" 2>/dev/null
            ;;
    esac
}

# ========== 主命令 ==========
case "$1" in
    l0)
        update_l0 "$2"
        ;;
    l1)
        compress_l1
        ;;
    l2)
        extract_l2
        ;;
    load)
        load_context "${2:-all}"
        ;;
    sync)
        compress_l1
        extract_l2
        echo "✅ 层级记忆同步完成"
        ;;
    *)
        echo "用法: $0 {l0 <内容>|l1|l2|load <L0|L1|L2|all>|sync}"
        ;;
esac
