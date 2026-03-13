#!/bin/bash
# Simmer 简单策略 - 只买低概率
# 运行: 每小时 (crontab)

API_KEY="sk_live_23e89127d0f0ef51900d6c49c6c419eebee38449b43778811624009e39e7bf69"
LOG="$HOME/.openclaw/workspace/memory/simmer-simple.log"

log() { echo "[$(date '+%m-%d %H:%M')] $1" >> "$LOG"; }

# 检查冷却 (1小时)
[ -f /tmp/simmer_simple.last ] && [ $(($(date +%s)-$(cat /tmp/simmer_simple.last))) -lt 3600 ] && log "冷却中" && exit 0

# 获取市场
MARKETS=$(curl -s "https://api.simmer.markets/api/markets?status=open&venue=simmer" -H "Authorization: Bearer $API_KEY")

# 只选BTC/ETH + 低概率
MARKET=$(echo "$MARKETS" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for m in data.get('markets',[]):
    q=m.get('question','')
    if 'Bitcoin' not in q and 'BTC' not in q: continue
    yes=m.get('yes_price',0.5)
    if yes<0.12 or yes>0.88:
        print(m['id'], yes, m['question'][:40], sep='|')
        break
" 2>/dev/null)

[ -z "$MARKET" ] && log "无低概率市场" && exit 0

ID=$(echo "$MARKET" | cut -d'|' -f1)
PRICE=$(echo "$MARKET" | cut -d'|' -f2)
SIDE=$(echo "$MARKET" | awk -F'|' '{print ($2<0.5)?"yes":"no"}')

# 交易
RESULT=$(curl -s -X POST "https://api.simmer.markets/api/sdk/trade" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"market_id\":\"$ID\",\"side\":\"$SIDE\",\"amount\":5,\"venue\":\"simmer\",\"reason\":\"低概率策略\"}")

echo "$ID|$SIDE|$PRICE|$RESULT" >> "$LOG"
[ -n "$ID" ] && date +%s > /tmp/simmer_simple.last
