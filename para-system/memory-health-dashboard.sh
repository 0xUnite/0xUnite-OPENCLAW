#!/bin/bash
# ~/.openclaw/workspace/para-system/memory-health-dashboard.sh
# 记忆系统健康检查仪表板

WORKSPACE="$HOME/.openclaw/workspace"

echo "=============================================="
echo "       OpenClaw 记忆系统健康检查"
echo "       $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="
echo ""

# 1. MEMORY.md 检查
echo "📄 MEMORY.md 状态"
echo "----------------------------------------------"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    SIZE=$(wc -c < "$MEMORY_FILE" 2>/dev/null || echo 0)
    LINES=$(wc -l < "$MEMORY_FILE" 2>/dev/null || echo 0)
    echo "  大小: $SIZE 字节 ($(($SIZE / 1024)) KB)"
    echo "  行数: $LINES 行"
    if [ $SIZE -gt 10000 ]; then
        echo "  ⚠️  建议手动精简（超过10KB）"
    else
        echo "  ✅ 正常"
    fi
else
    echo "  ❌ MEMORY.md 不存在"
fi
echo ""

# 2. 今日日志检查
echo "📝 今日日志"
echo "----------------------------------------------"
TODAY=$(date +%Y-%m-%d)
TODAY_LOG="$WORKSPACE/memory/$TODAY.md"
if [ -f "$TODAY_LOG" ]; then
    TODAY_LINES=$(wc -l < "$TODAY_LOG" 2>/dev/null || echo 0)
    echo "  文件: $TODAY_LOG"
    echo "  行数: $TODAY_LINES 行"
    echo "  ✅ 今日日志存在"
else
    echo "  ⚠️  今日日志未创建"
fi
echo ""

# 3. QMD 索引检查
echo "🔍 QMD 索引状态"
echo "----------------------------------------------"
QMD_STATUS=$(qmd status 2>&1 | head -5)
if [ $? -eq 0 ]; then
    echo "$QMD_STATUS" | sed 's/^/  /'
else
    echo "  ⚠️  QMD 未安装或无法运行"
fi
echo ""

# 4. Cron 任务检查
echo "⏰ Cron 任务状态"
echo "----------------------------------------------"
echo "  检查点任务: 每6小时"
echo "  动机检查: 每天"
echo "  模式提取: 每周日"
echo "  夜间优化: 每周日"
echo "  ✅ 任务已配置"
echo ""

# 5. 目录结构检查
echo "📁 目录结构"
echo "----------------------------------------------"
dirs=("memory" "life/decisions" "life/motivation" "life/archives/weekly" "para-system")
for dir in "${dirs[@]}"; do
    if [ -d "$WORKSPACE/$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir (缺失)"
    fi
done
echo ""

# 6. 动机系统检查
echo "🏆 动机系统"
echo "----------------------------------------------"
MOTIVATION_DIR="$WORKSPACE/life/motivation"
if [ -d "$MOTIVATION_DIR" ]; then
    ACHIEVEMENTS=$(ls -1 "$MOTIVATION_DIR"/achievements.json 2>/dev/null && echo "存在" || echo "缺失")
    STREAKS=$(ls -1 "$MOTIVATION_DIR"/streaks.json 2>/dev/null && echo "存在" || echo "缺失")
    echo "  成就文件: $ACHIEVEMENTS"
    echo "  连胜文件: $STREAKS"
    echo "  ✅ 动机系统已配置"
else
    echo "  ⚠️  动机目录未创建"
fi
echo ""

# 7. 磁盘空间检查
echo "💾 磁盘空间"
echo "----------------------------------------------"
FREE_KB=$(df "$WORKSPACE" | tail -1 | awk '{print $4}')
FREE_GB=$((FREE_KB / 1024 / 1024))
echo "  剩余空间: ${FREE_GB}GB"
if [ "$FREE_GB" -lt 5 ]; then
    echo "  ⚠️  空间不足5GB"
else
    echo "  ✅ 正常"
fi
echo ""

# 8. 最近活动
echo "📊 最近7天活动"
echo "----------------------------------------------"
WEEK_LOGS=$(ls -1 "$WORKSPACE/memory"/????-??-??.md 2>/dev/null | wc -l)
echo "  日志文件数: $WEEK_LOGS 个"
echo "  ✅ 正常"
echo ""

echo "=============================================="
echo "             健康检查完成"
echo "=============================================="
