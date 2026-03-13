#!/usr/bin/env python3
# binance_arb_scanner.py
# Binance 套利扫描器 - 自然交易理论策略
# 专注 BTC/ETH | 4小时级别 | 能量理论

import requests
import json
import time
import sys
from datetime import datetime

# 强制输出flush
def log_msg(msg):
    print(msg, flush=True)

# ============ 配置 ============
CONFIG = {
    "BINANCE_API": "https://api.binance.com/api/v3",
    "SCAN_INTERVAL": 300,         # 5分钟扫描一次
    "MAX_POSITION": 0.25,         # 每次25%仓位
    "MAX_TRADES_PER_COIN": 2,    # 每个币最多买2次
    "MOCK_MODE": True,            # 模拟盘模式
    "INITIAL_CAPITAL": 100,       # 初始资金 $100
    
    # 自然交易理论参数
    "VOLUME_SPIKE": 2.0,         # 放量倍数 >2x
    "PRICE_DROP": 2.0,           # 跌幅 >2% 买入
    "PRICE_RISE": 2.0,           # 涨幅 >2% 卖出
    
    # 止盈止损 (5x杠杆)
    "STOP_LOSS": 0.05,           # 5%止损 → 实际亏损25%
    "TAKE_PROFIT": 0.06,        # 6%止盈 → 实际盈利30%
    
    # 杠杆
    "LEVERAGE": 5,
    
    # 交易对
    "SYMBOLS": ["BTCUSDT", "ETHUSDT"],
}

capital = CONFIG["INITIAL_CAPITAL"]
positions = {}  # {"BTCUSDT": 2, "ETHUSDT": 0}
trade_log = []  # 重置交易记录
trade_log = []
signals = []

# ============ API 函数 ============
def get_4h_klines(symbol, limit=6):
    """获取4小时K线"""
    try:
        url = f"{CONFIG['BINANCE_API']}/klines"
        params = {"symbol": symbol, "interval": "4h", "limit": limit}
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        
        result = []
        for k in data:
            result.append({
                "time": k[0],
                "close": float(k[4]),
                "quote_volume": float(k[7])
            })
        return result
    except Exception as e:
        log_msg(f"❌ K线获取失败: {e}")
        return []

def analyze_4h_energy(symbol):
    """自然交易理论分析 - 能量要素"""
    klines = get_4h_klines(symbol)
    if len(klines) < 2:
        return None
    
    # 比较最新一根和前一根
    current = klines[-1]
    previous = klines[-2]
    
    # 价格变化
    price_change = (current['close'] - previous['close']) / previous['close'] * 100
    
    # 量能变化
    vol_change = current['quote_volume'] / previous['quote_volume'] if previous['quote_volume'] > 0 else 1
    
    return {
        "symbol": symbol,
        "price": current['close'],
        "price_change": price_change,
        "vol_change": vol_change,
        "time": datetime.fromtimestamp(current['time']/1000).strftime("%Y-%m-%d %H:%M")
    }

def get_24h_change(symbol):
    """获取24h变化"""
    try:
        url = f"{CONFIG['BINANCE_API']}/ticker/24hr"
        params = {"symbol": symbol}
        r = requests.get(url, params=params, timeout=10)
        t = r.json()
        return float(t['priceChangePercent'])
    except:
        return 0

# ============ 交易执行 ============
def execute_trade(analysis, direction="BUY"):
    global capital, trade_log, positions
    
    symbol = analysis['symbol']
    price = analysis['price']
    
    # 检查仓位
    current_positions = positions.get(symbol, 0)
    if current_positions >= CONFIG["MAX_TRADES_PER_COIN"]:
        log_msg(f"  ⏭️ {symbol} 已买满 ({current_positions}/{CONFIG['MAX_TRADES_PER_COIN']})")
        return False
    
    # 计算买入金额 (5x杠杆)
    available = capital * CONFIG["MAX_POSITION"]
    cost = available * CONFIG["LEVERAGE"]  # 5x杠杆
    if cost < 1:
        log_msg(f"  ⚠️ 资金不足")
        return False
    
    # 计算止盈止损
    if direction == "BUY":
        stop_loss = price * (1 - CONFIG["STOP_LOSS"])
        take_profit = price * (1 + CONFIG["TAKE_PROFIT"])
    else:
        stop_loss = price * (1 + CONFIG["STOP_LOSS"])
        take_profit = price * (1 - CONFIG["TAKE_PROFIT"])
    
    trade = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "type": direction,
        "entry_price": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "price_change_4h": analysis['price_change'],
        "vol_change": analysis['vol_change'],
        "cost": cost,
        "mode": "MOCK"
    }
    
    trade_log.append(trade)
    
    if direction == "BUY":
        positions[symbol] = current_positions + 1
        capital -= cost
        log_msg(f"  🟢 [买入] {symbol} @ ${price:.2f}")
        log_msg(f"      4h: {analysis['price_change']:.2f}% | 量: {analysis['vol_change']:.1f}x | 止损: ${stop_loss:.2f} | 止盈: ${take_profit:.2f}")
    else:
        # 卖出：平仓，加回资金
        if current_positions > 0:
            positions[symbol] = current_positions - 1
            capital += cost  # 加回卖出资金
            log_msg(f"  🔴 [卖出] {symbol} @ ${price:.2f} | 回收: ${cost:.2f}")
        else:
            log_msg(f"  ⚠️ {symbol} 无仓位可卖")
            return False
    
    # 保存
    with open("/Users/sudi/.openclaw/workspace/memory/binance-trades.json", "w") as f:
        json.dump(trade_log, f, indent=2)
    
    return True

def save_signals(analysis_list):
    global signals
    for a in analysis_list:
        signals.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": a['symbol'],
            "price": a['price'],
            "price_change_4h": a['price_change'],
            "vol_change": a['vol_change'],
        })
    
    # 只保留最近100条
    with open("/Users/sudi/.openclaw/workspace/memory/binance-signals.json", "w") as f:
        json.dump(signals[-100:], f, indent=2)

# ============ 主循环 ============
def scan():
    global capital
    
    log_msg(f"\n{'='*50}")
    log_msg(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Binance自然交易扫描")
    log_msg(f"💰 资金: ${capital:.2f} | 仓位: {positions}")
    
    analysis_list = []
    signals_to_save = []
    
    for symbol in CONFIG["SYMBOLS"]:
        # 获取4小时分析
        analysis = analyze_4h_energy(symbol)
        if not analysis:
            continue
        
        analysis_list.append(analysis)
        signals_to_save.append(analysis)
        
        price_change = analysis['price_change']
        vol_change = analysis['vol_change']
        
        log_msg(f"\n📊 {symbol}:")
        log_msg(f"   价格: ${analysis['price']:.2f}")
        log_msg(f"   4h涨跌: {price_change:.2f}%")
        log_msg(f"   量能变化: {vol_change:.1f}x")
        
        # 自然交易理论策略
        # 买入：放量下跌 (量能>2x + 跌幅>2%)
        if price_change < -CONFIG["PRICE_DROP"] and vol_change > CONFIG["VOLUME_SPIKE"]:
            log_msg(f"   🎯 信号: 放量下跌 → 买入!")
            execute_trade(analysis, "BUY")
        
        # 卖出：放量上涨 (量能>2x + 涨幅>2%)
        elif price_change > CONFIG["PRICE_RISE"] and vol_change > CONFIG["VOLUME_SPIKE"]:
            log_msg(f"   🎯 信号: 放量上涨 → 卖出!")
            execute_trade(analysis, "SELL")
        
        else:
            log_msg(f"   ⏸️ 无信号")
    
    # 保存信号
    if signals_to_save:
        save_signals(signals_to_save)

# ============ 启动 ============
if __name__ == "__main__":
    log_msg("🚀 Binance 自然交易扫描器启动")
    log_msg(f"📋 交易对: {CONFIG['SYMBOLS']}")
    log_msg(f"📋 策略: 放量>{CONFIG['VOLUME_SPIKE']}x + 涨跌>{CONFIG['PRICE_DROP']}%")
    log_msg(f"📋 止损: {CONFIG['STOP_LOSS']*100}% | 止盈: {CONFIG['TAKE_PROFIT']*100}%")
    log_msg(f"💵 初始资金: ${CONFIG['INITIAL_CAPITAL']}")
    
    # 首次运行
    scan()
    
    # 循环
    while True:
        time.sleep(CONFIG["SCAN_INTERVAL"])
        try:
            scan()
        except Exception as e:
            log_msg(f"❌ 错误: {e}")
            time.sleep(60)
