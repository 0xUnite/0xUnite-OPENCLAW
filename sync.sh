#!/bin/bash
# OpenClaw Memory Sync Script
# Syncs to 0xUnite-OPENCLAW repo twice daily

cd /Users/sudi/0xUnite-OPENCLAW || exit 1

# Add and commit
git add -A
git commit -m "docs: $(date '+%Y-%m-%d %H:%M') - 内存同步" 2>/dev/null

# Push
git push origin main 2>/dev/null

echo "Memory synced at $(date)"
