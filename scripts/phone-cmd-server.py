#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import os
import base64
import io
from PIL import Image

app = Flask(__name__)

# Use BLIP - a lighter image captioning model
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    
    print("Loading BLIP model...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    print("BLIP model loaded!")
    MODEL_AVAILABLE = True
except Exception as e:
    print(f"BLIP model error: {e}")
    MODEL_AVAILABLE = False

def execute_command(cmd):
    try:
        cmd = cmd.strip()
        if cmd.startswith('adb shell '):
            cmd = cmd[10:]
        elif cmd.startswith('adb '):
            cmd = cmd[4:]
        
        if cmd.startswith('screencap'):
            subprocess.run("adb shell screencap -p /sdcard/screen.png", shell=True, timeout=10)
            subprocess.run("adb pull /sdcard/screen.png /tmp/phone_screen.png", shell=True, timeout=10)
            if os.path.exists("/tmp/phone_screen.png"):
                return "Screenshot saved"
            return "Screenshot failed"
        
        result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_image(image_data):
    """Analyze image using BLIP"""
    try:
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=100)
        result = processor.decode(out[0], skip_special_tokens=True)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/exec')
def exec_cmd():
    cmd = request.args.get('cmd', '')
    if not cmd:
        return jsonify({'error': 'No cmd'}), 400
    return jsonify({'result': execute_command(cmd)})

@app.route('/screenshot/b64')
def screenshot_b64():
    subprocess.run("adb shell screencap -p /sdcard/screen.png", shell=True, timeout=10)
    subprocess.run("adb pull /sdcard/screen.png /tmp/phone_screen.png", shell=True, timeout=10)
    if os.path.exists("/tmp/phone_screen.png"):
        with open("/tmp/phone_screen.png", "rb") as f:
            return jsonify({"image": base64.b64encode(f.read()).decode()})
    return jsonify({"error": "Screenshot failed"}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    if not MODEL_AVAILABLE:
        return jsonify({'error': 'Model not loaded'}), 500
    data = request.get_json()
    image_b64 = data.get('image', '')
    if not image_b64:
        return jsonify({'error': 'No image'}), 400
    result = analyze_image(image_b64)
    return jsonify({'analysis': result})

@app.route('/analyze/screenshot')
def analyze_screenshot():
    if not MODEL_AVAILABLE:
        return jsonify({'error': 'Model not loaded'}), 500
    subprocess.run("adb shell screencap -p /sdcard/screen.png", shell=True, timeout=10)
    subprocess.run("adb pull /sdcard/screen.png /tmp/phone_screen.png", shell=True, timeout=10)
    if not os.path.exists("/tmp/phone_screen.png"):
        return jsonify({'error': 'Screenshot failed'}), 500
    with open("/tmp/phone_screen.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    result = analyze_image(b64)
    return jsonify({'analysis': result})

@app.route('/status')
def status():
    devices = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    return jsonify({'status': 'running', 'model': MODEL_AVAILABLE, 'adb_devices': devices.stdout})

if __name__ == '__main__':
    print("Phone CMD Server with BLIP on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False)
