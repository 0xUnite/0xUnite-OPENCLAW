# 🎉 OpenClaw 可用功能汇总

## ✅ 已安装的功能（16个）

### 📝 笔记管理
- **Apple Notes** - 用 `memo` CLI 管理苹果笔记
- **Bear Notes** - Bear 笔记管理
- **Obsidian** - Obsidian 笔记库管理

### ✅ 待办管理
- **Apple Reminders** - 苹果提醒事项
- **Things 3** - Things 3 待办管理

### 💬 消息
- **Telegram** - ✅ 已配置（你在用）
- **iMessage** - ⚪ 未安装（需要额外配置）
- **WhatsApp** - ⚪ 未安装（需要手机配对）

### 📧 邮件
- **Himalaya** - CLI 邮件管理（已安装）

### 🔧 开发工具
- **coding-agent** - Claude Code / Codex 编程助手（已配置）
- **GitHub** - GitHub CLI 管理
- **healthcheck** - 系统安全检查
- **skill-auto-iteration** - 🔥 自动学习系统（刚创建）

### 📰 监控
- **blogwatcher** - RSS 订阅监控（已配置加密货币）
- **tavily-search** - AI 优化搜索

### 🔍 研究
- **find-skills** - 查找和安装新 Skills
- **proactive-agent** - 主动式 AI 助手

---

## 🔧 可以安装的功能（推荐）

### 🔊 语音合成（TTS）
**用途**：文本转语音，生成播客

**安装命令**：
```bash
# ElevenLabs（高质量，需要 API Key）
brew install elevenlabs-cli

# 或 OpenAI TTS（内置）
# 直接使用 OpenClaw 的 messages.tts 配置
```

**配置**：
在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "messages": {
    "tts": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "apiKey": "你的API Key",
        "voiceId": "21m00Tcm4TlvDq8ikWAM"
      }
    }
  }
}
```

---

### 🎙️ 语音转文字（Whisper）
**用途**：音频转文字、会议纪要

**安装**：
```bash
brew install openai-whisper
# 或
pip install openai-whisper
```

---

### 🏠 智能家居（Home Assistant）
**用途**：控制智能灯泡、空调等

**安装**：
```bash
brew install homeassistant/homeassistant/homeassistant-cli
```

**配置**：
需要 Home Assistant 的访问令牌。

---

### 📞 语音通话（Voice Call）
**用途**：AI 自动打电话

**安装**：
```bash
openclaw plugins install @openclaw/voice-call
```

**支持的提供商**：
- Twilio
- Telnyx
- Plivo

**配置**：
在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "accountSid": "你的 SID",
          "authToken": "你的 Token"
        }
      }
    }
  }
}
```

---

### 🔐 密码管理（1Password）
**用途**：安全存储和检索 API Keys

**安装**：
```bash
brew install 1password-cli
op account signin
```

---

### 💻 远程控制
**用途**：从手机控制电脑

**已配置**：
- ✅ Telegram（你在用）
- ⚪ Tailscale（明天配置）

**Tailscale 配置**（明天做）：
```bash
brew install tailscale
sudo tailscale up
```

---

## 🎯 推荐安装优先级

| 优先级 | 功能 | 原因 |
|-------|------|------|
| **1** | Tailscale | 远程控制 Chrome |
| **2** | RSS + Twitter | 自动发布（明天做）|
| **3** | Voice Call | AI 打电话 |
| **4** | Whisper | 语音转文字 |
| **5** | Home Assistant | 智能家居控制 |

---

## 📚 使用示例

### 发送提醒
```
"Hey OpenClaw，提醒我明天 10 点开会"
```

### 管理笔记
```
"在 Apple Notes 中创建笔记：..."
```

### 监控加密货币
```
"查看今天 BTC 价格"
```

### 编程任务
```
"用 Claude Code 创建一个 Python 脚本"
```

### 发送消息
```
"给张三发 iMessage：..."
```

### 健康检查
```
"检查系统安全性"
```

---

## 🔜 下次配置

### 明天12点：
1. **Tailscale** - 远程控制
2. **RSS + Twitter** - 自动发布

### 之后可以加：
3. **Voice Call** - AI 打电话
4. **Whisper** - 语音转文字
5. **Home Assistant** - 智能家居

---

## 💡 提示

- 大多数功能需要 API Keys（免费注册）
- OpenClaw 会记住配置，不会丢失
- 可以随时添加新功能

---

*最后更新：2026-02-08*
*基于 OpenClaw v2026.2.6-3*

