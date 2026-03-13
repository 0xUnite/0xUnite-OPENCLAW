#!/bin/bash
# Script to paste clipboard content to Android via scrcpy

# Start scrcpy with clipboard sync enabled
scrcpy --no-clipboard-autosync 2>&1 &
SCRCPY_PID=$!

# Wait for scrcpy to start
sleep 3

# Use AppleScript to send Cmd+v (paste) to scrcpy window
osascript -e 'tell application "System Events" to keystroke "v" using command down'

# Wait a bit
sleep 1

# Kill scrcpy
kill $SCRCPY_PID 2>/dev/null

echo "Done"
