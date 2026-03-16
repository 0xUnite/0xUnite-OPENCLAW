#!/bin/bash
# ~/.openclaw/skills/fortytwo/heartbeat.sh
# Fortytwo Swarm Auto-Participation with MiniMax 2.5

CONFIG_FILE="/Users/sudi/.openclaw/skills/fortytwo/config.json"
LOG_FILE="/Users/sudi/.openclaw/skills/fortytwo/heartbeat.log"
BASE_URL="https://app.fortytwo.network/api"

# MiniMax API Config
MINIMAX_API_KEY="sk-cp-I6J-KeKQnl-M_pzNQaEgKqSJptVFg4CQ45k5QQpqRZ-MQQodsiHI61m6HkFlRhc8K2R9HnClErdMaIYIufB6Fz1JjgilxPieRGOsMaUOiHLSHRllzt0BaFE"
MINIMAX_MODEL="MiniMax-M2.5"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

call_minimax() {
    local prompt="$1"
    local response
    
    response=$(curl -s -X POST "https://api.minimaxi.com/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $MINIMAX_API_KEY" \
        -d "{
            \"model\": \"$MINIMAX_MODEL\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.3
        }")
    
    echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])" 2>/dev/null
}

log "=== Heartbeat started ==="

# Load config fresh each time
agent_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['agent_id'])")
secret=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['secret'])")
refresh_token=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['refresh_token'])")

# Try to get access token
if [ -n "$refresh_token" ]; then
    RESP=$(curl -s -X POST "$BASE_URL/auth/refresh" \
        -H "Content-Type: application/json" \
        -d "{\"refresh_token\": \"$refresh_token\"}")
    
    if echo "$RESP" | grep -q "access_token"; then
        access_token=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
        new_refresh=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['refresh_token'])")
        
        python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    c = json.load(f)
c['access_token'] = '$access_token'
c['refresh_token'] = '$new_refresh'
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2)
"
        log "Token refreshed"
    else
        # Refresh failed, re-login
        LOGIN_RESP=$(curl -s -X POST "$BASE_URL/auth/login" \
            -H "Content-Type: application/json" \
            -d "{\"agent_id\": \"$agent_id\", \"secret\": \"$secret\"}")
        
        if echo "$LOGIN_RESP" | grep -q "access_token"; then
            access_token=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tokens']['access_token'])")
            new_refresh=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tokens']['refresh_token'])")
            
            python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    c = json.load(f)
c['access_token'] = '$access_token'
c['refresh_token'] = '$new_refresh'
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2)
"
            log "Logged in fresh"
        fi
    fi
elif [ -n "$secret" ]; then
    # No refresh token, login directly
    LOGIN_RESP=$(curl -s -X POST "$BASE_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"agent_id\": \"$agent_id\", \"secret\": \"$secret\"}")
    
    if echo "$LOGIN_RESP" | grep -q "access_token"; then
        access_token=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tokens']['access_token'])")
        new_refresh=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tokens']['refresh_token'])")
        
        python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    c = json.load(f)
c['access_token'] = '$access_token'
c['refresh_token'] = '$new_refresh'
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2)
"
        log "Logged in"
    fi
fi

# Check balance
BALANCE=$(curl -s "$BASE_URL/economy/balance/$agent_id" \
    -H "Authorization: Bearer $access_token")

available=$(echo "$BALANCE" | python3 -c "import sys,json; print(json.load(sys.stdin)['available'])")
log "⚡ Balance: $available Energy"

# ===== ANSWER QUERIES =====
if (( $(echo "$available >= 5" | bc -l) )); then
    QUERIES=$(curl -s "$BASE_URL/queries/active?page=1&page_size=10" \
        -H "Authorization: Bearer $access_token")
    
    query_count=$(echo "$QUERIES" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('queries',[])))")
    
    if [ "$query_count" -gt 0 ]; then
        log "Found $query_count active queries"
        
        # Filter queries by stake AND status (only join if status is 'active' and stake <= available)
        query_id=$(echo "$QUERIES" | python3 -c "
import json,sys
d=json.load(sys.stdin)
available = float('$available')
print(f'DEBUG: available={available}', file=sys.stderr)
for q in d.get('queries',[]):
    stake = float(q.get('calculated_submit_stake', '999999'))
    status = q.get('status', '')
    print(f'DEBUG: query {q.get(\"id\", \"?\")[:8]} stake={stake} status={status}', file=sys.stderr)
    if stake <= available and status == 'active':
        print(q['id'])
        break
" 2>> "$LOG_FILE")
        
        if [ -n "$query_id" ]; then
            log "Joining query: $query_id"
            
            JOIN_RESP=$(curl -s -X POST "$BASE_URL/queries/$query_id/join" \
                -H "Authorization: Bearer $access_token")
            
            if echo "$JOIN_RESP" | grep -q "success"; then
                QUERY_DETAIL=$(curl -s "$BASE_URL/queries/$query_id" \
                    -H "Authorization: Bearer $access_token")
                
                content=$(echo "$QUERY_DETAIL" | python3 -c "
import json,sys,base64
d=json.load(sys.stdin)
c = d.get('encrypted_content','')
if c:
    print(base64.b64decode(c).decode('utf-8'))
else:
    print('No content')
" 2>/dev/null)
                
                if [ -n "$content" ] && [ "$content" != "No content" ]; then
                    log "Evaluating: ${content:0:50}..."
                    
                    # Quality check: Do we understand this?
                    confidence=$(call_minimax "On a scale of 0-100, how confident are you answering this question accurately? Consider: Do you have sufficient knowledge? Is the question clear? Can you verify your answer? Would most people agree with your answer?

Question: $content

Respond with ONLY a number (0-100).")
                    
                    # Extract numeric confidence
                    confidence_num=$(echo "$confidence" | grep -oE '[0-9]+' | head -1)
                    
                    if [ -z "$confidence_num" ] || [ "$confidence_num" -lt 70 ]; then
                        log "⏭️ Skipped - low confidence ($confidence_num)"
                    else
                        log "✅ Confident ($confidence_num%) - answering..."
                        
                        # Get detailed answer with reasoning - improved prompt from Veenoway guide
                        answer=$(call_minimax "You are a senior researcher. Your answer will be judged by other AI agents.

Requirements:
- Lead with the most important insight first
- Include specific technical details and references
- Compare different approaches objectively
- Provide verifiable evidence

Format your response as:
FINAL_ANSWER: [your answer here]

Question: $content")
                    
                    # Double check answer quality - be more strict
                    if echo "$answer" | grep -qi "UNABLE_TO_ANSWER\|NOT_SURE\|UNCERTAIN\|I_CANT\|I_DONT_KNOW"; then
                        log "⏭️ Skipped - AI uncertain"
                    elif [ -n "$answer" ] && [ ${#answer} -gt 30 ]; then
                        # Self-critique: Verify answer quality
                        critique=$(call_minimax "Is this answer correct and verifiable? Answer YES or NO. If there's any doubt, say NO.

Original Question: $content
Proposed Answer: $answer")
                        
                        if echo "$critique" | grep -qi "^NO"; then
                            log "⏭️ Skipped - failed self-critique"
                        else
                            log "✅ Self-critique passed"
                            encrypted_answer=$(echo -n "$answer" | base64 | tr -d '\n')
                            
                            SUBMIT_RESP=$(curl -s -X POST "$BASE_URL/queries/$query_id/answers" \
                                -H "Authorization: Bearer $access_token" \
                                -H "Content-Type: application/json" \
                                -d "{\"encrypted_content\": \"$encrypted_answer\"}")
                            
                            if echo "$SUBMIT_RESP" | grep -q "id"; then
                                log "✅ Answer submitted!"
                            else
                                log "Submit failed"
                            fi
                        fi
                    else
                        log "⏭️ Skipped - answer too short"
                    fi
                fi
            else
                log "No content available"
            fi
        else
            log "Join: $JOIN_RESP"
        fi
    fi
else
    log "No active queries"
fi
else
    log "Balance too low to answer (need >= 5)"
fi
CHALLENGES=$(curl -s "$BASE_URL/rankings/pending/$agent_id?page=1&page_size=5" \
    -H "Authorization: Bearer $access_token")

challenge_count=$(echo "$CHALLENGES" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('challenges',[])))")

if [ "$challenge_count" -gt 0 ]; then
    log "Found $challenge_count pending rankings - attempting to participate..."
    
    # Try to participate in each ranking
    for challenge_id in $(echo "$CHALLENGES" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(c.get('id')) for c in d.get('challenges',[])]"); do
        query_id=$(echo "$CHALLENGES" | python3 -c "import sys,json; d=json.load(sys.stdin)
for c in d.get('challenges',[]):
    if c.get('id') == '$challenge_id':
        print(c.get('query_id'))
        break")
        
        if [ -n "$query_id" ]; then
            # Try to join the ranking challenge
            JOIN_RESP=$(curl -s -X POST "$BASE_URL/rankings/$challenge_id/join" \
                -H "Authorization: Bearer $access_token" \
                -H "Content-Type: application/json" \
                -d '{}')
            
            if echo "$JOIN_RESP" | grep -q "success"; then
                log "✅ Joined ranking challenge: $challenge_id"
            else
                log "⚠️ Ranking join failed: $(echo $JOIN_RESP | head -100)"
            fi
        fi
    done
fi

log "=== Heartbeat complete ==="
