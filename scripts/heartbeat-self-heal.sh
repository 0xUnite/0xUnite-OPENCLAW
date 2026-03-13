#!/bin/bash
# 智能心跳检测 + 自愈系统（安全版）
# 每 10 分钟运行一次

set -u

LOG_FILE="$HOME/.openclaw/workspace/memory/heartbeat.log"
LAST_ACTIVE_FILE="$HOME/.openclaw/workspace/memory/last-active.txt"
NOTIFICATION_FILE="$HOME/.openclaw/workspace/memory/pending-notification.txt"
STATE_FILE="$HOME/.openclaw/workspace/memory/heartbeat-gateway-fail.state"
LOCK_DIR="/tmp/openclaw-heartbeat-self-heal.lock"
GATEWAY_HEALTH_URL="http://127.0.0.1:18789/health"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    local now
    now="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$now] $1" >> "$LOG_FILE"
}

# 防止并发执行导致重复重启
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    log "⏭️ 检测已在运行，跳过本次任务"
    exit 0
fi
trap 'rmdir "$LOCK_DIR" >/dev/null 2>&1 || true' EXIT

check_gateway_once() {
    curl -fsS --max-time 4 "$GATEWAY_HEALTH_URL" >/dev/null 2>&1
}

# 多次探测，避免瞬时抖动误判
check_gateway() {
    local i
    for i in 1 2 3; do
        if check_gateway_once; then
            return 0
        fi
        sleep 2
    done
    return 1
}

wait_gateway_up() {
    local n=0
    while [ "$n" -lt 20 ]; do
        if check_gateway_once; then
            return 0
        fi
        n=$((n + 1))
        sleep 1
    done
    return 1
}

read_fail_count() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

write_fail_count() {
    echo "$1" >"$STATE_FILE"
}

reset_fail_count() {
    write_fail_count 0
}

attempt_heal() {
    local fail_count="${1:-0}"
    log "⚠️ 检测到 Gateway 无响应（连续 ${fail_count} 次），开始软自愈..."

    if ! command -v openclaw >/dev/null 2>&1; then
        log "❌ openclaw 命令不存在，无法自愈"
        return 1
    fi

    # 仅做温和恢复，避免与 minute 级 watchdog 互相打架。
    log "  尝试启动网关服务（openclaw gateway start）..."
    openclaw gateway start >>"$LOG_FILE" 2>&1 || true
    if wait_gateway_up; then
        log "  🎉 启动成功，Gateway 已恢复"
        return 0
    fi

    log "  ❌ 软自愈失败，交给 gateway-self-heal 持续处理"
    return 1
}

log "=== 开始健康检查 ==="
if check_gateway; then
    log "✅ Gateway: 正常"
    date '+%Y-%m-%d %H:%M:%S' >"$LAST_ACTIVE_FILE"
    reset_fail_count
else
    fail_count="$(read_fail_count)"
    case "$fail_count" in
        ''|*[!0-9]*) fail_count=0 ;;
    esac
    fail_count=$((fail_count + 1))
    write_fail_count "$fail_count"

    log "❌ Gateway: 无响应（连续 ${fail_count} 次）"
    if [ "$fail_count" -lt 2 ]; then
        log "⏳ 首次失败，等待下一轮确认，避免误触发"
    else
        if attempt_heal "$fail_count"; then
            reset_fail_count
            echo "Gateway 在 $(date '+%Y-%m-%d %H:%M:%S') 检测到无响应（连续${fail_count}次），软自愈状态: 成功" >>"$NOTIFICATION_FILE"
        else
            echo "Gateway 在 $(date '+%Y-%m-%d %H:%M:%S') 检测到无响应（连续${fail_count}次），软自愈状态: 失败" >>"$NOTIFICATION_FILE"
        fi
    fi
fi
log "=== 检查完成 ==="
echo "" >>"$LOG_FILE"
