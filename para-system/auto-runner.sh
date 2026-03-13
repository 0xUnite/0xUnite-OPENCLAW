#!/bin/bash
# ~/.openclaw/workspace/para-system/auto-runner.sh
# 自动化任务调度器

WORKSPACE="$HOME/.openclaw/workspace"
LOG_FILE="$WORKSPACE/para-system/auto-runner.log"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查是否需要运行
check_needed() {
    local last_run=$1
    local interval=$2
    
    if [ -z "$last_run" ]; then
        return 0
    fi
    
    last_ts=$(date -d "$last_run" +%s 2>/dev/null || echo 0)
    now_ts=$(date +%s)
    interval_ts=$2
    
    if [ $((now_ts - last_ts)) -ge $interval_ts ]; then
        return 0
    fi
    return 1
}

# 读取上次运行时间
read_last_run() {
    local task=$1
    grep "$task:" "$WORKSPACE/para-system/.last-runs" 2>/dev/null | cut -d: -f2
}

# 记录运行时间
record_run() {
    local task=$1
    local now=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ -f "$WORKSPACE/para-system/.last-runs" ]; then
        grep -v "^$task:" "$WORKSPACE/para-system/.last-runs" > "$WORKSPACE/para-system/.last-runs.tmp" 2>/dev/null
        mv "$WORKSPACE/para-system/.last-runs.tmp" "$WORKSPACE/para-system/.last-runs"
    fi
    
    echo "$task:$now" >> "$WORKSPACE/para-system/.last-runs"
}

log "=== 自动化任务调度开始 ==="

# 1. 检查点（每6小时）
last_checkpoint=$(read_last_run "checkpoint")
now_ts=$(date +%s)
last_ts=$(date -d "$last_checkpoint" +%s 2>/dev/null || echo 0)
interval=21600  # 6小时

if [ -z "$last_checkpoint" ] || [ $((now_ts - last_ts)) -ge $interval ]; then
    log "运行检查点..."
    bash "$WORKSPACE/para-system/checkpoint-memory-llm.sh" >> "$LOG_FILE" 2>&1
    record_run "checkpoint"
    log "检查点完成"
fi

# 2. 动机每日检查
last_motivation=$(read_last_run "motivation")
last_ms_ts=$(date -d "$last_motivation" +%s 2>/dev/null || echo 0)
motivation_interval=86400  # 24小时

if [ -z "$last_motivation" ] || [ $((now_ts - last_ms_ts)) -ge $motivation_interval ]; then
    log "运行动机检查..."
    python3 "$WORKSPACE/life/projects/motivation/motivation_tracker.py" daily >> "$LOG_FILE" 2>&1
    record_run "motivation"
    log "动机检查完成"
fi

# 3. 周模式提取（每周日）
today_weekday=$(date +%u)  # 1-7, 7是周日
last_pattern=$(read_last_run "pattern")

if [ "$today_weekday" = "7" ]; then
    last_pattern_date=$(date -d "$last_pattern" +%u 2>/dev/null || echo 0)
    if [ "$last_pattern_date" != "7" ]; then
        log "运行周模式提取..."
        python3 "$WORKSPACE/life/projects/pattern-extraction/weekly_pattern_extractor.py" 7 >> "$LOG_FILE" 2>&1
        record_run "pattern"
        log "模式提取完成"
    fi
fi

# 4. 夜间优化（每周日）
if [ "$today_weekday" = "7" ]; then
    last_optimizer=$(read_last_run "optimizer")
    last_opt_date=$(date -d "$last_optimizer" +%u 2>/dev/null || echo 0)
    if [ "$last_opt_date" != "7" ]; then
        log "运行夜间优化..."
        python3 "$WORKSPACE/life/projects/nighttime-optimizer/nighttime_optimizer.py" >> "$LOG_FILE" 2>&1
        record_run "optimizer"
        log "优化完成"
    fi
fi

log "=== 自动化任务调度完成 ==="
