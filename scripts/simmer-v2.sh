#!/bin/bash
# Simmer V2 优化策略 - 只买低概率 + 减少交易频率

API_KEY="sk_live_23e89127d0f0ef51900d6c49c6c419eebee38449b43778811624009e39e7bf69"
LOG_FILE="/Users/sudi/.openclaw/workspace/memory/simmer-v2.log"
AMOUNT=5

# 冷却: 每小时最多1笔交易
LAST_TRADE_FILE="/tmp/simmer_v2_last_trade"
if [ -f "$LAST_TRADE_FILE" ]; then
    last=$(cat "$LAST_TRADE_FILE")
    now=$(date +%s)
    if [ $((now - last)) -lt 1800 ]; then  # 30分钟冷却
        echo "[$(date '+%m-%d %H:%M')] 冷却中，跳过" >> "$LOG_FILE"
        exit 0
    fi
fi

# 获取市场列表
MARKETS=$(curl -s "https://api.simmer.markets/api/markets?status=open&venue=simmer" \
    -H "Authorization: Bearer $API_KEY")

# 过滤高质量市场
QUALITY_MARKETS=$(echo "$MARKETS" | python3 -c "
import sys,json
data=json.load(sys.stdin)
markets=data.get('markets',[])

# 只选满足条件的市场
good = []
for m in markets:
    q = m.get('question','')
    
    # 必须包含关键词
    if not any(k in q for k in ['Bitcoin','BTC','Ethereum','ETH','AI','Nvidia','Tesla','Crypto']):
        continue
    
    # 跳过已结束的
    if m.get('volume',0) < 1000:
        continue
    
    # 获取当前价格
    yes_price = m.get('yes_price', 0.5)
    
    # 只买低概率 (yes_price < 0.15 或 yes_price > 0.85)
    if yes_price < 0.15:
        good.append({
            'id': m['id'],
            'question': q,
            'price': yes_price,
            'direction': 'yes',
            'reason': '低概率高赔率'
        })
    elif yes_price > 0.85:
        good.append({
            'id': m['id'],
            'question': q,
            'price': yes_price,
            'direction': 'no', 
            'reason': '高概率但赔率差'
        })

# 只返回最好的1个
if good:
    best = good[0]
    print(json.dumps(best))
")

if [ -z "$QUALITY_MARKETS" ]; then
    echo "[$(date '+%m-%d %H:%M')] 无高质量市场" >> "$LOG_FILE"
    exit 0
fi

echo "选中: $(echo $QUALITY_MARKETS | python3 -c 'import sys,json; print(json.load(sys.stdin)[\"question\"][:50])')"

# 执行交易
MARKET_ID=$(echo "$QUALITY_MARKETS" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
DIRECTION=$(echo "$QUALITY_MARKETS" | python3 -c 'import sys,json; print(json.load(sys.stdin)["direction"])')

RESULT=$(curl -s -X POST "https://api.simmer.markets/api/sdk/trade" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"market_id\": \"$MARKET_ID\",
        \"side\": \"$DIRECTION\",
        \"amount\": $AMOUNT,
        \"venue\": \"simmer\",
        \"reason\": \"V2低概率策略\"
    }")

echo "$RESULT" >> "$LOG_FILE"

if echo "$RESULT" | grep -q "error"; then
    echo "交易失败"
else
    echo "$(date '+%m-%d %H:%M') 成交: $DIRECTION \$$AMOUNT" >> "$LOG_FILE"
    date +%s > "$LAST_TRADE_FILE"
fi
