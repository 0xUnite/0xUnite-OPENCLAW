#!/usr/bin/env python3
# Binance V3 交易系统 - 百万Eric核心原则

import requests
import time
from datetime import datetime

API = "https://api.binance.com/api/v3"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]

log = lambda msg: print(f"[{datetime.now().strftime('%m-%d %H:%M')}] {msg}", flush=True)

def get_klines(symbol, interval="4h", limit=20):
    try:
        url = f"{API}/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        
        result = []
        for k in data:
            result.append({
                "close": float(k[4]),
                "volume": float(k[5])
            })
        return result
    except Exception as e:
        log(f"❌ {e}")
        return []

def calc_ma(data, period):
    if len(data) < period:
        return None
    return sum(d['close'] for d in data[-period:]) / period

def check_trend(symbol):
    h4 = get_klines(symbol, "4h", 50)
    d1 = get_klines(symbol, "1d", 20)
    
    if not h4 or not d1:
        return None
    
    price = h4[-1]['close']
    ma20_4h = calc_ma(h4, 20)
    ma50_4h = calc_ma(h4, 50)
    ma20_d1 = calc_ma(d1, 20)
    
    if not ma20_4h or not ma50_4h or not ma20_d1:
        return None
    
    # 趋势判断
    signal = None
    if price > ma20_d1 and price > ma20_4h and ma20_4h > ma50_4h:
        signal = "做多"
    elif price < ma20_d1 and price < ma20_4h and ma20_4h < ma50_4h:
        signal = "做空"
    
    return {
        "symbol": symbol,
        "price": price,
        "ma20_4h": ma20_4h,
        "ma50_4h": ma50_4h,
        "ma20_d1": ma20_d1,
        "signal": signal
    }

def main():
    log("=== Binance V3 启动 ===")
    log("原则: 均线多头+回调企稳 | 严格止损2%")
    
    while True:
        try:
            for symbol in SYMBOLS:
                info = check_trend(symbol)
                if info:
                    log(f"{symbol}: 价格${info['price']:,.0f} | MA20={info['ma20_4h']:,.0f} | MA50={info['ma50_4h']:,.0f} | 信号: {info['signal']}")
            time.sleep(300)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log(f"错误: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
