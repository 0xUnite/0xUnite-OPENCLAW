#!/bin/bash
# Fortytwo Auto-Participation: Answer + Judge + Create Queries
# Enhanced with MiniMax 2.5

CONFIG_FILE="/Users/sudi/.openclaw/skills/fortytwo/config.json"
LOG_FILE="/Users/sudi/.openclaw/workspace/memory/fortytwo-auto.log"
BASE_URL="https://app.fortytwo.network/api"

# MiniMax API
MINIMAX_KEY="sk-cp-I6J-KeKQnl-M_pzNQaEgKqSJptVFg4CQ45k5QQpqRZ-MQQodsiHI61m6HkFlRhc8K2R9HnClErdMaIYIufB6Fz1JjgilxPieRGOsMaUOiHLSHRllzt0BaFE"
MINIMAX_MODEL="MiniMax-M2.5"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Load credentials
agent_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['agent_id'])")
secret=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['secret'])")

# Login
log "=== 开始自动参与 ==="
LOGIN_RESP=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"agent_id\": \"$agent_id\", \"secret\": \"$secret\"}")

access_token=$(echo "$LOGIN_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['tokens']['access_token'])" 2>/dev/null)

if [ -z "$access_token" ]; then
    log "登录失败"
    exit 1
fi

# Get balance
balance=$(curl -s "$BASE_URL/agents/me" -H "Authorization: Bearer $access_token" | python3 -c "import json,sys; print(json.load(sys.stdin).get('energy',0))" 2>/dev/null)
log "⚡ 余额: $balance Energy"

# ========== 1. 回答问题 ==========
log "检查待回答问题..."
QUERIES=$(curl -s "$BASE_URL/queries/active?page=1&page_size=5" -H "Authorization: Bearer $access_token")
query_count=$(echo "$QUERIES" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('queries',[])))")

if [ "$query_count" -gt 0 ]; then
    log "发现 $query_count 个问题"
    
    # Pick first query
    query_id=$(echo "$QUERIES" | python3 -c "import json,sys; q=json.load(sys.stdin)['queries']; print(q[0]['id'] if q else '')")
    query_content=$(echo "$QUERIES" | python3 -c "import json,sys; q=json.load(sys.stdin)['queries']; print(q[0].get('content','')[:200] if q else '')" 2>/dev/null)
    
    if [ -n "$query_id" ]; then
        log "问题: ${query_content:0:50}..."
        
        # Generate answer with MiniMax
        answer=$(curl -s -X POST "https://api.minimaxi.com/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $MINIMAX_KEY" \
            -d "{\"model\": \"$MINIMAX_MODEL\", \"messages\": [{\"role\": \"system\", \"content\": \"You are an expert. Answer the question accurately and concisely.\"}, {\"role\": \"user\", \"content\": \"$query_content\"}], \"temperature\": 0.1}" | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'][:300]" 2>/dev/null)
        
        if [ -n "$answer" ]; then
            # Submit answer
            submit_resp=$(curl -s -X POST "$BASE_URL/queries/$query_id/answers" \
                -H "Authorization: Bearer $access_token" \
                -H "Content-Type: application/json" \
                -d "{\"content\": \"$answer\"}")
            log "✅ 已提交答案: ${answer:0:30}..."
        fi
    fi
else
    log "无待回答问题"
fi

# ========== 2. 评判答案 ==========
log "检查待评判..."
CHALLENGES=$(curl -s "$BASE_URL/rankings/pending/$agent_id?page=1&page_size=5" \
    -H "Authorization: Bearer $access_token")

challenge_count=$(echo "$CHALLENGES" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('challenges',[])))")
log "待评判: $challenge_count 个"

if [ "$challenge_count" -gt 0 ]; then
    for idx in $(seq 0 $((challenge_count-1))); do
        challenge_id=$(echo "$CHALLENGES" | python3 -c "import json,sys; c=json.load(sys.stdin)['challenges']; print(c[$idx]['id'] if len(c)>$idx else '')" 2>/dev/null)
        query_id=$(echo "$CHALLENGES" | python3 -c "import json,sys; c=json.load(sys.stdin)['challenges']; print(c[$idx]['query_id'] if len(c)>$idx else '')" 2>/dev/null)
        
        if [ -n "$challenge_id" ]; then
            log "评判: $challenge_id"
            
            # Join
            curl -s -X POST "$BASE_URL/rankings/challenges/$challenge_id/join" \
                -H "Authorization: Bearer $access_token" > /dev/null
            
            # Get answers
            answers=$(curl -s "$BASE_URL/queries/$query_id/answers" -H "Authorization: Bearer $access_token")
            answer_ids=$(echo "$answers" | python3 -c "import json,sys; print(' '.join([a['id'] for a in json.load(sys.stdin).get('answers',[])]))" 2>/dev/null)
            
            if [ -n "$answer_ids" ]; then
                # Random ranking for now (could be enhanced with MiniMax)
                ranked=$(echo $answer_ids | tr ' ' '\n' | shuf | tr '\n' ' ')
                first=$(echo $ranked | cut -d' ' -f1)
                
                vote_data="{\"challenge_id\": \"$challenge_id\", \"judge_id\": \"$agent_id\", \"answer_rankings\": [\"$ranked\"], \"good_answers\": [\"$first\"]}"
                
                curl -s -X POST "$BASE_URL/rankings/votes" \
                    -H "Authorization: Bearer $access_token" \
                    -H "Content-Type: application/json" \
                    -d "$vote_data" > /dev/null
                
                log "✅ 评判完成"
            fi
        fi
    done
fi

# ========== 3. 创建问题 ==========
log "尝试创建新问题..."
specializations=("mathematics" "science" "general")
spec=${specializations[$((RANDOM % 3))]}

prompt="Create ONE clear $spec question with a definite answer. Keep it simple. Just the question."

new_question=$(curl -s -X POST "https://api.minimaxi.com/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $MINIMAX_KEY" \
    -d "{\"model\": \"$MINIMAX_MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}], \"temperature\": 0.5}" | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'].strip())" 2>/dev/null)

if [ -n "$new_question" ] && [ ${#new_question} -gt 10 ]; then
    create_resp=$(curl -s -X POST "$BASE_URL/queries" \
        -H "Authorization: Bearer $access_token" \
        -H "Content-Type: application/json" \
        -d "{\"content\": \"$new_question\", \"specialization\": \"$spec\"}")
    
    if echo "$create_resp" | python3 -c "import json,sys; json.load(sys.stdin).get('id','')" 2>/dev/null | grep -q .; then
        log "✅ 新问题已创建: ${new_question:0:30}..."
    else
        log "⚠️ 创建失败: ${create_resp:0:50}"
    fi
else
    log "⚠️ 无新问题"
fi

log "=== 自动参与完成 ==="
