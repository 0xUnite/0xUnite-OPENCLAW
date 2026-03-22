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
| Nexus | ✅ 12节点运行中 | 本周持续健康，自动重启链路正常 |
| KoreaRealEstate网站 | ✅ 运行中 | 端口3000 + Cloudflare |
| Fortytwo | ⚠️ 服务在线但接口层异常 | 终端余额约717~717.5；join/ranking与token、available、JSON解析问题反复出现，更像脚本/接口兼容问题 |
| Binance AI Assistant | ⏸️ 比赛期已过 | 保留仓库与成果，后续按产品化价值决定是否继续 |
| 600589大位科技 | 📈 监控中 | 继续观察 |

## 已停止 / 已过期项目
- Simmer V2 - 已禁用
- WTT 模拟盘 - 已禁用
- MOLT Mint - 已禁用
- binance_arb_scanner - 已停止
- binance_v3 - 已停止
- OKX OnchainOS AI - 已提交，比赛截止已过

## 当前关注点
- 0xUnite Twitter账号运营
- MiniMax API余额问题排查
- Fortytwo 心跳/接口脚本修复（token、available、JSON解析、Not Found）
- OKX API Key配置（新API）
- daily-automation.sh 路径错误排查
- pending-notification.txt 生成链路确认

## 最近稳定结论
- Fortytwo 最近的主要问题不是“服务挂了”，而是 **心跳脚本 / 接口字段 / JSON解析层不稳定**。
- Nexus 本周稳定，12节点持续在线；自动重启与状态巡检都在正常跑。
- 自动记忆、微同步、状态播报这套日常运维链路整体可用。
- Gateway 通知检查多次显示没有待处理告警，但要确认是“确实无告警”还是“通知文件没生成”。

## 决策 / 偏好模式
- 运维判断上，先区分“核心服务故障”还是“脚本/接口层故障”，别一上来就按宕机处理。
- Git/备份上，强烈偏好先防大文件进历史：先配 `.gitignore`，再下载/生成大二进制。
- 处理异常时，优先保留可恢复路径，避免为了修一个问题把历史和备份一起炸掉。

## 重要教训
- 2026-03-21: Git push 失败根因是 patchright driver (105MB) 进入历史；处理方式为 reset 到 origin/main、补 `.gitignore`、只 cherry-pick 必要提交。教训：**大二进制别进 Git 历史**。
- 2026-03-21~22: Fortytwo 多次显示服务在线，但心跳层反复报 `access_token`、`refresh_token`、`available`、JSON parse 等错误。教训：**这类情况优先查脚本/接口字段变化，不要误判为服务宕机**。
- 2026-03-21: `daily-automation.sh` 未找到，属于路径配置问题，不是业务异常。
- 2026-03-17: CDP浏览器超时问题 - OpenClaw browser + browser-use 均有兼容性问题。
- 2026-03-16: A股监控使用腾讯财经API (`qt.gtimg.cn`)。
- 2026-03-15: 浏览器操作最佳实践 - 使用稳定 profile + targetId。

## 已安装 Skills
| Skill | 用途 |
|-------|------|
| proactive-agent | 主动模式 |
| automation-workflows | 自动化工作流 |
| auto-updater | 自动更新 |
| daily-stock-analysis | 股票分析 |
| okx-trade-mcp | OKX 交易/链上相关 |
| x-tweet-fetcher | Twitter获取 |
| actionbook | 浏览器自动化 |
| browser-use | 浏览器自动化 |

## 工具配置
- 浏览器: OpenClaw内置
- TTS: sherpa-onnx (御姐音)
- 搜索: skillhub优先，失败则clawhub

## 自动化任务
- daily-automation.sh: 计划存在，但当前发现路径错误，需修正
- stock-monitor: A股分时监控 (600589)
- 股票报告: memory/stock-monitor/reports/
- auto-memory-runner: 正常运行
- nexus-auto-restart: 正常运行
- notification-check: 正常运行，但需确认通知文件生成链路

## BUG / 问题
- CDP超时: OpenClaw浏览器不稳定
- Python 3.14: browser-use 不兼容
- Fortytwo API / heartbeat: token / available / JSON 解析 / Not Found 错误反复出现
- GitHub 大文件限制: 历史中混入 >100MB 文件会阻断 push
