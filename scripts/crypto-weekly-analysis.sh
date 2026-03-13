#!/bin/bash
# 加密货币每周分析报告
# 每周五 18:00 自动运行

TODAY=$(date +%Y-%m-%d)
TREND_FILE="$HOME/.openclaw/workspace/memory/crypto-trend.md"

echo "=== $TODAY 加密货币周分析 ==="

# 获取当前价格
BTC=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" | python3 -c "import sys,json; print(json.load(sys.stdin)['bitcoin']['usd'])")
ETH=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" | python3 -c "import sys,json; print(json.load(sys.stdin)['ethereum']['usd'])")
SOL=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd" | python3 -c "import sys,json; print(json.load(sys.stdin)['solana']['usd'])")

FNG=$(curl -s "https://api.alternative.me/fng/?limit=1" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['data'][0]['value'])" 2>/dev/null || echo "N/A")

echo ""
echo "📊 本周价格快照"
echo "| 币种 | 价格 |"
echo "|------|------|"
echo "| BTC | \$$BTC |"
echo "| ETH | \$$ETH |"
echo "| SOL | \$$SOL |"
echo "| FNG | $FNG |"

# 生成分析报告并追加到文件
cat >> "$TREND_FILE" << EOF

---

## $TODAY 周分析

### 价格对比

| 币种 | 上周 | 本周 | 涨跌 |
|------|------|------|------|
| BTC | 待记录 | \$$BTC | - |
| ETH | 待记录 | \$$ETH | - |
| SOL | 待记录 | \$$SOL | - |

### 趋势判断

- 待分析

### 建议

- 待更新

EOF

echo ""
echo "✅ 周分析已记录到 $TREND_FILE"
