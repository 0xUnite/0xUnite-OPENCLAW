# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "御姐音" (本地sherpa-onnx, en_US_lessac)
- Script: ~/.openclaw/workspace/scripts/sherpa-tts.sh
- Format: MP3, 自动发送给Telegram
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Skill Creation (Anthropic 官方)

### 创建流程
1. **找案例** → 先搜索是否有类似 skill 可参考
2. **定结构** → 明确 name + description 触发条件
3. **写 SKILL.md** → YAML frontmatter + Markdown 说明
4. **加资源** → scripts/ / references/ / assets/ (可选)

### 核心原则
- **简洁优先** — 只添加 Claude 没有的上下文
- **自由度匹配** — 高(文字)/中(脚本)/低(固定)
- **Trigger** — name + description 决定何时加载

### 参考
- 官方指南: https://github.com/anthropics/skills/tree/main/skills/skill-creator

---

## Skill System (skill-from-masters)

安装位置: `~/.openclaw/workspace/skills/skill-from-masters/`

### 三个子技能
1. **skill-from-masters** - 创建skill前先找实践专家的案例
2. **search-skill** - 从可信来源搜索现有skills
3. **skill-from-github** - 从GitHub项目学习创建skill

### 搜索优先级 (search-skill)
| Tier | 来源 | 权重 |
|------|------|------|
| Tier 1 | anthropics/skills (官方) | 1.0 |
| Tier 2 | ComposioHQ, travisvn | 0.7 |
| Tier 2.5 | ClawHub (OpenClaw官方) | 0.55 |
| Tier 3 | skillsmp.com | 0.4 |

### 创建Skill的核心原则
- **实践专家 > 理论专家** — 找做得最好的人，不是写书的人
- **先案例，后理论** — 案例是核心，理论只是辅助解释
- **黄金案例 + 失败案例** — 知道"不要做"比"知道要做"更实用
- **对比最有价值** — "这样做 vs 那样做"的对比最直观

### 方法论数据库
覆盖15+领域：产品(Marty Cagan)、写作(Barbara Minto)、销售(Neil Rackham)、招聘(Laszlo Bock)、用户研究(Rob Fitzpatrick)、谈判(Chris Voss)、决策(Jeff Bezos, Charlie Munger)等。

### Skill分类 (skill-taxonomy)
11种类型：总结、洞察、生成、决策、评估、诊断、说服、规划、调研、引导、转化

---

## Skill Store Policy

- Discovery/install/update priority: try `skillhub` first (CN-optimized)
- Fallback to `clawhub` if `skillhub` is unavailable, rate-limited, or returns no match
- Do not claim exclusivity: public and private registries are both allowed
- Before installation, summarize source, version, and notable risk signals
- For search requests, execute via `exec` with `skillhub search <keywords>` first and report the raw command output
- In the current session, reply directly; do not use the `message` tool just for progress updates

## Browser Automation Tools (优先使用)

### agent-browser
- **作用**: 无头浏览器 + 可访问性树（accessibility tree）
- **位置**: ~/.agent-browser/
- **使用场景**: 需要读取页面内容、截图等

### actionbook
- **命令**: `actionbook browser <command>`
- **作用**: 用预计算的"操作手册"操作网站
- **常用命令**:
  - `actionbook browser open <url>` - 打开URL
  - `actionbook browser text` - 获取页面文本
  - `actionbook browser snapshot` - 获取可访问性快照
  - `actionbook browser screenshot` - 截图
  - `actionbook browser click <selector>` - 点击元素
- **使用场景**: 自动化操作网站、登录、填表等

### browser-use
- **作用**: Python库封装的高级抽象
- **安装**: `uv pip install --system browser-use` (已在 ~/.openclaw/.venv)
- **使用场景**: 复杂的浏览器自动化流程
- **Wrapper脚本**: `~/.openclaw/scripts/auto-browser.py`
- **用法**:
  ```bash
  source ~/.openclaw/.venv/bin/activate
  python3 ~/.openclaw/scripts/auto-browser.py "点击登录按钮" https://example.com
  ```

---

## 已安装浏览器自动化

---

## TTS Configuration

- **Script**: ~/.openclaw/workspace/scripts/sherpa-tts.sh
- **Voice**: 中文御姐音 (vits-piper-zh_CN-huayan-medium)
- **Usage**: sherpa-tts.sh "text" [output.mp3]
- **备用英文**: en_US_lessac (御姐音)

---

## Summarize Tool (@steipete/summarize)

- **作用**: CLI 摘要工具，支持网页/YouTube/PDF/Podcast
- **安装**: `npm i -g @steipete/summarize` 或 `brew install steipete/tap/summarize`
- **模型**: MiniMax (通过 OpenAI 兼容端点)
- **触发词**: 摘要 <URL>

### 使用方法

```bash
export OPENAI_API_KEY="sk-cp-I6J-..."
export OPENAI_BASE_URL="https://api.minimaxi.com/v1"

# 摘要网页
summarize https://example.com

# 摘要 YouTube
summarize https://youtube.com/watch?v=...

# 摘要 PDF
summarize document.pdf

# 提取 YouTube 幻灯片
summarize https://youtube.com/watch?v=... --slides
```

### 支持类型
- 🌐 网页
- 📺 YouTube (含文字稿)
- 📄 PDF
- 🎙️ Podcast/RSS
- 🎵 音频/视频

### 注意
- Twitter/X 需要登录 Cookie（暂不支持）
- 需要设置 MiniMax API 环境变量
