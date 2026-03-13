#!/usr/bin/env python3
"""
Orb Direct Connector - Direct access to Orb's MiniMax backend
Uses BotDrop's stored API credentials
"""

import requests
import json
import sys

# Orb's credentials (from BotDrop app data)
API_KEY = "sk-cp-I6J-KeKQnl-M_pzNQaEgKqSJptVFg4CQ45k5QQpqRZ-MQQodsiHI61m6HkFlRhc8K2R9HnClErdMaIYIufB6Fz1JjgilxPieRGOsMaUOiHLSHRllzt0BaFE"
MODEL = "MiniMax-M2.5"
BASE_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"

def chat(message, system_prompt=None):
    """Send a message to Orb's backend"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    response = requests.post(BASE_URL, headers=headers, json=data, timeout=180)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    result = response.json()
    if "choices" in result and result["choices"]:
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Error: {result}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: orb.py <message>")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    print(f"You: {message}")
    print("Orb: ", end="", flush=True)
    response = chat(message)
    if response:
        print(response)
