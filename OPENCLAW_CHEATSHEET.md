# OpenClaw Mega Cheatsheet - 完整指令参考

> 2026-02-10学习 | 来源: moltfounders.com/openclaw-mega-cheatsheet

## 🚀 快速开始

```bash
# 全局安装
npm install -g openclaw@latest

# 引导设置
openclaw onboard --install-daemon

# 通道登录
openclaw channels login

# 启动网关
openclaw gateway --port 18789

# Onboard flags
openclaw onboard --mode local        # 本地网关模式
openclaw onboard --mode remote      # 远程网关
openclaw onboard --flow quickstart # 最小化设置
openclaw onboard --skip-channels   # 跳过通道设置
```

## 💬 通道设置

```bash
# 登录所有通道
openclaw channels login

# WhatsApp - QR扫码登录

# Telegram
channels add --channel telegram --token $TOKEN

# Discord
channels add --channel discord --token $TOKEN

# iMessage (macOS原生)
# macOS bridge

# Slack
channels add --channel slack --token $TOKEN

# Google Chat
channels add --channel googlechat --service-account $FILE

# Signal
channels add --channel signal --linked-device $DEVICE

# MS Teams
channels add --channel msteams --app-registry $ID

# 快速诊断
openclaw channels status --probe          # 状态检查
openclaw channels logs --channel [id]    # 通道日志
```

## 📁 工作区文件

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | Agent操作说明 |
| `SOUL.md` | Persona、语气、边界 |
| `USER.md` | 用户信息与偏好 |
| `IDENTITY.md` | Agent名称、emoji、主题 |
| `MEMORY.md` | 长期记忆 (仅DM会话加载) |
| `memory/YYYY-MM-DD.md` | 每日追加日志 |
| `TOOLS.md` | 本地工具笔记 |
| `HEARTBEAT.md` |心跳检查清单 |
| `BOOT.md` | 启动检查清单 |

**根目录**: `~/.openclaw/workspace`

## 🧠 记忆系统

```bash
# 每日日志: memory/YYYY-MM-DD.md
# - 追加写入
# - 会话开始时读取今天+昨天

# 长期记忆: MEMORY.md
# - 仅在主DM会话加载
# - 精心整理的事实

# 向量搜索
openclaw memory search "查询内容"    # 语义搜索 (~400 tokens块)

# 重新索引
openclaw memory index --all
```

### 记忆提供商配置
```json
{
  "memorySearch.provider": "auto",  // 自动选择: local GGUF → OpenAI → Gemini → Voyage
  "memory.backend": "qmd",           // BM25 + 向量 + 重排序
  "hybridSearch.weights": [0.7, 0.3]  // 向量相似度 + BM25关键词
}
```

## 🤖 模型与认证

```bash
# 列出所有模型
openclaw models list --all

# 设置默认模型
openclaw models set <model>                    # 主要模型
openclaw models set-image <model>             # 图像模型
openclaw models fallbacks add <model>         # 添加回退链

# 认证设置
openclaw models auth setup-token               # 首选Anthropic认证 (OAuth)
openclaw models auth add --provider <p>       # 添加提供商API key
openclaw models status --probe                # 实时探测认证状态

# 别名
openclaw models aliases add <alias> <model>   # 创建模型别名
```

### 回退与冷却
| 层级 | 冷却时间 |
|------|---------|
| 第1次回退 | 1 min |
| 第2次回退 | 5 min |
| 第3次回退 | 1 hour |

## 🔐 会话管理

```bash
# 会话范围配置
session.dm: "main"                    # main | per-peer | per-channel-peer | per-account-channel-peer
session.reset.mode: "daily"            # daily (默认4am) | idle
session.reset.idleMinutes: 60          # 滑动空闲窗口

# 重置策略
session.resetByType: {dm, group, thread}  # 覆盖策略
session.resetByChannel: {channel: policy} # 每个通道覆盖
session.identityLinks: {provider:id → canonical}  # 跨通道身份映射
session.sendPolicy: {session: block}      # 阻止特定会话类型发送

# 存储位置
~/.openclaw/agents/{agentId}/sessions/sessions.json

# ⚠️ 多用户收件箱使用 per-channel-peer 防止上下文泄漏
```

## ⚡ 斜杠命令

| 命令 | 功能 |
|------|------|
| `/status` | 会话健康+上下文使用+WhatsApp凭据 |
| `/context list` | 上下文窗口内容 (最大贡献者) |
| `/context detail` | 完整系统提示+注入的工作区文件 |
| `/model <model>` | 切换模型 (或 `/model list` 列表) |
| `/compact [instructions]` | 总结旧上下文，释放窗口空间 |
| `/new [model]` | 全新会话 (可选设置模型) |
| `/reset` | `/new` 的别名 |
| `/stop` | 中止当前运行+清除排队后续 |
| `/send on\|off\|inherit` | 覆盖此会话的传递设置 |
| `/tts on\|off` | 切换文本转语音 |
| `/think\|/verbose` | 切换推理/详细模式 |
| `/config` | 持久化配置更改 |
| `/debug` | 运行时配置覆盖 (需要 commands.debug: true) |

## 🔊 文本转语音

| 提供商 | 特点 |
|--------|------|
| ElevenLabs | 超真实，高延迟 |
| OpenAI | 快速，高质量 |
| Edge TTS | 免费，多语言支持 |

```json
{
  "messages.tts.auto": "always"  // 启用自动TTS
}
```

## 📊 日志与诊断

```bash
# 网关日志
openclaw logs --follow              # 尾随网关文件日志 (TTY着色)
openclaw logs --json                # 行分隔JSON (每行一个事件)
openclaw logs --limit 200           # 限制日志行数
openclaw channels logs --channel whatsapp  # 特定通道日志

# OTel导出
{
  "diagnostics": {
    "otel": { "enabled": true }
  }
}
```

## 🌐 浏览器与Cron

### 浏览器操作
```bash
openclaw browser start|stop        # 启动/停止无头实例
openclaw browser tabs              # 列出所有打开的页面
openclaw browser open <url>        # 新标签页打开URL
openclaw browser screenshot        # 捕获当前视图
openclaw browser navigate <url>    # 导航当前标签页
openclaw browser click|type|press # DOM交互
openclaw browser evaluate <js>     # 在页面运行JavaScript
openclaw browser pdf               # 导出页面为PDF
```

### Cron任务
```bash
openclaw cron list                 # 查看计划任务
openclaw cron add                  # 创建新任务
openclaw cron edit <id>            # 编辑现有任务
openclaw cron enable|disable <id>  # 切换任务
openclaw cron run <id>             # 手动触发
openclaw cron runs                 # 查看运行历史
```

## 🔗 钩子与自动化

### 内置钩子
| 钩子 | 命令 | 功能 |
|------|------|------|
| session-memory | command:new | /new时保存会话上下文到记忆 |
| command-logger | command | 将所有命令记录到审计文件 |
| boot-md | gateway:startup | 网关启动时运行BOOT.md |
| soul-evil | agent:bootstrap | 清窗口期间交换SOUL.md |

```bash
openclaw hooks list                 # 列出所有发现的钩子
openclaw hooks enable <name>       # 启用钩子
openclaw hooks disable <name>      # 禁用钩子
openclaw hooks info <name>         # 显示钩子详情
openclaw hooks check               # 检查资格
```

### 事件类型
- `command:new` - 发出/new时
- `command:reset` - 发出/reset时
- `command:stop` - 发出/stop时
- `gateway:startup` - 通道启动后
- `agent:bootstrap` - 注入工作区文件前

## 🧩 技能系统

### 技能优先级
1. `<workspace>/skills/` - 每个Agent，最高优先级
2. `~/.openclaw/skills/` - 托管/本地，跨工作区共享
3. 内置技能 - 随OpenClaw发货 (最低)

### ClawHub
```bash
clawhub install <slug>              # 从ClawHub安装技能
clawhub update --all               # 更新所有已安装技能
clawhub sync --all                 # 扫描并发布更新
```

### SKILL.md格式
```yaml
---
name: my-skill
description: "这个技能做什么"
metadata:
  openclaw:
    requires: {...}
---
```

## 👥 多Agent路由

### 隔离工作区
- 每个Agent有独立的AGENTS.md, SOUL.md, USER.md
- 每个Agent独立认证
- 聊天历史存储在 `~/.openclaw/agents/<id>/sessions`

### 路由优先级
1. `peer` - 精确DM/群组ID (最高)
2. `guildId` - Discord公会级
3. `teamId` - Slack团队级
4. `accountId` - 账户级
5. `channel` - 通道范围回退
6. `default` - 最终回退 (默认Agent)

```bash
openclaw agents add <name>
openclaw agents list --bindings
```

## 💓 心跳系统

```yaml
heartbeat:
  every: "30m"                     # 间隔 (Anthropic OAuth默认1h)
  target: "last"                   # last | none | <channel id>
  to: Optionalrecipient           # 可选的收件人覆盖
  model: Modeloverride            # 心跳运行的模型覆盖
  prompt: Custompromptbody        # 自定义提示主体
  activeHours:
    start: "09:00"
    end: "22:00"
    timezone: "Asia/Seoul"
```

**合同**: 回复 `HEARTBEAT_OK` 如果没有需要关注的事项。Agent会剥离并丢弃仅OK的回复。

## 🔐 沙箱

```yaml
sandbox:
  mode: "non-main"                # off | non-main (默认) | all
  scope: "session"                # session (默认) | agent | shared
  workspaceAccess: "none"         # none | ro | rw
```

### 设置镜像
```bash
scripts/sandbox-setup.sh
# 默认镜像: openclaw-sandbox:bookworm-slim
```

## 🎯 子Agent

```bash
/subagents list                   # 列出活动的子Agent
/subagents stop <id|#|all>        # 停止子Agent运行
/subagents log <id|#>             # 查看子Agent日志
/subagents info <id|#>            # 显示运行元数据
/subagents send <id|#> <msg>      # 发送消息到子Agent

# sessions_spawn工具
{
  task: "任务描述",
  label?: "标签",
  model?: "模型",
  thinking?: "推理模式",
  runTimeoutSeconds?: 600,
  cleanup?: "delete"
}
# 返回: { status, runId, childSessionKey }
```

## 🔧 故障排除

| 问题 | 解决方案 |
|------|---------|
| 无DM回复 | `openclaw pairing list` → 批准待处理请求 |
| 群组沉默 | 检查 mentionPatterns 配置 (需要@提及) |
| 认证过期 | `openclaw models auth setup-token --provider anthropic` |
| 网关宕机 | `openclaw doctor --deep` (扫描额外安装) |
| 记忆未索引 | `openclaw memory index` (重新索引记忆文件) |
| 上下文满 | `/compact` 或 `/new` (开始全新会话) |
| 通道断开 | `openclaw channels status --probe` |
| 会话问题 | `openclaw reset --scope sessions` |

**万能修复命令**:
```bash
openclaw doctor --deep --yes
# 健康检查 + 快速修复 + 系统服务扫描
```

## 📂 关键路径

| 路径 | 用途 |
|------|------|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/workspace/` | 默认Agent工作区 |
| `~/.openclaw/agents/<id>/` | 每个Agent状态目录 |
| `~/.openclaw/agents/<id>/sessions/` | 会话存储+转录 |
| `~/.openclaw/credentials/` | OAuth/API密钥 |
| `~/.openclaw/memory/<agentId>.sqlite` | 向量索引存储 |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | 网关日志文件 |

**提示**: 使用 `--dev` 或 `--profile <name>` 在不同目录下隔离状态。

---

*最后更新: 2026-02-10*
*来源: moltfounders.com/openclaw-mega-cheatsheet*
