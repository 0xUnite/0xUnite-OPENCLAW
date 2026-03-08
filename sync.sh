#!/bin/bash
# OpenClaw Memory Sync Script
# Syncs to 0xUnite-OPENCLAW repo twice daily

cd ~/0xUnite-OPENCLAW || exit 1

# Update README with current status
cat > README.md << 'EOF'
# 0xUnite OpenCLAW 记忆库

> 个人 AI 助手 OpenClaw 的功能记忆库

---

## 概述

本仓库用于记录 OpenClaw AI 助手已配置的功能、技能、项目，避免重复造轮子。

---

## 核心项目

| 项目 | 状态 | 描述 |
|------|------|------|
| KoreaRealEstate | ✅ | 韩国租房网站 (端口3000+Cloudflare) |
| Nexus | ✅ | 6节点运行中 |
| Fortytwo | ✅ | AI Agent (余额717.5 Energy) |
| binance-ai-assistant | ✅ | 币安AI交易助手 |
| okx-onchain-assistant | ✅ | OKX OnchainOS AI 助手 (参赛作品) |

EOF

# Add and commit
git add -A
git commit -m "docs: $(date '+%Y-%m-%d %H:%M') - 内存同步" 2>/dev/null

# Push
git push origin main 2>/dev/null

echo "Memory synced at $(date)"
EOF

chmod +x ~/0xUnite-OPENCLAW/sync.sh