# 0xUnite OpenCLAW 记忆库

> 个人 AI 助手 OpenClaw 的功能记忆库

---

## 概述

本仓库用于记录 OpenClaw AI 助手已配置的功能、技能、项目，避免重复造轮子。

---

## 核心项目

| 项目 | 状态 | 描述 |
|------|------|------|
| KoreaRealEstate | ✅ | 韩国租房网站 (端口3000+Cloudflare) |
| Nexus | ✅ | 6节点运行中 |
| Fortytwo | ✅ | AI Agent (余额717.5 Energy) |
| binance-ai-assistant | ✅ | 币安AI交易助手 |
| okx-onchain-assistant | ✅ | OKX OnchainOS AI 助手 (参赛作品) |

---

## 已安装 Skills

| Skill | 功能 |
|-------|------|
| fortytwo | AI Agent |
| moltbook | MOLT代币 |
| google-calendar | 日历管理 |
| reminder | 提醒功能 |
| square-post | Binance Square 发帖 |
| x-publish | X (Twitter) 发帖 |
| x-tweet-fetcher | X 推文获取 |
| onchainos-skills | OKX 链上技能 |

---

## 常用脚本

| 脚本 | 功能 |
|------|------|
| `~/.openclaw/scripts/binance_v3.py` | 币安v3交易 |
| `~/.openclaw/scripts/all-monitor.sh` | 监控脚本 |
| `~/.openclaw/scripts/sherpa-tts.sh` | TTS语音 |

---

## 工具配置

- **TTS**: sherpa-onnx, 御姐音 (en_US_lessac)
- **Browser**: Chrome extension relay + OpenClaw browser
- **社交**: Agent Reach (抖音, 小红书)

---

## API 配置

- **OpenClaw**: http://127.0.0.1:8080
- **模型**: anthropic/MiniMax-M2.5

---

## 更新日志

### 2026-03-08
- 新增 OKX OnchainOS AI 参赛作品
- 参赛作品: https://github.com/0xUnite/okx-onchain-assistant
