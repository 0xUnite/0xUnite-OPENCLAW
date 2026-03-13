#!/bin/bash
# WTT自然交易理论 - Bybit合约模拟盘
# 核心理念: 通道 + Fib回撤 + 买方/卖方量能

STATE_FILE="$HOME/.openclaw/workspace/memory/wtt-sim-state.json"

[ ! -f "$STATE_FILE" ] && echo '{"balance": 1000, "position": null, "entries": [], "pnl_total": 0, "trade_count": 0, "win_count": 0}' > "$STATE_FILE"

echo "========== WTT交易系统 =========="

# 1. 获取实时价格
PRICE=$(curl -s "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['list'][0]['lastPrice'])")
echo "BTC价格: $PRICE"

# 2. 获取K线
K240=$(curl -s "https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=240&limit=100")

# 3. 提取高低点
HL240=$(echo "$K240" | python3 -c "
import sys, json
d = json.loads(input())
k = d['result']['list']
highs = [float(x[2]) for x in k]
lows = [float(x[3]) for x in k]
print(f'{max(highs[-10:])},{min(lows[-10:])},{max(highs[-30:])},{min(lows[-30:])}')
")

H240_10=$(echo "$HL240" | cut -d, -f1)
L240_10=$(echo "$HL240" | cut -d, -f2)
H240_30=$(echo "$HL240" | cut -d, -f3)
L240_30=$(echo "$HL240" | cut -d, -f4)

echo "周期(4H): 高=$H240_30, 低=$L240_30"

# 4. 判断通道
if python3 -c "exit(0 if float('$H240_10') > float('$H240_30') and float('$L240_10') > float('$L240_30') else 1)" 2>/dev/null; then
    CH_TYPE="up"
elif python3 -c "exit(0 if float('$H240_10') < float('$H240_30') and float('$L240_10') < float('$L240_30') else 1)" 2>/dev/null; then
    CH_TYPE="down"
else
    CH_TYPE="sideways"
fi
echo "通道: $CH_TYPE"

# 5. Fib回撤
FIB_382=$(python3 -c "print(round($L240_30 + ($H240_30 - $L240_30) * 0.382, 2))")
FIB_618=$(python3 -c "print(round($L240_30 + ($H240_30 - $L240_30) * 0.618, 2))")
echo "Fib: 0.382=$FIB_382, 0.618=$FIB_618"

# 6. 买方/卖方量能
ENERGY=$(curl -s "https://api.bybit.com/v5/market/orderbook?category=linear&symbol=BTCUSDT&limit=20" | python3 -c "
import sys, json
d = json.load(sys.stdin)
bids = [(float(p[1]), float(p[0])) for p in d['result']['b'][:10]]
asks = [(float(p[1]), float(p[0])) for p in d['result']['a'][:10]]
buy = sum(b[0]*b[1] for b in bids)
sell = sum(a[0]*a[1] for a in asks)
ratio = buy/sell if sell > 0 else 1
if ratio > 1.5: print('buy')
elif ratio < 0.67: print('sell')
else: print('balanced')
")
echo "量能: $ENERGY"

# 7. WTT信号判断
SIGNAL="none"
DIRECTION="观望"

if [ "$CH_TYPE" = "up" ]; then
    echo ">>> 上升通道 <<<"
    if [ "$ENERGY" = "buy" ]; then
        SIGNAL="long"; DIRECTION="做多"
    fi
elif [ "$CH_TYPE" = "down" ]; then
    echo ">>> 下降通道 <<<"
    if [ "$ENERGY" = "sell" ]; then
        SIGNAL="short"; DIRECTION="做空"
    fi
else
    echo ">>> 震荡 <<<"
    # 买方强+价格低 做多
    if [ "$ENERGY" = "buy" ] && python3 -c "exit(0 if float('$PRICE') <= float('$FIB_618') else 1)" 2>/dev/null; then
        SIGNAL="long"; DIRECTION="做多(支撑)"
    # 卖方强+价格高 做空  
    elif [ "$ENERGY" = "sell" ] && python3 -c "exit(0 if float('$PRICE') >= float('$FIB_382') else 1)" 2>/dev/null; then
        SIGNAL="short"; DIRECTION="做空(压力)"
    fi
fi

echo "信号: $SIGNAL $DIRECTION"

# 8. 交易执行
balance=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['balance'])")
has_pos=$(python3 -c "import json; print('yes' if json.load(open('$STATE_FILE'))['position'] else 'no')")
echo "余额: ${balance}U, 持仓: $has_pos"

if [ "$has_pos" = "yes" ]; then
    pos=$(python3 -c "import json; p=json.load(open('$STATE_FILE'))['position']; print(f'{p[\"side\"]},{p[\"entry_price\"]},{p[\"stop_loss\"]},{p[\"take_profit\"]}')")
    side=$(echo "$pos" | cut -d, -f1)
    entry=$(echo "$pos" | cut -d, -f2)
    sl=$(echo "$pos" | cut -d, -f3)
    tp=$(echo "$pos" | cut -d, -f4)
    echo "持仓检查: $side @ $entry"
    
    pnl=0; reason=""
    if [ "$side" = "long" ]; then
        python3 -c "exit(0 if float('$PRICE') <= float('$sl'))" 2>/dev/null && { pnl=$(python3 -c "print(int(($sl-$entry)/$entry*1000))"); reason="SL"; }
        python3 -c "exit(0 if float('$PRICE') >= float('$tp'))" 2>/dev/null && { pnl=$(python3 -c "print(int(($tp-$entry)/$entry*1000))"); reason="TP"; }
    else
        python3 -c "exit(0 if float('$PRICE') >= float('$sl'))" 2>/dev/null && { pnl=$(python3 -c "print(int(($entry-$sl)/$entry*1000))"); reason="SL"; }
        python3 -c "exit(0 if float('$PRICE') <= float('$tp'))" 2>/dev/null && { pnl=$(python3 -c "print(int(($entry-$tp)/$entry*1000))"); reason="TP"; }
    fi
    
    if [ -n "$reason" ]; then
        python3 << EOF
import json
with open("$STATE_FILE") as f: s=json.load(f)
s["balance"] = s["balance"] + $pnl
s["pnl_total"] = s["pnl_total"] + $pnl
s["trade_count"] += 1
if $pnl > 0: s["win_count"] += 1
s["position"] = None
with open("$STATE_FILE", "w") as f: json.dump(s, f)
EOF
        echo "✅ 平仓: ${pnl}U ($reason)"
    fi
else
    if [ "$SIGNAL" != "none" ]; then
        if [ "$SIGNAL" = "long" ]; then
            sl=$(python3 -c "print(int(float('$PRICE')*0.98))")
            tp=$(python3 -c "print(int(float('$PRICE')*1.04))")
        else
            sl=$(python3 -c "print(int(float('$PRICE')*1.02))")
            tp=$(python3 -c "print(int(float('$PRICE')*0.98))")
        fi
        python3 << EOF
import json
with open("$STATE_FILE") as f: s=json.load(f)
s["position"] = {"side": "$SIGNAL", "size": 100, "entry_price": float("$PRICE"), "stop_loss": $sl, "take_profit": $tp}
with open("$STATE_FILE", "w") as f: json.dump(s, f)
EOF
        echo "✅ 开仓: $SIGNAL 100U @ $PRICE"
    fi
fi

# 计算未实现盈亏
unrealized_pnl=0
if [ "$has_pos" = "yes" ]; then
    if [ "$side" = "long" ]; then
        unrealized_pnl=$(python3 -c "print(round(($PRICE - $entry) / $entry * 1000, 2))")
    else
        unrealized_pnl=$(python3 -c "print(round(($entry - $PRICE) / $entry * 1000, 2))")
    fi
fi

total_pnl=$(python3 -c "print(round($unrealized_pnl + $(python3 -c "import json; print(json.load(open('$STATE_FILE'))['pnl_total'])"), 2))")

python3 -c "
import json
s=json.load(open('$STATE_FILE'))
print(f\"余额: {s['balance']}U, 盈亏: $total_pnl U (已实现: {s['pnl_total']}U, 未实现: $unrealized_pnl U), 交易:{s['trade_count']}\")
if s['position']: print(f\"持仓: {s['position']['side']} @ {s['position']['entry_price']}\")
"
