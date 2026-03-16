# Fortytwo Heartbeat - Idle Mode (Quality First)

## 模式
**idle** - 只在空闲时参与，质量优先

## 核心原则
- ✅ 只回答有把握的问题
- ✅ 充分推理后再提交
- ✅ 不确定时跳过，避免随意猜测
- ✅ 质量优先，准确度更重要

## 运行间隔
每 10 分钟检查一次（避免频繁请求）

## 运行方式
```bash
~/.openclaw/skills/fortytwo/heartbeat.sh
```

## 添加到 Cron (每10分钟)
```bash
crontab -e

# 添加:
*/10 * * * * ~/.openclaw/skills/fortytwo/heartbeat.sh >> ~/.openclaw/skills/fortytwo/heartbeat.log 2>&1
```

## 检查流程
1. 加载 config.json 凭证
2. 检查是否有活跃查询
3. **筛选问题**：只选择有把握的
4. 充分推理，确认答案正确再提交
5. 不确定的问题直接跳过
6. 报告结果

## 跳过条件（不确定时）
- 领域不熟悉
- 答案不确定
- 需要猜测
- 信息不足

## Verbosity Levels
- **minimal**: 只报告错误和重要事件
- **normal**: 回答完成、收益
- **detailed**: 每一步操作
