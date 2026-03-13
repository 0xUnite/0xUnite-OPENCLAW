#!/bin/bash
# MiniMax-M2.5 一键升级脚本
# 使用方法: bash <(curl -sL https://raw.githubusercontent.com/xxx/upgrade-m25.sh)

echo "=== MiniMax-M2.5 升级开始 ==="

# 1. 安装 anthropic 库
echo "[1/4] 安装 anthropic 库..."
pip3 install anthropic --break-system-packages -q

# 2. 读取当前配置
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# 3. 检查是否已有 M2.5
if grep -q "MiniMax-M2.5" "$CONFIG_FILE"; then
    echo "[2/4] M2.5 已配置，跳过"
else
    echo "[2/4] 添加 M2.5 模型..."
    # 备份
    cp "$CONFIG_FILE" "$CONFIG_FILE.bak"
    
    # 使用 python 更新配置
    python3 << 'PYEOF'
import json

config_file = "/Users/sudi/.openclaw/openclaw.json"
with open(config_file, 'r') as f:
    config = json.load(f)

# 添加 M2.5 模型
m25_model = {
    "id": "MiniMax-M2.5",
    "name": "MiniMax M2.5",
    "reasoning": False,
    "input": ["text"],
    "cost": {"input": 15, "output": 60, "cacheRead": 2, "cacheWrite": 10},
    "contextWindow": 200000,
    "maxTokens": 8192
}

models = config['models']['providers']['minimax']['models']
# 添加 M2.5 到列表前面
config['models']['providers']['minimax']['models'] = [m25_model] + models

# 更新主 agent
config['agents']['list'][0]['model']['primary'] = 'minimax/MiniMax-M2.5'
config['agents']['list'][1]['model']['primary'] = 'minimax/MiniMax-M2.5'
config['defaults']['model']['primary'] = 'minimax/MiniMax-M2.5'

# 添加 alias
config['defaults']['models']['minimax/MiniMax-M2.5'] = {"alias": "Minimax"}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("配置已更新")
PYEOF
fi

# 4. 重启 OpenClaw
echo "[3/4] 重启 OpenClaw..."
pkill -f openclaw-gateway 2>/dev/null
sleep 2
openclaw gateway start >/dev/null 2>&1 &
sleep 3

# 5. 验证
echo "[4/4] 验证 M2.5..."
python3 << 'PYEOF'
import anthropic, os
os.environ['ANTHROPIC_BASE_URL'] = 'https://api.minimaxi.com/anthropic'
os.environ['ANTHROPIC_API_KEY'] = '你的API_KEY'
client = anthropic.Anthropic()
msg = client.messages.create(model='MiniMax-M2.5', max_tokens=20, messages=[{'role': 'user', 'content': 'Hi'}])
print(f"✅ 成功! Model: {msg.model}")
PYEOF

echo "=== 升级完成 ==="
