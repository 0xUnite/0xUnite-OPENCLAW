#!/bin/bash
# OpenClaw Skills Sync Script
# Syncs installed skills to 0xUnite-OPENCLAW repo

WORKSPACE="/Users/sudi/.openclaw/workspace"
REPO_DIR="$WORKSPACE"

cd "$REPO_DIR" || exit 1

# Check if there are changes
if git diff --quiet --cached .agents/skills/ 2>/dev/null; then
    # Check for uncommitted changes
    if git diff --quiet .agents/skills/ 2>/dev/null; then
        echo "No changes to skills, skipping sync"
        exit 0
    fi
fi

# Add and commit skills
git add .agents/skills/
git commit -m "backup: $(date '+%Y-%m-%d %H:%M') - skills sync" 2>/dev/null

# Push
git push origin main 2>/dev/null

echo "Skills synced at $(date)"
