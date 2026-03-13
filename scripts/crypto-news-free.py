#!/usr/bin/env python3
"""
Crypto News - Free daily briefing
Uses public RSS feeds + CoinGecko price API (no API key required)
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
]


def fetch_rss_items(source_name, url, limit=4):
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    items = []

    for item in root.findall("./channel/item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        if title:
            items.append({
                "title": title,
                "url": link,
                "source": source_name,
                "pub_date": pub_date,
            })

    return items


def get_btc_price():
    btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    btc_resp = requests.get(btc_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    btc_resp.raise_for_status()
    btc_data = btc_resp.json()
    btc_price = btc_data.get("bitcoin", {}).get("usd", 0)
    btc_change = btc_data.get("bitcoin", {}).get("usd_24h_change", 0)
    return btc_price, btc_change


def get_crypto_news():
    articles = []
    errors = []

    for source_name, feed_url in RSS_FEEDS:
        try:
            articles.extend(fetch_rss_items(source_name, feed_url, limit=4))
        except Exception as e:
            errors.append(f"{source_name}: {e}")

    articles = articles[:8]
    btc_price, btc_change = get_btc_price()

    lines = [
        "📰 加密货币新闻摘要",
        f"🪙 BTC: ${btc_price:,.0f} ({btc_change:+.2f}%/24h)",
        "",
        "最新新闻:",
    ]

    if not articles:
        lines.append("- 暂时没有抓到新闻源。")
    else:
        for i, article in enumerate(articles, 1):
            title = article.get("title", "")
            source = article.get("source", "N/A")
            lines.append(f"{i}. {title}")
            lines.append(f"   来源: {source}")

    if errors:
        lines.append("")
        lines.append("部分源抓取失败:")
        for err in errors:
            lines.append(f"- {err}")

    lines.append("")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


if __name__ == "__main__":
    print(get_crypto_news())
