# Skills 清单

## 已安装 Skills (按字母排序)

### 官方 Skills
- `fortytwo` - AI Agent
- `google-calendar` - 日历管理
- `moltbook` - MOLT代币
- `reminder` - 提醒功能

### 社区 Skills
- `onchainos-skills` - OKX 链上技能
- `square-post` - Binance Square 发帖
- `x-publish` - X 发帖
- `x-tweet-fetcher` - X 推文获取
- `x-collect` - X 数据收集
- `x-create` - X 内容创建
- `x-filter` - X 内容过滤

---

## Skill 创建指南

参考: https://github.com/anthropics/skills/tree/main/skills/skill-creator

### 创建流程
1. 找案例 → 先搜索是否有类似 skill
2. 定结构 → 明确 name + description 触发条件
3. 写 SKILL.md → YAML frontmatter + Markdown 说明

### 技能来源优先级
| Tier | 来源 | 权重 |
|------|------|------|
| Tier 1 | anthropics/skills (官方) | 1.0 |
| Tier 2 | ComposioHQ, travisvn | 0.7 |
| Tier 2.5 | ClawHub (OpenClaw官方) | 0.55 |
| Tier 3 | skillsmp.com | 0.4 |

---

## 自定义 Skills 位置

- `~/.openclaw/skills/` - 官方安装
- `~/.openclaw/workspace/skills/` - 工作区技能
- `~/.openclaw/workspace/.claude/skills/` - Claude 技能
-  - BNB Chain MCP (区块/交易/合约/Token/NFT/钱包/ERC-8004/Greenfield)
