#!/usr/bin/env python3
# polymarket_arb_scanner.py
# OpenClaw 预测市场套利扫描器 - 模拟盘模式
# 测试几天复盘改进

import requests
import json
import time
import os
from datetime import datetime
from collections import defaultdict

# ============ 配置 ============
CONFIG = {
    "POLYMARKET_API": "https://clob.polymarket.com",
    "SCAN_INTERVAL": 600,        # 10分钟扫描一次
    "MIN_PREMIUM": 0.08,        # 最小溢价 8%
    "MAX_POSITION": 0.06,        # 最大仓位 6%
    "KELLY_FRACTION": 0.5,      # 凯利准则使用一半
    "MOCK_MODE": True,           # 模拟盘模式
    "INITIAL_CAPITAL": 100,     # 初始资金 $100
}

# 模拟资金
capital = CONFIG["INITIAL_CAPITAL"]
positions = []  # 持仓记录
signals = []    # 信号记录
trade_log = []  # 交易日志

# ============ API 函数 ============
def get_markets(category="trending", limit=100):
    """获取市场列表"""
    try:
        r = requests.get(f"{CONFIG['POLYMARKET_API']}/markets",
                         params={"category": category, "limit": limit},
                         timeout=30)
        return r.json().get("data", [])
    except Exception as e:
        print(f"❌ 获取市场失败: {e}")
        return []

def get_market_prices(condition_id):
    """获取市场价格"""
    try:
        r = requests.get(f"{CONFIG['POLYMARKET_API']}/prices",
                         params={"condition_id": condition_id},
                         timeout=10)
        return r.json()
    except:
        return {}

def get_external_data(market_question):
    """获取外部数据（简化版）"""
    data = {
        "crypto": get_crypto_sentiment(),
        "news": get_news_sentiment(market_question),
    }
    return data

def get_crypto_sentiment():
    """加密货币市场情绪"""
    try:
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                        params={"vs_currency": "usd", "ids": "bitcoin,ethereum", "order": "market_cap_desc", "per_page": 2},
                        timeout=10)
        data = r.json()
        if data:
            return {"btc_change_24h": data[0].get("price_change_percentage_24h", 0),
                   "eth_change_24h": data[1].get("price_change_percentage_24h", 0)}
    except:
        pass
    return {"btc_change_24h": 0, "eth_change_24h": 0}

def get_news_sentiment(question):
    """简单情感分析（实际可以用更复杂的API）"""
    # 简化版：关键词判断
    positive_words = ["win", "rise", "up", "bull", "growth", "pass", "yes"]
    negative_words = ["lose", "fall", "down", "bear", "drop", "fail", "no"]
    
    question_lower = question.lower()
    pos_count = sum(1 for w in positive_words if w in question_lower)
    neg_count = sum(1 for w in negative_words if w in question_lower)
    
    if pos_count > neg_count:
        return 0.1  # 略微乐观
    elif neg_count > pos_count:
        return -0.1  # 略微悲观
    return 0

# ============ 凯利准则 ============
def kelly_bet(win_prob, odds, fraction=0.5):
    """凯利准则计算仓位"""
    if odds <= 1:
        return 0
    b = odds - 1
    p = win_prob
    q = 1 - p
    kelly = (b * p - q) / b
    if kelly <= 0:
        return 0
    return kelly * fraction

# ============ AI 分析 ============
def analyze_with_ai(market_question, prices, external_data):
    """
    分析溢价机会
    返回: {"premium": 0.1, "true_probability": 0.6, "recommendation": "BUY_YES", "reason": "..."}
    """
    # 简化版分析（实际可以用 MiniMax API）
    try:
        current_price = float(prices.get("yes_price", 0.5))
    except:
        current_price = 0.5
    
    # 基于外部数据的概率调整
    sentiment = external_data.get("news", 0)
    crypto_sent = external_data.get("crypto", {})
    crypto_factor = (crypto_sent.get("btc_change_24h", 0) + crypto_sent.get("eth_change_24h", 0)) / 100
    
    # 调整后的真实概率
    true_prob = current_price + sentiment + crypto_factor
    true_prob = max(0.01, min(0.99, true_prob))
    
    # 溢价
    premium = true_prob - current_price
    
    return {
        "premium": premium,
        "true_probability": true_prob,
        "current_price": current_price,
        "recommendation": "BUY_YES" if premium > CONFIG["MIN_PREMIUM"] else "HOLD",
        "reason": f"价格:{current_price:.2%}, 真实概率:{true_prob:.2%}, 溢价:{premium:.2%}"
    }

# ============ 交易执行 ============
def execute_trade(market, analysis, size):
    """执行交易"""
    global capital, positions, trade_log
    
    if CONFIG["MOCK_MODE"]:
        # 模拟盘
        cost = capital * size
        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market": market["question"][:50],
            "type": "BUY_YES",
            "size": size,
            "cost": cost,
            "price": analysis["current_price"],
            "premium": analysis["premium"],
            "mode": "MOCK"
        }
        trade_log.append(trade)
        capital -= cost
        positions.append(trade)
        print(f"  📝 [模拟] 买入 {size:.2%} @ {analysis['current_price']:.2%}, 成本 ${cost:.2f}")
    else:
        # 实盘（待实现）
        pass

def record_signal(market, analysis):
    """记录信号"""
    global signals
    signal = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": market["question"][:80],
        "current_price": analysis["current_price"],
        "true_prob": analysis["true_probability"],
        "premium": analysis["premium"],
        "recommendation": analysis["recommendation"],
    }
    signals.append(signal)
    
    # 保存信号
    with open("/Users/sudi/.openclaw/workspace/memory/arb-signals.json", "w") as f:
        json.dump(signals[-100:], f, indent=2)

# ============ 主循环 ============
def scan_and_analyze():
    global capital
    
    print(f"\n{'='*50}")
    print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始扫描...")
    print(f"💰 资金: ${capital:.2f}")
    
    markets = get_markets("trending", 100)
    print(f"📊 获取到 {len(markets)} 个市场")
    
    opportunities = 0
    
    for market in markets[:50]:  # 分析前50个
        condition_id = market.get("condition_id")
        if not condition_id:
            continue
            
        prices = get_market_prices(condition_id)
        if not prices or "yes_price" not in prices:
            continue
        
        external_data = get_external_data(market["question"])
        analysis = analyze_with_ai(market["question"], prices, external_data)
        
        if analysis["premium"] > CONFIG["MIN_PREMIUM"]:
            opportunities += 1
            print(f"  ✅ 机会! {market['question'][:40]}...")
            print(f"     价格: {analysis['current_price']:.2%} → 真实: {analysis['true_probability']:.2%}")
            print(f"     溢价: {analysis['premium']:.2%}")
            
            # 记录信号
            record_signal(market, analysis)
            
            # 计算仓位
            odds = 1 / analysis["current_price"]
            position = kelly_bet(analysis["true_probability"], odds, CONFIG["KELLY_FRACTION"])
            position = min(position, CONFIG["MAX_POSITION"])
            
            if position > 0.01:  # 最小1%
                execute_trade(market, analysis, position)
    
    print(f"📈 发现 {opportunities} 个机会")
    
    # 保存交易日志
    with open("/Users/sudi/.openclaw/workspace/memory/arb-trades.json", "w") as f:
        json.dump(trade_log, f, indent=2)
    
    return opportunities

# ============ 启动 ============
if __name__ == "__main__":
    print("🚀 Polymarket 套利扫描器启动（模拟盘模式）")
    print(f"📋 配置: 扫描间隔 {CONFIG['SCAN_INTERVAL']}s, 最小溢价 {CONFIG['MIN_PREMIUM']:.0%}")
    print(f"💵 初始资金: ${CONFIG['INITIAL_CAPITAL']}")
    
    # 首次运行
    scan_and_analyze()
    
    # 循环
    while True:
        time.sleep(CONFIG["SCAN_INTERVAL"])
        try:
            scan_and_analyze()
        except Exception as e:
            print(f"❌ 错误: {e}")
            time.sleep(60)
