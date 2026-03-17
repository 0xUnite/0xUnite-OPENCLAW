# MEMORY.md - 精简版

## 关于布布大王
- 名字: 布布大王
- 身份: 管理学博士生 (AI服务失误研究方向)
- 时区: Asia/Seoul (GMT+9)
- 沟通风格: 简洁直接，追问时详细解释
- 实时沟通 (0-8点外)，凌晨勿扰
- 踩坑: 必须做好备份，防止数据丢失
- 目标: 通过合作实现睡后收入，躺平生活

## 核心项目
| 项目 | 状态 | 备注 |
|------|------|------|
| Nexus | ✅ 12节点运行中 | 2026年3月从6节点扩展 |
| KoreaRealEstate网站 | ✅ 运行中 | 端口3000+Cloudflare |
| Fortytwo | ⚠️ 运行但API异常 | 717.5 Energy, join报Insufficient funds |
| OKX OnchainOS AI | ✅ 已提交 | 截止3/11 23:59 |
| Binance AI Assistant | 🔥 开发中 | 截止3/18 |
| 600589大位科技 | 📈 监控中 | 今日收盘10.71 (0.00%) |

## 已停止项目
- Simmer V2 - 已禁用 (交易策略优化后仍有问题)
- WTT 模拟盘 - 已禁用
- MOLT Mint - 已禁用
- binance_arb_scanner - 已停止
- binance_v3 - 已停止

## 待办事项
- 0xUnite Twitter账号运营
- MiniMax API余额问题排查
- Fortytwo "Insufficient funds" API问题排查
- OKX API Key配置 (新API)

## 教训
- 2026-03-17: CDP浏览器超时问题 - OpenClaw browser + browser-use均有兼容性问题
- 2026-03-16: A股监控使用腾讯财经API (qt.gtimg.cn)
- 2026-03-16: Onboarding完成 - 布布大王12个问题已回答
- 2026-03-16: 主动模式(proactive-agent)已启用
- 2026-03-16: daily-stock-analysis skill安装
- 2026-03-16: okx-trade-mcp/cli安装 (需配置API Key)
- 2026-03-16: 股票分时监控脚本创建 (600589, 9:30-10:00, 14:30-14:50)
- 2026-03-15: 浏览器操作最佳实践 - 使用 profile="openclaw" + targetId
- 2026-03-13: WIN/GEM 触发器不会自动执行 - 需要手动spawn
- 2026-03-13: Gemini 模型名确认: gemini-3.1-pro-preview
- 2026-03-13: x-tweet-fetcher安装 - 推文获取工具(免费)
- 2026-02-18: Fortytwo质量优先模式 - 信心度<70%跳过

## 已安装Skills
| Skill | 用途 |
|-------|------|
| proactive-agent | 主动模式 |
| automation-workflows | 自动化工作流 |
| auto-updater | 自动更新 |
| daily-stock-analysis | 股票分析 |
| okx-trade-mcp | 币安交易 |
| x-tweet-fetcher | Twitter获取 |
| actionbook | 浏览器自动化 |
| browser-use | 浏览器自动化 |

## 工具配置
- 浏览器: OpenClaw内置 (profile="openclaw")
- TTS: sherpa-onnx (御姐音)
- 搜索: skillhub优先，失败则clawhub

## 参赛作品
### Binance AI Assistant
- GitHub: https://github.com/0xUnite/binance-ai-assistant
- 功能: Web仪表盘+Telegram Bot+技术分析+巨鲸追踪+多链热点+Honeypot检测+策略回测+模拟交易+共同账户+社交跟单
- 截止: 2026-03-18

### OKX OnchainOS AI
- GitHub: https://github.com/0xUnite/okx-onchain-assistant
- 功能: 钱包+新币扫描+合约审计+Gas预测+聪明钱雷达+Holder分析+池子分析+交易机器人
- 截止: 2026-03-11

## 自动化任务
- daily-automation.sh: 每日9:00, 21:00运行
- stock-monitor: A股分时监控 (600589)
- 股票报告: memory/stock-monitor/reports/

## BUG/问题
- CDP超时: OpenClaw浏览器不稳定
- Python 3.14: browser-use不兼容
- Fortytwo API: Insufficient funds错误
