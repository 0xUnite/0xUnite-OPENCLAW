#!/bin/bash
# TTS wrapper - 使用本地御姐音

# 调用sherpa-tts
~/.openclaw/workspace/scripts/sherpa-tts.sh "$1" "$2"

# 输出文件路径
if [ -n "$2" ]; then
    echo "$2"
else
    echo "/tmp/tts-output.mp3"
fi
