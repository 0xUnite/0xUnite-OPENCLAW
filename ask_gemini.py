#!/usr/bin/env python3
"""
使用 Gemini API 询问问卷优化建议
"""

import requests
import json
import sys

# Gemini API 配置
GEMINI_API_KEY = "AIzaSyCXTCJ88oj8RaeCzGLBorfIyZES3T4D2i0"
MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# 问题
QUESTION = """
我是管理学博士生，研究题目是'AI服务失误对消费者信任的影响'，
核心假设是：AI的某些'失误'可能产生意外积极的结果（如Serendipity、Pratfall Effect）。

我已经设计了5个情境实验：
A. 意外创意：AI失误→更好的创意
B. 幽默对话：AI幽默回答荒谬问题  
C. 诚实道歉：AI承认错误
D. 意外功能：AI给得比预期多
E. 对照组：无失误

请帮我：
1. 评估这些情境是否有效捕捉核心假设
2. 推荐成熟量表测量意外惊喜、拟人化、信任
3. 建议如何优化问卷题目
4. 指出实验设计的不足之处
"""

def ask_gemini():
    print("🔄 正在调用 Gemini API...")
    print("")
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"请用中文回答以下问题：\n\n{QUESTION}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
            "topP": 0.95
        }
    }
    
    try:
        response = requests.post(
            f"{MODEL_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            print("=" * 60)
            print("✅ Gemini 回答：")
            print("=" * 60)
            print(answer)
            print("=" * 60)
            
            # 保存到文件
            with open("/Users/sudi/.openclaw/workspace/gemini_advice.md", "w", encoding="utf-8") as f:
                f.write("# Gemini 问卷优化建议\n\n")
                f.write(f"**时间**: 2026-02-08\n\n")
                f.write("## 完整回答\n\n")
                f.write(answer)
                f.write("\n\n## 关键建议\n\n")
                f.write("- 需要整理的关键点...\n")
            
            print("")
            print("✅ 回答已保存到: /Users/sudi/.openclaw/workspace/gemini_advice.md")
            
        else:
            print(f"❌ API 调用失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    ask_gemini()
