#!/bin/bash
# Phone automation script for OpenClaw
# Usage: bash ~/.openclaw/workspace/scripts/phone-auto.sh [command]
# Commands: screenshot, list, click, swipe, input, shell, unlock

# Unlock password (stored locally - change if needed)
PASSWORD="202020"

PHONE_DIR="/Users/sudi/.openclaw/workspace/memory/phone"
SCREENSHOT="$PHONE_DIR/screenshot.png"
mkdir -p "$PHONE_DIR"

case "$1" in
    screenshot)
        adb exec-out screencap -p > "$SCREENSHOT"
        echo "Screenshot saved to $SCREENSHOT"
        ls -la "$SCREENSHOT"
        ;;
    click)
        if [ -z "$2" ]; then
            echo "Usage: phone-auto.sh click <x> <y>"
            exit 1
        fi
        adb shell input tap "$2" "$3"
        echo "Tapped at $2, $3"
        ;;
    swipe)
        if [ -z "$2" ]; then
            echo "Usage: phone-auto.sh swipe <x1> <y1> <x2> <y2> [duration]"
            exit 1
        fi
        DURATION="${5:-300}"
        adb shell input swipe "$2" "$3" "$4" "$5" "$DURATION"
        echo "Swiped from $2,$3 to $4,$5"
        ;;
    input)
        if [ -z "$2" ]; then
            echo "Usage: phone-auto.sh input <text>"
            exit 1
        fi
        TEXT="$2"
        adb shell input text "$TEXT"
        echo "Input: $TEXT"
        ;;
    shell)
        shift
        adb shell "$@"
        ;;
    list)
        echo "Available commands:"
        echo "  screenshot - Capture screen"
        echo "  click <x> <y> - Tap at coordinates"
        echo "  swipe <x1> <y1> <x2> <y2> [duration] - Swipe gesture"
        echo "  input <text> - Input text"
        echo "  shell <command> - Run ADB shell command"
        echo "  unlock - Wake and unlock phone"
        echo ""
        echo "Screenshot location: $SCREENSHOT"
        ;;
    unlock)
        echo "Waking phone..."
        adb shell input keyevent KEYCODE_WAKEUP
        sleep 1
        adb shell input keyevent KEYCODE_MENU
        sleep 1
        echo "Inputting password: $PASSWORD"
        adb shell input text "$PASSWORD"
        echo "Unlock attempted"
        ;;
    *)
        echo "Phone Automation for OpenClaw"
        echo "Usage: $0 <command> [args]"
        echo ""
        $0 list
        ;;
esac
