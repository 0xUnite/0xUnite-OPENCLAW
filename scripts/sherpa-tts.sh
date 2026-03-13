#!/bin/bash
# ~/.openclaw/workspace/scripts/sherpa-tts.sh
# 本地TTS脚本 - 中文御姐音

RUNTIME_DIR="/Users/sudi/.openclaw/tools/sherpa-onnx-tts/runtime/sherpa-onnx-v1.12.23-osx-universal2-shared"

# 中文御姐音
MODEL_DIR="/Users/sudi/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-zh_CN-huayan-medium"

TEXT="$1"
OUTPUT_FILE="$2"

if [ -z "$TEXT" ]; then
    echo "Usage: sherpa-tts.sh \"text to speak\" [output_file]"
    exit 1
fi

if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="/tmp/tts-output-$(date +%s).mp3"
fi

# 生成语音
"$RUNTIME_DIR/bin/sherpa-onnx-offline-tts" \
    --vits-model="$MODEL_DIR/zh_CN-huayan-medium.onnx" \
    --vits-tokens="$MODEL_DIR/tokens.txt" \
    --vits-data-dir="$MODEL_DIR/espeak-ng-data" \
    --output-filename="${OUTPUT_FILE%.mp3}.wav" \
    "$TEXT" 2>/dev/null

# 转换MP3
if [ -f "${OUTPUT_FILE%.mp3}.wav" ]; then
    ffmpeg -i "${OUTPUT_FILE%.mp3}.wav" -vn -acodec libmp3lame -q:a 2 "$OUTPUT_FILE" 2>/dev/null
    rm -f "${OUTPUT_FILE%.mp3}.wav"
    echo "$OUTPUT_FILE"
else
    echo "Error: Failed to generate speech" >&2
    exit 1
fi
