#!/bin/bash
# 自我健康检查脚本
# 每 5 分钟运行一次

echo "=== $(date) 健康检查 ==="

# 1. 检查 Gateway 是否响应
if curl -s --max-time 5 "http://127.0.0.1:18789/health" > /dev/null 2>&1; then
    echo "✅ Gateway: OK"
else
    echo "❌ Gateway: 无响应，尝试重启..."
    # 这里可以添加自动重启逻辑
fi

# 2. 检查最后活跃时间
LAST_ACTIVE=$(cat ~/.openclaw/workspace/memory/last-active.txt 2>/dev/null || echo "未知")
echo "📅 最后活跃: $LAST_ACTIVE"

# 3. 更新活跃时间
date +%Y-%m-%d\ %H:%M:%S > ~/.openclaw/workspace/memory/last-active.txt

echo "✅ 检查完成"
