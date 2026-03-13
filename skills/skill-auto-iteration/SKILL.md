---
name: skill-auto-iteration
description: Automatically learn from errors and improve OpenClaw Skills through iteration.
metadata:
  {
    "openclaw": { "emoji": "🔄", "requires": { "anyBins": ["claude", "codex"] } },
  }
---

# Skill Auto-Iteration System

自动从错误中学习并改进 OpenClaw Skills。

## 核心机制

```
报错 → 调试 → 总结经验 → 写入 Skill → 推送到 GitHub
    ↓              ↓            ↓            ↓
  捕获错误     分析根因      编写文档      版本控制
              制定方案      更新代码      同步改进
```

## 使用场景

当 OpenClaw 执行任务遇到错误时：
1. 捕获错误信息
2. 分析根本原因
3. 总结经验教训
4. 更新 Skill 文档
5. 提交到 GitHub

## 快速开始

### 手动触发错误学习

```
学习这个错误：{错误信息}
原因：{可能的原因}
解决方案：{如何修复}
```

### 自动学习模式

在任务执行时遇到错误，系统会自动：
1. 记录错误日志
2. 分析错误模式
3. 生成改进建议
4. 更新 Skill

## 示例流程

### 1. 捕获错误
```bash
# Claude Code 执行任务
bash pty:true workdir:~/project command:"claude 'Build a web app'"
# 假设这里报错
```

### 2. 分析原因
分析错误日志，确定是：
- 代码错误
- 配置问题
- 环境缺失
- 权限不足

### 3. 总结经验
```markdown
## 错误：XXX

**原因**：YYY

**解决方案**：
- 方案1：ZZZ
- 方案2：AAA

**预防措施**：
- 添加检查
- 更新文档
- 修改配置
```

### 4. 写入 Skill
更新对应的 SKILL.md 文件，添加错误处理和预防措施。

### 5. 推送到 GitHub
```bash
git add skills/xxx/
git commit -m "fix: 改进 Skill XXX 的错误处理"
git push
```

## 自动迭代配置

### 创建迭代任务

```json
{
  "name": "skill-iteration",
  "trigger": "on-error",
  "actions": [
    "log_error",
    "analyze_pattern",
    "generate_fix",
    "update_skill",
    "notify_user"
  ]
}
```

### 设置学习触发器

当错误率超过阈值时自动触发学习：
```bash
openclaw cron add \
  --name "skill-check" \
  --schedule "0 */4 * * *" \
  --task "检查最近错误并学习"
```

## 最佳实践

1. **及时记录**：遇到错误立即记录
2. **深入分析**：不只是修复，要理解原因
3. **文档更新**：将经验写入 Skill
4. **版本控制**：每次改进都是一次 commit
5. **持续改进**：定期回顾和优化

## 与 coding-agent 集成

使用 coding-agent Skill 执行开发任务：

```bash
# 开发新功能
bash pty:true workdir:~/project command:"codex --yolo exec '添加新功能'"

# 如果报错，自动学习
```

## 输出

- ✅ 更健壮的 Skill
- ✅ 减少重复错误
- ✅ 持续自我改进
- ✅ 知识积累

---

*Auto-generated skill for skill-auto-iteration*
