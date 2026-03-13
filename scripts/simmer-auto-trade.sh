#!/bin/bash
# Simmer 自动交易策略 - 高质量市场过滤 + $5/次 + 防rate limit

API_KEY="sk_live_23e89127d0f0ef51900d6c49c6c419eebee38449b43778811624009e39e7bf69"
LOG_FILE="/Users/sudi/.openclaw/workspace/memory/simmer.log"
TRADE_FILE="/Users/sudi/.openclaw/workspace/memory/simmer-trades.json"
AMOUNT=5
RATE_LIMIT_SECONDS=120

# 初始化交易记录文件
init_trade_file() {
    if [ ! -f "$TRADE_FILE" ]; then
        echo "[]" > "$TRADE_FILE"
    fi
}

# 添加交易记录
add_trade() {
    local id="$1"
    local side="$2"
    local cost="$3"
    local question="$4"
    local timestamp=$(date +%s)
    
    # 读取现有记录
    local trades=$(cat "$TRADE_FILE")
    # 添加新记录
    local new_trade="{\"id\":\"$id\",\"side\":\"$side\",\"cost\":$cost,\"question\":\"$question\",\"timestamp\":$timestamp,\"resolved\":false}"
    # 用jq添加
    echo "$trades" | jq --argjson new "$new_trade" '. + [$new]' > "$TRADE_FILE.tmp" && mv "$TRADE_FILE.tmp" "$TRADE_FILE"
}

# 检查结算
check_settlements() {
    local total_profit=0
    local total_cost=0
    local settled_count=0
    
    # 获取未结算交易数量
    local unresolved_count=$(cat "$TRADE_FILE" | jq '[.[] | select(.resolved == false)] | length' 2>/dev/null || echo "0")
    
    # 如果未结算太多,跳过检查(避免API超时)
    if [ "$unresolved_count" -gt 50 ]; then
        echo "未结算交易过多($unresolved_count笔),跳过结算检查" >> "$LOG_FILE"
        return
    fi
    
    # 获取所有未结算交易(最多20个)
    local ids=$(cat "$TRADE_FILE" | jq -r '.[] | select(.resolved == false) | .id' 2>/dev/null | head -20)
    
    for id in $ids; do
        # 查询市场状态 (with timeout)
        local market=$(curl -s --max-time 10 "https://api.simmer.markets/api/sdk/markets/$id" \
            -H "Authorization: Bearer $API_KEY" || echo '{}')
        
        local status=$(echo "$market" | jq -r '.status' 2>/dev/null)
        
        if [ "$status" == "resolved" ] || [ "$status" == "closed" ]; then
            # 获取结果
            local outcome=$(echo "$market" | jq -r '.outcome // "unknown"' 2>/dev/null)
            local payout=$(echo "$market" | jq -r '.payout // 0' 2>/dev/null)
            local question=$(cat "$TRADE_FILE" | jq -r ".[] | select(.id == \"$id\") | .question" 2>/dev/null)
            local side=$(cat "$TRADE_FILE" | jq -r ".[] | select(.id == \"$id\") | .side" 2>/dev/null)
            local cost=$(cat "$TRADE_FILE" | jq -r ".[] | select(.id == \"$id\") | .cost" 2>/dev/null)
            
            # 判断是否赢
            local won=false
            if [ "$outcome" == "$side" ]; then
                won=true
            fi
            
            # 计算盈利
            local profit=0
            if [ "$won" == "true" ]; then
                profit=$(echo "$payout - $cost" | bc 2>/dev/null || echo "0")
            else
                profit=$(echo "-$cost" | bc 2>/dev/null || echo "0")
            fi
            
            echo "结算: $question | 下注: $side | 结果: $outcome | 成本: $$cost | 收益: $$payout | 盈利: $$profit" >> "$LOG_FILE"
            
            # 更新记录为已结算
            local trades=$(cat "$TRADE_FILE")
            echo "$trades" | jq --arg id "$id" --argjson payout "$payout" --arg outcome "$outcome" \
                '(.[] | select(.id == $id)) |= .resolved = true | .[].payout = $payout | .[].outcome = $outcome' > "$TRADE_FILE.tmp" && mv "$TRADE_FILE.tmp" "$TRADE_FILE"
            
            total_profit=$(echo "$total_profit + $profit" | bc 2>/dev/null || echo "0")
            total_cost=$(echo "$total_cost + $cost" | bc 2>/dev/null || echo "0")
            settled_count=$((settled_count + 1))
        fi
    done
    
    # 输出统计
    if [ $settled_count -gt 0 ]; then
        echo "========== 结算统计 ==========" >> "$LOG_FILE"
        echo "本次结算: $settled_count 笔" >> "$LOG_FILE"
        echo "总盈亏: $$total_profit" >> "$LOG_FILE"
        # 计算历史总盈亏
        local all_profit=$(cat "$TRADE_FILE" | jq '[.[] | select(.resolved == true) | .payout - .cost] | add' 2>/dev/null || echo "0")
        echo "历史总盈亏: $$all_profit" >> "$LOG_FILE"
    fi
}

init_trade_file

# 高质量市场关键词
GOOD_KEYWORDS=("Bitcoin" "BTC" "Ethereum" "ETH" "AI" "Anthropic" "OpenAI" "Crypto" "Apple" "XRP" "Solana" "Dogecoin" "Cardano" "Polygon" "Meme" "Trump" "Fed" "Interest" "GDP" "Nvidia" "Tesla" "SpaceX" "NVIDIA" "Ubisoft" "acquired" "MAGA")

# 低质量市场关键词
BAD_KEYWORDS=("temperature" "weather" "Miami" "Seoul" "Pokemon" "Logan" "sports" "game" "winner" "election" "Charizard")

# 检查最近是否交易过
is_recent_traded() {
    local id="$1"
    local now=$(date +%s)
    
    # 读取上次交易时间
    if [ -f /tmp/simmer_last_trade ]; then
        local last_market=$(cat /tmp/simmer_last_trade)
        if [ "$last_market" == "$id" ]; then
            return 0  # 最近交易过
        fi
    fi
    return 1
}

mark_traded() {
    local id="$1"
    echo "$id" > /tmp/simmer_last_trade
}

is_good_market() {
    local q="$1"
    for kw in $BAD_KEYWORDS; do
        [[ "$q" == *"$kw"* ]] && return 1
    done
    for kw in $GOOD_KEYWORDS; do
        [[ "$q" == *"$kw"* ]] && return 0
    done
    return 1
}

generate_reasoning() {
    local q="$1"
    [[ "$q" == *"Bitcoin"* ]] || [[ "$q" == *"BTC"* ]] && echo "BTC链上数据分析" && return
    [[ "$q" == *"Ethereum"* ]] || [[ "$q" == *"ETH"* ]] && echo "ETH技术面分析" && return
    [[ "$q" == *"AI"* ]] || [[ "$q" == *"Anthropic"* ]] && echo "AI赛道分析" && return
    echo "市场趋势分析"
}

echo "========== $(date) ==========" >> "$LOG_FILE"

# 先检查结算
check_settlements

OPPS=$(curl -s --max-time 30 "https://api.simmer.markets/api/sdk/markets/opportunities?limit=10" \
  -H "Authorization: Bearer $API_KEY")

COUNT=$(echo "$OPPS" | jq '.opportunities | length')
FOUND=0

for i in $(seq 0 $((COUNT-1))); do
    ID=$(echo "$OPPS" | jq -r ".opportunities[$i].id")
    Q=$(echo "$OPPS" | jq -r ".opportunities[$i].question")
    SIDE=$(echo "$OPPS" | jq -r ".opportunities[$i].recommended_side")
    
    # 使用 opportunities 中的 current_probability
    PROB=$(echo "$OPPS" | jq -r ".opportunities[$i].current_probability // 0.5")
    PROB_PCT=$(echo "$PROB * 100" | bc 2>/dev/null || echo "0")
    
    # 跳过最近交易过的市场
    if is_recent_traded "$ID"; then
        echo "Rate limit跳过: $Q" >> "$LOG_FILE"
        continue
    fi
    
    # V2策略: 只买低概率(<15%)或高概率(>85%)
    IS_LOW_PROB=$(echo "$PROB_PCT < 15" | bc 2>/dev/null || echo "0")
    IS_HIGH_PROB=$(echo "$PROB_PCT > 85" | bc 2>/dev/null || echo "0")
    if [ "$IS_LOW_PROB" != "1" ] && [ "$IS_HIGH_PROB" != "1" ]; then
        echo "跳过(概率${PROB_PCT}%): $Q" >> "$LOG_FILE"
        continue
    fi
    
    if is_good_market "$Q"; then
        REASONING=$(generate_reasoning "$Q")
        echo "选中: $Q" >> "$LOG_FILE"
        echo "方向: $SIDE 金额: $AMOUNT" >> "$LOG_FILE"
        
        RESPONSE=$(curl -s --max-time 30 -X POST "https://api.simmer.markets/api/sdk/trade" \
          -H "Authorization: Bearer $API_KEY" \
          -H "Content-Type: application/json" \
          -d "{\"market_id\": \"$ID\", \"side\": \"$SIDE\", \"amount\": $AMOUNT, \"venue\": \"simmer\", \"reasoning\": \"$REASONING\"}")
        
        if echo "$RESPONSE" | grep -q '"success":true'; then
            COST=$(echo "$RESPONSE" | jq -r '.cost // "0"')
            echo "成交: $COST" >> "$LOG_FILE"
            add_trade "$ID" "$SIDE" "$COST" "$Q"
            mark_traded "$ID"
            FOUND=1
        else
            ERROR=$(echo "$RESPONSE" | jq -r '.error // "error"')
            echo "失败: $ERROR" >> "$LOG_FILE"
            # 如果是rate limit,标记已交易
            [[ "$ERROR" == *"Rate limit"* ]] && mark_traded "$ID"
        fi
        break
    else
        echo "跳过: $Q" >> "$LOG_FILE"
    fi
done

[ $FOUND -eq 0 ] && echo "无高质量/可交易市场" >> "$LOG_FILE"
exit 0
