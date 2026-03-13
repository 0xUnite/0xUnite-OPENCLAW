#!/usr/bin/env python3
"""
Enhanced Android Phone Controller
Orb Eye-like functionality via ADB (runs from Mac side)
"""

import subprocess
import re
import sys
import os
import time
import json
import xml.etree.ElementTree as ET

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def get_ui_hierarchy():
    """Dump UI hierarchy"""
    run_cmd('adb shell uiautomator dump /sdcard/ui.xml')
    run_cmd(f'adb pull /sdcard/ui.xml {os.path.expanduser("~/.openclaw/workspace/ui.xml")} 2>/dev/null')
    return os.path.expanduser('~/.openclaw/workspace/ui.xml')

def parse_bounds(bounds_str):
    """Parse bounds to center coordinates"""
    match = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if match:
        x1, y1, x2, y2 = map(int, match[0])
        return (x1 + x2) // 2, (y1 + y2) // 2
    return None, None

# ========== ORB EYE API COMPATIBLE ENDPOINTS ==========

def ping():
    """Health check - returns version"""
    return {"ok": True, "version": "1.0-mac-adb"}

def screen():
    """Get all UI elements on screen"""
    xml_file = get_ui_hierarchy()
    elements = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for node in root.iter('node'):
            text = node.get('text', '')
            bounds = node.get('bounds', '')
            resource_id = node.get('resource-id', '')
            clickable = node.get('clickable', 'false')
            enabled = node.get('enabled', 'true')
            
            x, y = parse_bounds(bounds)
            if x:
                elements.append({
                    "text": text,
                    "resource-id": resource_id,
                    "clickable": clickable == "true",
                    "enabled": enabled == "true",
                    "bounds": bounds,
                    "center": {"x": x, "y": y}
                })
    except Exception as e:
        return {"error": str(e)}
    
    return elements

def tree():
    """Full accessibility node tree"""
    return screen()  # Simplified version

def info():
    """Get current app info"""
    out, _ = run_cmd("adb shell dumpsys window | grep mCurrentFocus")
    match = re.search(r'mCurrentFocus=Window.*u0 (\S+)/(\S+)', out)
    if match:
        return {"package": match.group(1), "activity": match.group(2)}
    return {"package": "unknown", "activity": "unknown"}

def notify():
    """Get recent notifications"""
    out, _ = run_cmd('adb shell dumpsys notification --noredact | head -100')
    
    notifications = []
    # Parse notification lines
    for line in out.split('\n'):
        if 'title=' in line:
            match = re.search(r'title=(.+?)(?:\n|$)', line)
            if match:
                notifications.append({"title": match.group(1).strip()})
    
    return notifications[:10]

def click(text=None, x=None, y=None):
    """Click by text or coordinates"""
    if text:
        # Find element by text
        xml_file = get_ui_hierarchy()
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for node in root.iter('node'):
                if text.lower() in node.get('text', '').lower():
                    bounds = node.get('bounds', '')
                    cx, cy = parse_bounds(bounds)
                    if cx:
                        run_cmd(f'adb shell input tap {cx} {cy}')
                        return {"ok": True, "clicked": f"{text} at {cx},{cy}"}
        except:
            pass
        return {"error": f"Element not found: {text}"}
    
    if x and y:
        run_cmd(f'adb shell input tap {x} {y}')
        return {"ok": True, "clicked": f"{x},{y}"}
    
    return {"error": "Need text or x,y"}

def tap(x, y):
    """Tap at coordinates"""
    run_cmd(f'adb shell input tap {x} {y}')
    return {"ok": True}

def swipe(x1, y1, x2, y2, duration=300):
    """Swipe gesture"""
    run_cmd(f'adb shell input swipe {x1} {y1} {x2} {y2} {duration}')
    return {"ok": True}

def longpress(x, y):
    """Long press"""
    run_cmd(f'adb shell input swipe {x} {y} {x} {y} 500')
    return {"ok": True}

def setText(text):
    """Inject text into focused field"""
    # Escape special characters
    text = text.replace(' ', '%s')
    run_cmd(f'adb shell input text "{text}"')
    return {"ok": True}

def back():
    """Press back button"""
    run_cmd('adb shell input keyevent 4')
    return {"ok": True}

def home():
    """Press home button"""
    run_cmd('adb shell input keyevent 3')
    return {"ok": True}

# ========== CONVENIENCE FUNCTIONS ==========

def screenshot():
    """Take screenshot"""
    run_cmd('adb shell screencap -p /sdcard/screen.png')
    run_cmd(f'adb pull /sdcard/screen.png {os.path.expanduser("~/.openclaw/workspace/phone_screen.png")} 2>/dev/null')
    return {"path": os.path.expanduser("~/.openclaw/workspace/phone_screen.png")}

def unlock(pin):
    """Unlock with PIN"""
    run_cmd('adb shell input keyevent 26')  # Wake
    time.sleep(1)
    run_cmd(f'adb shell input text "{pin}"')
    time.sleep(1)
    return {"ok": True}

def open_app(package):
    """Open app by package name"""
    out, _ = run_cmd(f'adb shell pm resolve-activity -c android.intent.category.LAUNCHER {package} 2>/dev/null')
    if out:
        run_cmd(f'adb shell am start -n {out}')
        return {"ok": True, "started": out}
    return {"error": f"Cannot resolve {package}"}

def list_apps():
    """List installed apps"""
    out, _ = run_cmd('adb shell pm list packages -3')
    packages = [p.replace('package:', '') for p in out.split('\n') if p.strip()]
    return packages[:50]

# ========== CLI ==========

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Android Phone Controller (Orb Eye compatible)

Orb Eye API:
  ping                 - Health check
  screen               - Get all UI elements
  info                 - Current app info
  notify               - Recent notifications
  click <text>         - Click element by text
  tap <x> <y>         - Tap coordinates
  swipe <x1> <y1> <x2> <y2> - Swipe
  setText <text>       - Input text
  back                 - Press back
  home                 - Press home

Convenience:
  screenshot           - Take screenshot
  unlock <pin>        - Unlock with PIN
  open <package>      - Open app
  apps                - List installed apps
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "ping":
        print(json.dumps(ping()))
    elif cmd == "screen":
        print(json.dumps(screen(), indent=2))
    elif cmd == "info":
        print(json.dumps(info(), indent=2))
    elif cmd == "notify":
        print(json.dumps(notify(), indent=2))
    elif cmd == "screenshot":
        print(json.dumps(screenshot()))
    elif cmd == "back":
        print(json.dumps(back()))
    elif cmd == "home":
        print(json.dumps(home()))
    elif cmd == "click" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        print(json.dumps(click(text=text)))
    elif cmd == "tap" and len(sys.argv) > 3:
        x, y = int(sys.argv[2]), int(sys.argv[3])
        print(json.dumps(tap(x, y)))
    elif cmd == "swipe" and len(sys.argv) > 5:
        x1, y1, x2, y2 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        print(json.dumps(swipe(x1, y1, x2, y2)))
    elif cmd == "setText" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        print(json.dumps(setText(text)))
    elif cmd == "unlock" and len(sys.argv) > 2:
        pin = sys.argv[2]
        print(json.dumps(unlock(pin)))
    elif cmd == "open" and len(sys.argv) > 2:
        pkg = sys.argv[2]
        print(json.dumps(open_app(pkg)))
    elif cmd == "apps":
        print(json.dumps(list_apps(), indent=2))
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
