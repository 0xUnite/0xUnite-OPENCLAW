#!/bin/bash
# Voice to text using mlx-whisper
# Usage: voice-to-text.sh [audio_file] or voice-to-text.sh --mic

export PATH="/Users/sudi/Library/Python/3.9/bin:$PATH"

if [[ "$1" == "--mic" || "$1" == "-m" ]]; then
    # Record from microphone
    echo "🎙️ Recording... (press Ctrl+C to stop)"
    ffmpeg -f avfoundation -i ":0" -t 60 -y /tmp/voice-input.m4a 2>/dev/null
    AUDIO_FILE="/tmp/voice-input.m4a"
elif [[ -n "$1" ]]; then
    AUDIO_FILE="$1"
else
    echo "Usage: voice-to-text.sh [audio_file] or voice-to-text.sh --mic"
    exit 1
fi

echo "🔄 Transcribing..."
mlx_whisper "$AUDIO_FILE" --model mlx-community/whisper-base-mlx --output-dir /tmp --output-format txt 2>/dev/null

# Show result
RESULT=$(cat /tmp/voice-input.txt 2>/dev/null || echo "Transcription failed")
echo ""
echo "📝 Result:"
echo "$RESULT"
