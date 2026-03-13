#!/data/data/com.termux/files/usr/bin/python3
"""
手机端 HTTP 服务 - 接收电脑指令
"""
import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/exec')
def exec_cmd():
    cmd = request.args.get('cmd', '')
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return jsonify({
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/screenshot')
def screenshot():
    subprocess.run('screencap -p /sdcard/screen.png', shell=True)
    with open('/sdcard/screen.png', 'rb') as f:
        import base64
        return jsonify({'image': base64.b64encode(f.read()).decode()})

if __name__ == '__main__':
    # 端口转发: adb forward tcp:8080 tcp:8080
    print("Starting phone HTTP server on port 8080...")
    app.run(host='0.0.0.0', port=8080)
