#!/bin/bash
# 加密货币每日新闻摘要 (含币安数据)

DATE=$(date +%Y-%m-%d)
echo "=== $DATE 加密货币新闻摘要 ==="
echo ""

# 获取币安价格
echo "💰 币安价格快照"
echo "| 币种 | 价格 (USDT) |"
echo "|------|------------|"

BTC=$(curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" | python3 -c "import sys,json; print(json.load(sys.stdin)['price'])" 2>/dev/null || echo "N/A")
ETH=$(curl -s "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT" | python3 -c "import sys,json; print(json.load(sys.stdin)['price'])" 2>/dev/null || echo "N/A")
SOL=$(curl -s "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT" | python3 -c "import sys,json; print(json.load(sys.stdin)['price'])" 2>/dev/null || echo "N/A")

echo "| BTC | \$$BTC |"
echo "| ETH | \$$ETH |"
echo "| SOL | \$$SOL |"
echo ""

# 抓取 RSS 新闻
echo "📰 抓取最新新闻..."
blogwatcher scan 2>&1

echo ""
echo "📄 最新文章 (前5篇):"
blogwatcher articles -a | head -10

echo ""
echo "✅ 完成"
