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
| Fortytwo | ⚠️ 服务在线但接口层异常 | 终端余额约717~717.5；join/ranking与token、available、JSON解析问题反复出现 |
| Binance AI Assistant | ⏸️ 比赛期已过 | 保留仓库与成果 |
| Binance Square Auto-Post | ✅ 已确认正常 | 晚间21:00 KST发帖成功；格式确认，2026-03-30起早间10:00 KST开始 |
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
- daily-automation.sh 路径错误排查
- pending-notification.txt 生成链路确认

## 持续性BUG/问题（未解决）
| 问题 | 状态 | 说明 |
|------|------|------|
| auto-memory-runner 检查点 LLM 失败 | ⚠️ 持续数周 | API问题，无明确修复方案 |
| total-recall-observer 超时 | ⚠️ ~50%失败率 | 内部timeout问题 |
| Fortytwo 接口字段/JSON解析错误 | ⚠️ 持续 | 心跳脚本层不稳定，非服务宕机 |
| crypto-daily-briefing 超时 | ⚠️ 本周新增 | 脚本超时~98s，建议增大timeout到300s |
| cron job 模型验证失败 | ⚠️ 本周新增 | 多个job指定了不允许的model字段(MiniMax-M2.5/gemini-2.5-flash)，建议移除model字段 |
| clawdhub registry 空JSON | 🆕 本周 | 10+ skills无法通过clawdhub更新（registry bug） |
| Gateway 长时间离线 | 🔴 本周重大 | 2026-03-24 14:00~22:00 KST Gateway超时，需监控是否复发 |

## 最近稳定结论
- Fortytwo 最近的主要问题不是"服务挂了"，而是 **心跳脚本 / 接口字段 / JSON解析层不稳定**。
- Nexus 本周稳定，12节点持续在线；自动重启与状态巡检都在正常跑。
- 自动记忆、微同步、状态播报这套日常运维链路整体可用。
- Binance Square 早间发帖从2026-03-30开始正式运行（10:00 KST）。
- Gateway 3/24曾发生约8小时离线，需关注复发。

## 决策 / 偏好模式
- 运维判断上，先区分"核心服务故障"还是"脚本/接口层故障"，别一上来就按宕机处理。
- Git/备份上，强烈偏好先防大文件进历史：先配 `.gitignore`，再下载/生成大二进制。
- 处理异常时，优先保留可恢复路径，避免为了修一个问题把历史和备份一起炸掉。

## 重要教训
- 2026-03-21: Git push 失败根因是 patchright driver (105MB) 进入历史；处理方式为 reset 到 origin/main、补 `.gitignore`、只 cherry-pick 必要提交。教训：**大二进制别进 Git 历史**。
- 2026-03-21~22: Fortytwo 多次显示服务在线，但心跳层反复报 `access_token`、`refresh_token`、`available`、JSON parse 等错误。教训：**这类情况优先查脚本/接口字段变化，不要误判为服务宕机**。
- 2026-03-21: `daily-automation.sh` 未找到，属于路径配置问题，不是业务异常。
- 2026-03-17: CDP浏览器超时问题 - OpenClaw browser + browser-use 均有兼容性问题。
- 2026-03-16: A股监控使用腾讯财经API (`qt.gtimg.cn`)。
- 2026-03-15: 浏览器操作最佳实践 - 使用稳定 profile + targetId。

## AI / 行业观察（本周）
- Ginkgo Bioworks CEO: AI模型控制机器人实验室6轮迭代后超SOTA 40%，"生物学Waymo时刻"
- Andrej Karpathy: LLM记忆功能反而是干扰——会过度拟合上下文中的信息
- Box CEO Aaron Levie: Jevons悖论 - AI降低软件生产成本后，更多企业开始有能力承接软件项目
- Matt Turck: VC角色演变 - 2016治理指导 → 2021啦啦队 → 2026成为Anthropic/OpenAI销售代表
- OpenClaw新维护者@izhukov加入，负责Telegram支持，首要修复bot streaming API消息重复问题
- Claude session limits调整（工作日5-11am PT影响约7% Pro用户）

## 已安装 Skills
| Skill | 版本/备注 |
|-------|-----------|
| proactive-agent | 主动模式 |
| automation-workflows | 自动化工作流 |
| auto-updater | 自动更新 |
| daily-stock-analysis | 股票分析 |
| okx-trade-mcp | OKX 交易/链上相关 |
| x-tweet-fetcher | Twitter获取 |
| actionbook | 浏览器自动化 |
| browser-use | 0.12.2（官方最新0.12.3待pipx同步）|
| slowmist-agent-security | 🆕 本周安装 |

## 工具配置
- 浏览器: OpenClaw内置
- TTS: sherpa-onnx (御姐音)
- 搜索: skillhub优先，失败则clawhub

## 自动化任务（本周状态）
- nexus-auto-restart: ✅ 正常运行
- fortytwo-heartbeat: ✅ 正常运行（接口层警告可忽略）
- notification-check: ✅ 正常运行
- binance-square-morning: ✅ 正常运行（2026-03-30起10:00 KST）
- binance-square-evening: ✅ 正常运行（21:00 KST）
- auto-memory-runner: ⚠️ 检查点LLM持续失败
- total-recall-observer: ⚠️ 超时失败率高
- crypto-daily-briefing: ⚠️ 超时偶发
- Daily Auto-Update: ✅ 正常运行
- AI Builders Digest: ✅ 正常运行（本周已优化prompts，增加解读深度）
- status-report-2h: ✅ 正常运行

## ClawHub 镜像站 (2026-04-01)
- **Mirror**: https://mirror-cn.clawhub.com
- **用途**: 国内加速搜索/安装 OpenClaw Skills
- **命令**: 
  ```bash
  clawhub search "关键词" --registry https://mirror-cn.clawhub.com
  clawhub install <slug> --registry https://mirror-cn.clawhub.com
  ```
- **已验证**: 可用，搜索 AI/Agent 相关技能正常

## 今日新增能力 (2026-04-01)
- ✅ MiniMax TokenPlan 多模态 (视频/音乐/语音/图片生成)
- ✅ mlx-whisper (本地语音转文字，Mac优化)
- ⚠️ 语音输入 - Mac mini无麦克风，需外接设备
