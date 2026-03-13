#!/bin/bash
# ~/.openclaw/workspace/scripts/voice-to-text.sh
# 语音转文字脚本

AUDIO_FILE="$1"

if [ -z "$AUDIO_FILE" ]; then
    echo "Usage: voice-to-text.sh <audio_file>"
    exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
    echo "文件不存在: $AUDIO_FILE"
    exit 1
fi

# 检查文件格式，OGG需要转换
FILE_EXT="${AUDIO_FILE##*.}"
if [ "$FILE_EXT" = "ogg" ] || [ "$FILE_EXT" = "oga" ]; then
    # OGG转MP3 (Whisper支持OGG但某些版本可能需要转换)
    MP3_FILE="${AUDIO_FILE%.ogg}.mp3"
    if [ ! -f "$MP3_FILE" ]; then
        ffmpeg -i "$AUDIO_FILE" -vn -acodec libmp3lame -q:a 2 "$MP3_FILE" 2>/dev/null
    fi
    AUDIO_FILE="$MP3_FILE"
fi

# 使用Whisper转文字
whisper "$AUDIO_FILE" \
    --model small \
    --output_format txt \
    --output_dir "$(dirname "$AUDIO_FILE")" \
    --language Chinese 2>/dev/null

# 输出结果
TXT_FILE="${AUDIO_FILE%.*}.txt"
if [ -f "$TXT_FILE" ]; then
    cat "$TXT_FILE"
else
    echo "转文字失败"
    exit 1
fi
