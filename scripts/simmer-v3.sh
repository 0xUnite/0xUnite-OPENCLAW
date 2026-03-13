#!/bin/bash
# Simmer V3 - 百万Eric交易体系
# 核心原则：截断亏损、让利润奔跑、保护本金

API_KEY="sk_live_23e89127d0f0ef51900d6c49c6c419eebee38449b43778811624009e39e7bf69"
LOG="$HOME/.openclaw/workspace/memory/simmer-v3.log"

log() { echo "[$(date '+%m-%d %H:%M')] $1" | tee -a "$LOG"; }

# ========== V3 核心原则 ==========
# 1. 只做高概率 (>85% 或 <15%)
# 2. 大周期定方向，小周期找入场
# 3. 严格止损 (1-2%)
# 4. 让利润奔跑
# 5. 减少交易频率

# 冷却: 每2小时最多1笔
LAST_TRADE="/tmp/simmer_v3.last"
[ -f "$LAST_TRADE" ] && [ $(($(date +%s)-$(cat $LAST_TRADE))) -lt 7200 ] && log "冷却中" && exit 0

# 获取市场
MARKETS=$(curl -s "https://api.simmer.markets/api/markets?status=open&venue=simmer" -H "Authorization: Bearer $API_KEY")

# 筛选高质量市场
SELECTED=$(echo "$MARKETS" | python3 -c "
import sys,json
data=json.load(sys.stdin)
markets=data.get('markets',[])

candidates = []
for m in markets:
    q=m.get('question','')
    vol=m.get('volume',0)
    yes=m.get('yes_price',0.5)
    
    # 只选高质量关键词
    if not any(k in q for k in ['Bitcoin','BTC','Ethereum','ETH','AI','Crypto']):
        continue
    
    if vol < 5000:
        continue
    
    # 只买极端概率
    if yes < 0.12:
        candidates.append({
            'id': m['id'],
            'question': q[:50],
            'price': yes,
            'direction': 'yes',
            'reason': '低概率高赔率'
        })
    elif yes > 0.88:
        candidates.append({
            'id': m['id'],
            'question': q[:50],
            'price': yes,
            'direction': 'no', 
            'reason': '高概率确认趋势'
        })

# 只返回最好的1个
if candidates:
    best = candidates[0]
    print(json.dumps(best))
")

[ -z "$SELECTED" ] && log "无高质量市场" && exit 0

# 解析
ID=$(echo "$SELECTED" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["id"])')
PRICE=$(echo "$SELECTED" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["price"])')
SIDE=$(echo "$SELECTED" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["direction"])')
REASON=$(echo "$SELECTED" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["reason"])')

log "=== V3交易 ==="
log "方向: $SIDE ($REASON)"
log "价格: $PRICE"

# 执行交易 (小额测试)
AMOUNT=5
RESULT=$(curl -s -X POST "https://api.simmer.markets/api/sdk/trade" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"market_id\":\"$ID\",\"side\":\"$SIDE\",\"amount\":$AMOUNT,\"venue\":\"simmer\",\"reason\":\"V3体系:$REASON\"}")

if echo "$RESULT" | grep -q "error"; then
    log "交易失败: $RESULT"
else
    log "✅ 成交: $SIDE \$$AMOUNT"
    date +%s > "$LAST_TRADE"
fi
