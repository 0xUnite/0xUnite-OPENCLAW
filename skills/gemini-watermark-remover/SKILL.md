---
name: gemini-watermark-remover
description: >
  Removes watermarks from Gemini AI-generated images using mathematical reverse alpha blending.
  No AI needed — pure algorithm based on the known Gemini watermark pattern (48×48 or 96×96, bottom-right).
  Trigger: user sends a Gemini-generated image and asks to remove the watermark.
  Supports PNG, JPG, WEBP. Output saved to /Users/sudi/.openclaw/workspace/.
license: MIT
---

# Gemini Watermark Remover

基于反向 Alpha 混合算法的 Gemini 水印去除工具，纯数学计算，无需 AI。

## 算法原理

Gemini 通过以下公式添加水印：
```
水印图 = α × 255(白) + (1-α) × 原图
```
反向求解：
```
原图 = (水印图 - α × 255) / (1-α)
```

水印位于图片**右下角**，尺寸为 48×48 或 96×96（根据图片分辨率自动判断）。

## 使用方法

### 命令行
```bash
python3 ~/.openclaw/workspace/skills/gemini-watermark-remover/scripts/remove_watermark.py <图片路径> [输出路径]
```

### 通过 AI Agent（推荐）
直接发送 Gemini 生成的图片给 Agent，说"去水印"即可。

## 示例

```bash
# 基本用法（自动保存为 input_named_no_watermark.png）
python3 ~/.openclaw/workspace/skills/gemini-watermark-remover/scripts/remove_watermark.py gemini_output.png

# 指定输出文件名
python3 ~/.openclaw/workspace/skills/gemini-watermark-remover/scripts/remove_watermark.py gemini_output.png clean.png

# 显示详细信息
python3 ~/.openclaw/workspace/skills/gemini-watermark-remover/scripts/remove_watermark.py gemini_output.png --verbose
```

## 依赖

```bash
pip3 install pillow numpy
```

## 限制

- ⚠️ 仅对 **Gemini AI 生成的图片**有效
- ⚠️ 水印必须在标准位置（右下方）
- ❌ 对其他来源图片（照片、其他AI生成图）无效
