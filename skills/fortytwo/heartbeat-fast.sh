#!/bin/bash
# ~/.openclaw/skills/fortytwo/heartbeat-fast.sh
# Fast mode: run every minute for max Energy

CONFIG_FILE="/Users/sudi/.openclaw/skills/fortytwo/config.json"
LOG_FILE="/Users/sudi/.openclaw/skills/fortytwo/heartbeat.log"
BASE_URL="https://app.fortytwo.network/api"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Load config
agent_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['agent_id'])")
access_token=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['access_token'])")
refresh_token=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['refresh_token'])")

# Refresh token
RESP=$(curl -s -X POST "$BASE_URL/auth/refresh" \
    -H "Content-Type: application/json" \
    -d "{\"refresh_token\": \"$refresh_token\"}")

if echo "$RESP" | grep -q "access_token"; then
    access_token=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
    refresh_token=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['refresh_token'])")
    python3 << EOF
import json
with open('$CONFIG_FILE', 'r') as f:
    c = json.load(f)
c['access_token'] = '$access_token'
c['refresh_token'] = '$refresh_token'
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2)
EOF
    log "Token refreshed"
fi

# Check balance
BALANCE=$(curl -s "$BASE_URL/economy/balance/$agent_id" \
    -H "Authorization: Bearer $access_token")
available=$(echo "$BALANCE" | python3 -c "import json,sys; print(json.load(sys.stdin)['available'])")

# Check pending judgments
PENDING=$(curl -s "$BASE_URL/rankings/pending/$agent_id?page=1&page_size=10" \
    -H "Authorization: Bearer $access_token")
pending_count=$(echo "$PENDING" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('challenges',[])))")

# Check active queries
ACTIVE=$(curl -s "$BASE_URL/queries/active?page=1&page_size=20" \
    -H "Authorization: Bearer $access_token")
active_count=$(echo "$ACTIVE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('queries',[])))")

log "⚡ Balance: $available | Pending: $pending_count | Active: $active_count"

if [ "$pending_count" -gt 0 ]; then
    log "Found $pending_count judgments to make"
fi
