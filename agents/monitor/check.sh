#!/bin/bash
# 状态汇报脚本 - 每小时/每2小时汇报

TELEGRAM_BOT="8560545483:AAEQ1D4qQbn7Kf4Ags7POXFPrURHxkGij80"
TELEGRAM_CHAT="-1003727098894"
LOG_FILE="/Users/sudi/.openclaw/workspace/memory/monitor.log"

# ==================== 1. Nexus节点 ====================
NEXUS_COUNT=$(pgrep -aif "nexus" 2>/dev/null | wc -l | tr -d " ")
NEXUS_PID=$(pgrep -aif "nexus" 2>/dev/null | head -1 | awk '{print $1}')
if [ -n "$NEXUS_PID" ]; then
    NEXUS_UPTIME=$(ps -o etime= -p "$NEXUS_PID" 2>/dev/null | tr -d " ")
    NEXUS_STATUS="✅ ${NEXUS_COUNT}节点(运行${NEXUS_UPTIME})"
else
    NEXUS_STATUS="❌ 已停止"
fi

# ==================== 2. Fortytwo Agent ====================
FT_LOG="/Users/sudi/.openclaw/skills/fortytwo/heartbeat.log"
if [ -f "$FT_LOG" ]; then
    FT_LAST=$(tail -10 "$FT_LOG" 2>/dev/null | grep -oE "[0-9]{2}:[0-9]{2}" | tail -1)
    FT_ACTIVE=$(tail -20 "$FT_LOG" 2>/dev/null | grep -oE "Found [0-9]+ active" | tail -1 | grep -oE "[0-9]+")
    FT_STATUS="✅ 心跳${FT_LAST}|活跃${FT_ACTIVE}"
else
    FT_STATUS="⚠️ 无日志"
fi

# ==================== 3. Fortytwo 终端 ====================
if [ -f "$FT_LOG" ]; then
    FT_BALANCE=$(grep -oE "[0-9.]+ Energy" "$FT_LOG" 2>/dev/null | tail -1 | grep -oE "[0-9.]+" | cut -d'.' -f1-2)
    FT_TERM_STATUS="✅ 余额${FT_BALANCE%.*}"
else
    FT_TERM_STATUS="⚠️ 无日志"
fi

# ==================== 构建消息 ====================
MSG="📊 *系统状态* $(date '+%m/%d %H:%M')

| 项目 | 状态 |
| :--- | :--- |
| Nexus 节点 | ${NEXUS_STATUS} |
| Fortytwo Agent | ${FT_STATUS} |
| Fortytwo 终端 | ${FT_TERM_STATUS} |

━━━━━━━━━━━━━━━━━━━━"

echo "$MSG"
echo "[$(date '+%m-%d %H:%M')] 监控汇报已发送" >> "$LOG_FILE"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT}/sendMessage" \
    -d "chat_id=${TELEGRAM_CHAT}" \
    -d "text=${MSG}" \
    -d "parse_mode=Markdown"
