#!/usr/bin/env python3
"""
Android Phone Controller - Enhanced Version
Uses uiautomator to get UI hierarchy and click elements by name
"""

import subprocess
import re
import sys
import os
import time
import xml.etree.ElementTree as ET

ANDROID_NS = '{http://schemas.android.com/apk/res/android}'

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def get_ui_hierarchy():
    """Dump UI hierarchy to file and pull it"""
    run_cmd('adb shell uiautomator dump /sdcard/ui.xml')
    run_cmd(f'adb pull /sdcard/ui.xml {os.path.expanduser("~/.openclaw/workspace/ui.xml")}')
    return os.path.expanduser('~/.openclaw/workspace/ui.xml')

def parse_bounds(bounds_str):
    """Parse bounds string like '[0,0][1080,2376]' to (x1, y1, x2, y2)"""
    match = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if match:
        x1, y1, x2, y2 = map(int, match[0])
        return (x1 + x2) // 2, (y1 + y2) // 2  # center
    return None, None

def find_element_by_text(xml_file, text):
    """Find element by text content"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for node in root.iter('node'):
            node_text = node.get('text', '')
            bounds = node.get('bounds', '')
            
            if text.lower() in node_text.lower():
                x, y = parse_bounds(bounds)
                if x:
                    return {
                        'text': node_text,
                        'resource-id': node.get('resource-id', ''),
                        'class': node.get('class', ''),
                        'clickable': node.get('clickable', 'false'),
                        'x': x,
                        'y': y,
                        'bounds': bounds
                    }
        return None
    except Exception as e:
        print(f"Error parsing UI: {e}")
        return None

def find_element_by_resource_id(xml_file, resource_id):
    """Find element by resource-id"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for node in root.iter('node'):
            rid = node.get('resource-id', '')
            bounds = node.get('bounds', '')
            
            if resource_id in rid:
                x, y = parse_bounds(bounds)
                if x:
                    return {
                        'text': node.get('text', ''),
                        'resource-id': rid,
                        'class': node.get('class', ''),
                        'clickable': node.get('clickable', 'false'),
                        'x': x,
                        'y': y,
                        'bounds': bounds
                    }
        return None
    except Exception as e:
        print(f"Error parsing UI: {e}")
        return None

def find_all_clickable_elements(xml_file):
    """Find all clickable elements"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        elements = []
        for node in root.iter('node'):
            clickable = node.get('clickable', 'false')
            bounds = node.get('bounds', '')
            
            if clickable == 'true':
                x, y = parse_bounds(bounds)
                if x:
                    elements.append({
                        'text': node.get('text', ''),
                        'resource-id': node.get('resource-id', ''),
                        'class': node.get('class', ''),
                        'x': x,
                        'y': y,
                        'bounds': bounds
                    })
        return elements
    except Exception as e:
        print(f"Error parsing UI: {e}")
        return []

def tap(x, y):
    """Tap at coordinates"""
    run_cmd(f'adb shell input tap {x} {y}')
    return True

def get_current_app():
    """Get currently focused app"""
    out, _ = run_cmd("adb shell dumpsys window | grep mCurrentFocus")
    match = re.search(r'mCurrentFocus=Window.*u0 (\S+)', out)
    if match:
        return match.group(1)
    return None

def take_screenshot():
    """Take screenshot and save to workspace"""
    run_cmd('adb shell screencap -p /sdcard/screen.png')
    run_cmd(f'adb pull /sdcard/screen.png {os.path.expanduser("~/.openclaw/workspace/phone_screen.png")}')
    return os.path.expanduser('~/.openclaw/workspace/phone_screen.png')

def input_text(text):
    """Input text (escaped for shell)"""
    # Escape special characters
    text = text.replace(' ', '%s')
    run_cmd(f'adb shell input text "{text}"')

def swipe(x1, y1, x2, y2, duration=300):
    """Swipe from (x1,y1) to (x2,y2)"""
    run_cmd(f'adb shell input swipe {x1} {y1} {x2} {y2} {duration}')

def press_key(keycode):
    """Press keyevent"""
    run_cmd(f'adb shell input keyevent {keycode}')

def open_app(package_name):
    """Open app by package name"""
    # Try to get main activity
    out, _ = run_cmd(f'adb shell cmd package resolve-activity --brief -c android.intent.category.LAUNCHER {package_name}')
    if out:
        run_cmd(f'adb shell am start -n {out}')
        return True
    return False

def get_notifications():
    """Get recent notifications (requires notification listener)"""
    # This is limited - we can only see what's in the notification shade
    out, _ = run_cmd('adb shell dumpsys notification --noredact')
    return out[:5000]  # Limit output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Android Phone Controller

Commands:
  screenshot              - Take screenshot
  ui                      - Get UI hierarchy and print clickable elements
  click <text>           - Click element containing text
  click-id <resource-id> - Click element by resource-id
  tap <x> <y>           - Tap at coordinates
  current-app            - Get current app
  text <string>         - Input text
  swipe <x1> <y1> <x2> <y2> - Swipe
  key <keycode>         - Press key (3=home, 4=back, 26=power)
  open <package>        - Open app by package name
  notify                 - Get notifications
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "screenshot":
        path = take_screenshot()
        print(f"Screenshot: {path}")
    
    elif cmd == "ui":
        xml_file = get_ui_hierarchy()
        elements = find_all_clickable_elements(xml_file)
        print(f"Found {len(elements)} clickable elements:\n")
        for e in elements[:20]:
            print(f"  - {e['text'] or '(no text)'} | {e['resource-id'] or '(no id)'} | {e['x']},{e['y']}")
    
    elif cmd == "click" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        xml_file = get_ui_hierarchy()
        elem = find_element_by_text(xml_file, text)
        if elem:
            print(f"Found: {elem['text']} at {elem['x']},{elem['y']}")
            tap(elem['x'], elem['y'])
            print("Tapped!")
        else:
            print(f"Element not found: {text}")
    
    elif cmd == "click-id" and len(sys.argv) > 2:
        rid = sys.argv[2]
        xml_file = get_ui_hierarchy()
        elem = find_element_by_resource_id(xml_file, rid)
        if elem:
            print(f"Found: {elem['text']} at {elem['x']},{elem['y']}")
            tap(elem['x'], elem['y'])
            print("Tapped!")
        else:
            print(f"Element not found: {rid}")
    
    elif cmd == "tap" and len(sys.argv) > 3:
        x, y = int(sys.argv[2]), int(sys.argv[3])
        tap(x, y)
        print(f"Tapped {x},{y}")
    
    elif cmd == "current-app":
        print(get_current_app())
    
    elif cmd == "text" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        input_text(text)
        print("Text input done")
    
    elif cmd == "swipe" and len(sys.argv) > 5:
        x1, y1, x2, y2 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        swipe(x1, y1, x2, y2)
        print("Swiped")
    
    elif cmd == "key" and len(sys.argv) > 2:
        press_key(sys.argv[2])
        print("Key pressed")
    
    elif cmd == "open" and len(sys.argv) > 2:
        open_app(sys.argv[2])
        print("App opened")
    
    elif cmd == "notify":
        print(get_notifications())
    
    else:
        print(f"Unknown command: {cmd}")
