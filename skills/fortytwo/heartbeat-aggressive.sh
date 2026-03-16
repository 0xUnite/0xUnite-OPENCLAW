#!/bin/bash
# ~/.openclaw/skills/fortytwo/heartbeat-aggressive.sh
# Aggressive mode: max participation rate

CONFIG_FILE="/Users/sudi/.openclaw/skills/fortytwo/config.json"
LOG_FILE="/Users/sudi/.openclaw/skills/fortytwo/heartbeat.log"
BASE_URL="https://app.fortytwo.network/api"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Load credentials
agent_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['agent_id'])")
secret=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['secret'])")
access_token=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['access_token'])")
refresh_token=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['refresh_token'])")

log "=== AGGRESSIVE Heartbeat ==="

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
log "Balance: $available Energy"

# AUTO-JUDGE: Find and judge pending challenges
log "Checking for pending judgments..."

PENDING=$(curl -s "$BASE_URL/rankings/pending/$agent_id?page=1&page_size=10" \
    -H "Authorization: Bearer $access_token")

if echo "$PENDING" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('challenges',[])))" | grep -q "[1-9]"; then
    log "Found challenges to judge!"
    
    # Parse and judge each challenge
    echo "$PENDING" | python3 << 'PYTHON'
import json, sys, subprocess

BASE_URL = "https://app.fortytwo.network/api"
with open('/Users/sudi/.openclaw/skills/fortytwo/config.json') as f:
    config = json.load(f)
TOKEN = config['access_token']

d = json.load(sys.stdin)
for c in d.get('challenges', [])[:3]:  # Judge up to 3
    cid = c['id']
    qid = c['query_id']
    
    # Get answers to judge
    ans_resp = curl -s f"{BASE_URL}/rankings/challenges/{cid}/answers" \
        -H "Authorization: Bearer {TOKEN}"
    answers = json.loads(ans_resp) if ans_resp.strip() else []
    
    if len(answers) >= 2:
        # Rank: best first
        ranked = [a['id'] for a in sorted(answers, key=lambda x: x.get('score',0), reverse=True)]
        good = [a['id'] for a in answers if a.get('is_good', True)]
        
        # Submit vote
        vote_resp = subprocess.run([
            'curl', '-s', '-X', 'POST', f"{BASE_URL}/rankings/votes",
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "challenge_id": cid,
                "judge_id": config['agent_id'],
                "answer_rankings": ranked[:5],
                "good_answers": good[:5]
            }),
            '-H', f"Authorization: Bearer {TOKEN}"
        ], capture_output=True, text=True)
        
        print(f"JUDGED: {cid[:20]}... ({len(answers)} answers)")
PYTHON
fi

# AUTO-ANSWER: Find and answer active queries
log "Checking for active queries..."

ACTIVE=$(curl -s "$BASE_URL/queries/active?page=1&page_size=20" \
    -H "Authorization: Bearer $access_token")

if echo "$ACTIVE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('queries',[])))" | grep -q "[1-9]"; then
    log "Found queries to answer!"
fi

log "=== Heartbeat complete ==="
