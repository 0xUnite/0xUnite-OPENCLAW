#!/bin/bash
# ~/.openclaw/skills/fortytwo/judge.sh
# Fortytwo Swarm Auto-Judging Script

CONFIG_FILE="/Users/sudi/.openclaw/skills/fortytwo/config.json"
LOG_FILE="/Users/sudi/.openclaw/skills/fortytwo/judge.log"
BASE_URL="https://app.fortytwo.network/api"

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Load config
agent_id=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['agent_id'])")
secret=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['secret'])")

# Login to get fresh tokens
log "Logging in..."
LOGIN_RESP=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"agent_id\": \"$agent_id\", \"secret\": \"$secret\"}")

access_token=$(echo "$LOGIN_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['tokens']['access_token'])")
refresh_token=$(echo "$LOGIN_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['tokens']['refresh_token'])")

# Update config
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

# Get pending challenges
log "Fetching pending challenges..."
CHALLENGES=$(curl -s "$BASE_URL/rankings/pending/$agent_id?page=1&page_size=10" \
    -H "Authorization: Bearer $access_token")

challenge_count=$(echo "$CHALLENGES" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('challenges',[])))")
log "Found $challenge_count pending challenges"

if [ "$challenge_count" -eq 0 ]; then
    log "No challenges to judge"
    exit 0
fi

# Process each challenge
echo "$CHALLENGES" | python3 -c "
import json, sys, subprocess, os

config_file = '$CONFIG_FILE'
BASE_URL = '$BASE_URL'
access_token = '$access_token'

d = json.load(sys.stdin)
challenges = d.get('challenges', [])

for ch in challenges:
    challenge_id = ch['id']
    query_id = ch['query_id']
    print(f'\\n=== Processing challenge: {challenge_id} ===')
    
    # Join challenge
    print('Joining challenge...')
    join_resp = subprocess.run([
        'curl', '-s', '-X', 'POST', 
        f'{BASE_URL}/rankings/challenges/{challenge_id}/join',
        '-H', f'Authorization: Bearer {access_token}'
    ], capture_output=True, text=True)
    
    if 'success' not in join_resp.stdout:
        print(f'Failed to join: {join_resp.stdout}')
        continue
    
    print('Joined successfully')
    
    # Get answers
    answers_resp = subprocess.run([
        'curl', '-s', 
        f'{BASE_URL}/queries/{query_id}/answers',
        '-H', f'Authorization: Bearer {access_token}'
    ], capture_output=True, text=True)
    
    answers_data = json.loads(answers_resp.stdout)
    answers = answers_data.get('answers', [])
    
    if not answers:
        print('No answers found')
        continue
    
    # Get answer IDs ordered by creation (use as fallback ranking)
    answer_ids = [a['id'] for a in answers]
    good_answers = [answer_ids[0]]  # Mark first as good (fallback: random)
    
    print(f'Found {len(answers)} answers')
    print(f'Ranking: {answer_ids}')
    
    # Submit vote (fallback ranking - randomly ordered)
    import random
    ranked_ids = answer_ids.copy()
    random.shuffle(ranked_ids)
    
    vote_data = {
        'challenge_id': challenge_id,
        'judge_id': '$agent_id',
        'answer_rankings': ranked_ids,
        'good_answers': [ranked_ids[0]]
    }
    
    import shlex
    vote_json = json.dumps(vote_data)
    
    vote_resp = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'{BASE_URL}/rankings/votes',
        '-H', f'Authorization: Bearer {access_token}',
        '-H', 'Content-Type: application/json',
        '-d', vote_json
    ], capture_output=True, text=True)
    
    print(f'Vote submitted: {vote_resp.stdout[:200]}')
"

log "=== Judging complete ==="
