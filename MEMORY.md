# MEMORY.md - 精简版

## 关于 User
- 名字: 0xUnite
- 身份: 管理学博士生 (AI服务失误研究方向)
- 时区: Asia/Seoul (GMT+9)

## 核心项目
| 项目 | 状态 | 备注 |
|------|------|------|
| KoreaRealEstate网站 | ✅ 运行中 | 端口3000+Cloudflare |
| Nexus | ✅ 6节点运行中 | |
| Fortytwo | ⚠️ 运行但API异常 | 余额717.5 Energy |
| OKX OnchainOS AI | 🔥 开发中 | 截止3/11 23:59 |
| Binance AI Assistant | 🔥 开发中 | 截止3/18 |

## 已停止项目 (2026-03-06)
- Simmer V2 - 已禁用 (交易策略优化后仍有问题)
- WTT 模拟盘 - 已禁用
- MOLT Mint - 已禁用
- binance_arb_scanner - 已停止
- binance_v3 - 已停止

## 待办事项 (Active TODOs)
- OKX OnchainOS AI Hackathon - 截止2026-03-11 23:59
- 0xUnite Twitter账号运营
- MiniMax API余额问题排查
- Fortytwo "Insufficient funds" API问题排查

## 教训
- Simmer旧策略: 买Bitcoin高价，胜率18%，亏损$998
- 优化: 只买低概率(yes<15% 或 yes>85%)
- MOLT API变更: moltbook.com移除submolt/tags，改用submolt_name字段
- MiniMax API余额问题: 导致Weekly Memory Compound、自动记忆检查点失败
- Fortytwo API问题: 717.5 Energy但Join Query报"Insufficient funds"

## 更新日志
- 2026-03-11: Skills Store policy 更新 — skills discovery/install/update 优先 `skillhub`，失败/限流/无结果再 fallback `clawhub`；安装前需总结 source、version、risk signals；搜索请求先执行 `skillhub search <keywords>` 并报告原始输出
- 2026-03-10: github-trending-cn skill安装成功
- 2026-03-09: ADB手机控制已配置 (scrcpy可用)
- 2026-03-08: OKX OnchainOS参赛作品开发中 (截止3/11)
- 2026-03-06: binance-ai-assistant升级v4.7 - 改用OpenClaw AI
- 2026-03-06: 批量项目停止: Simmer V2, WTT模拟盘, MOLT Mint
- 2026-02-18: MOLT API修复 (submolt_name字段)，添加速率限制处理
- 2026-02-17: 添加Simmer V2策略，修复任务追踪

## 已安装Skills (2026-02-17)
- fortytwo: AI Agent (2026-02-18 更新为 idle 模式)
- moltbook: MOLT代币
- google-calendar: 日历管理 (新安装)
- reminder: 提醒功能 (新创建)

## Agent Reach 社交媒体集成 (2026-03-06)
- 安装位置: ~/.agent-reach/
- 抖音 MCP: localhost:18070
- 小红书: 使用 redbook CLI (npm)，需要 Chrome 登录后 `redbook whoami` 授权
- LinkedIn/Boss直聘: 暂未配置（需手动浏览器登录）

## OKX OnchainOS 参赛作品 (2026-03-08)
- GitHub: https://github.com/0xUnite/okx-onchain-assistant
- 版本: v2.1 (持续更新中)
- 功能: 钱包+新币扫描+合约审计+Gas预测+聪明钱雷达+Holder分析+池子分析+交易机器人
- 截止日期: 2026-03-11 23:59

## 参赛作品文案风格 (2026-03-08)
- 第一人称 AI 视角
- 情感化叙事（有自己的名字、个性）
- 真实使用场景 + 具体命令提示词
- 真实成果/成就
- 时间线成长记录
- 参考: https://x.com/0X0CLOWN/status/2029445310989386127

## Binance 参赛作品 (2026-03-06)
- GitHub: https://github.com/0xUnite/binance-ai-assistant
- 版本: v4.3 (持续更新中)
- 功能: Web仪表盘+Telegram Bot+技术分析+巨鲸追踪+多链热点+Honeypot检测+策略回测+模拟交易+共同账户+社交跟单
- 截止日期: 2026-03-18

## Fortytwo 质量优先模式 (2026-02-18)
- 信心度 <70% 跳过
- 不确定问题跳过
- 答案太短跳过
- 每10分钟检查

## 手机ADB控制 (2026-03-09)
- USB调试连接Mac成功
- scrcpy 可实时显示手机画面
- ADB可截图、点击、输入英文
- 问题: Android 16 上 `adb shell input text` 有兼容性问题，中文输入困难
- 已安装 ADB Keyboard 但仍有bug
- 方案: Twitter Intent 分享、手机端备忘录手动复制

## BUG (2026-03-13)
- WIN 触发器未生效: 用户说 'WIN 优化浏览器' 时 MiniMax 直接回答，未 spawn GPT-5.4 子任务
- 需要在收到消息时先检测 WIN/GO 模式，再决定用哪个模型
