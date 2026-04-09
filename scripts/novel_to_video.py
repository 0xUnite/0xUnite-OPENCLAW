#!/usr/bin/env python3
"""
小说转AI短剧 - MiniMax全链路自动化脚本
==========================================
功能：
  1. 读取小说章节文本
  2. MiniMax LLM 生成视频分镜脚本
  3. MiniMax VL 生成关键帧图片
  4. Hailuo 生成视频片段
  5. MiniMax TTS 生成配音
  6. FFmpeg 自动拼接 + 字幕 + BGM
  7. 输出完整MP4视频

依赖： pip install requests python-dotenv
"""

import os
import sys
import json
import time
import requests
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "sk-cp-I6J-KeKQnl-M_pzNQaEgKqSJptVFg4CQ45k5QQpqRZ-MQQodsiHI61m6HkFlRhc8K2R9HnClErdMaIYIufB6Fz1JjgilxPieRGOsMaUOiHLSHRllzt0BaFE")
BASE_URL = "https://api.minimaxi.com"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ============== 数据结构 ==============
@dataclass
class Scene:
    """单个场景"""
    scene_id: int
    description: str  # 场景描述（用于生成视频）
    narration: str     # 旁白/对话文本（用于配音）
    duration: int = 6  # 视频时长（秒）

@dataclass
class ChapterScript:
    """章节脚本"""
    chapter_title: str
    scenes: List[Scene]
    total_duration: int  # 总时长（秒）

# ============== 工具函数 ==============

def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def save_json(data, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def download_file(url: str, output_path: str, headers=None) -> bool:
    """下载文件"""
    try:
        response = requests.get(url, headers=headers or {}, timeout=60)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        log(f"下载失败: {e}")
        return False

def upload_file_to_minimax(file_path: str, purpose: str = "video_generation") -> Optional[str]:
    """上传本地文件到 MiniMax 服务器并返回 file_id"""
    log(f"📤 上传文件: {file_path}")
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"purpose": purpose}
            response = requests.post(
                f"{BASE_URL}/v1/files/upload",
                headers={"Authorization": f"Bearer {API_KEY}"},
                files=files,
                data=data,
                timeout=60
            )
        
        if response.status_code != 200:
            log(f"❌ 文件上传失败: {response.text}")
            return None
        
        result = response.json()
        return result.get("file", {}).get("file_id")
    except Exception as e:
        log(f"❌ 上传过程出错: {e}")
        return None

# ============== MiniMax LLM - 分镜脚本生成 ==============

def generate_script_with_llm(chapter_text: str, chapter_title: str = "第X章") -> ChapterScript:
    """
    使用 MiniMax LLM 将小说章节转换为视频分镜脚本
    """
    log("📝 调用 MiniMax LLM 生成视频分镜脚本...")
    
    prompt = f"""你是一个专业的AI短剧分镜师。请将以下小说章节转换为一个完整的视频分镜脚本。

## 要求：
1. 将章节内容分解为6-10个关键场景
2. 每个场景包含：画面描述（用于AI视频生成）、旁白/对话（用于配音）
3. 每个场景时长控制在5-8秒
4. 优先选择有视觉冲击力的场景（对话、动作、情绪变化）
5. 保持故事连贯性

## 输出格式（严格JSON）：
{{
    "chapter_title": "章节标题",
    "scenes": [
        {{
            "scene_id": 1,
            "description": "画面描述，要详细具体，包含场景、人物、动作、光线等",
            "narration": "旁白或对话文本，简短有力",
            "duration": 6
        }}
    ]
}}

## 小说章节：
{chapter_text[:3000]}

请直接输出JSON，不要有其他内容。
"""

    payload = {
        "model": "MiniMax-M2.7",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{BASE_URL}/anthropic/v1/messages",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        },
        json=payload,
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"LLM调用失败: {response.text}")
    
    result = response.json()
    content_array = result.get("content", [])
    
    # 从content数组中提取text类型的块
    text_content = ""
    for item in content_array:
        if item.get("type") == "text":
            text_content = item.get("text", "")
            break
    
    if not text_content:
        raise Exception("LLM响应中没有找到text内容")
    
    # 提取JSON - 更精确的提取方式
    # 尝试从 ```json ... ``` 中提取
    json_patterns = [
        r'```json\s*([\s\S]*?)\s*```',  # markdown代码块
        r'```\s*([\s\S]*?)\s*```',       # 任意代码块
        r'\{[\s\S]*"scenes"[\s\S]*\}',  # 包含scenes字段的完整JSON
    ]
    
    script_data = None
    for pattern in json_patterns:
        match = re.search(pattern, text_content)
        if match:
            try:
                json_str = match.group(1) if '```' in pattern else match.group()
                script_data = json.loads(json_str)
                break
            except json.JSONDecodeError:
                continue
    
    if not script_data:
        # 最后尝试：找到第一个 { 和最后一个 } 之间的内容
        first_brace = text_content.find('{')
        last_brace = text_content.rfind('}')
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_str = text_content[first_brace:last_brace+1]
            try:
                script_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise Exception(f"无法解析LLM输出为JSON: {e}\n内容前100字符: {text_content[:100]}")
        else:
            raise Exception(f"无法在LLM输出中找到JSON\n内容前200字符: {text_content[:200]}")
    
    scenes = [
        Scene(
            scene_id=s["scene_id"],
            description=s["description"],
            narration=s["narration"],
            duration=s.get("duration", 6)
        )
        for s in script_data["scenes"]
    ]
    
    chapter_script = ChapterScript(
        chapter_title=script_data.get("chapter_title", chapter_title),
        scenes=scenes,
        total_duration=sum(s.duration for s in scenes)
    )
    
    log(f"✅ 生成了 {len(scenes)} 个场景，总时长 {chapter_script.total_duration} 秒")
    return chapter_script

# ============== MiniMax VL - 图片生成 ==============

def generate_image_with_vl(prompt: str, output_path: str) -> bool:
    """
    使用 MiniMax VL 生成关键帧图片
    """
    log(f"🖼️ 生成图片: {prompt[:50]}...")
    
    payload = {
        "model": "MiniMax-VL-01",
        "prompt": f"请生成一张高质量的AI短剧关键帧图片。风格要求：电影感、暖色调、构图精美。画面内容：{prompt}",
        "size": "16:9",
        "n": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/images",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=60
    )
    
    if response.status_code != 200:
        log(f"❌ 图片生成失败: {response.text}")
        return False
    
    result = response.json()
    image_url = result["data"][0]["url"]
    
    return download_file(image_url, output_path)

# ============== Hailuo - 视频生成 ==============

def generate_video_with_hailuo(
    prompt: str, 
    first_frame_image: str = None,
    duration: int = 6,
    model: str = "MiniMax-Video-01"
) -> Optional[str]:
    """
    使用 Hailuo 生成视频
    返回: task_id
    """
    log(f"🎬 提交视频生成任务: {prompt[:60]}...")
    
    payload = {
        "prompt": prompt,
        "model": model,
        "duration": duration,
        "resolution": "1080P"
    }
    
    if first_frame_image and os.path.exists(first_frame_image):
        # 先上传图片获取 file_id
        file_id = upload_file_to_minimax(first_frame_image)
        if file_id:
            payload["first_frame_image"] = file_id
    
    response = requests.post(
        f"{BASE_URL}/v1/video_generation",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=30
    )
    
    if response.status_code != 200:
        log(f"❌ 视频生成任务提交失败: {response.text}")
        return None
    
    result = response.json()
    task_id = result.get("task_id")
    log(f"📋 任务ID: {task_id}")
    return task_id

def query_video_status(task_id: str) -> Optional[str]:
    """
    查询视频生成状态
    返回: file_id (成功) / None (失败或进行中)
    """
    max_wait = 300  # 最多等5分钟
    interval = 10
    elapsed = 0
    
    while elapsed < max_wait:
        response = requests.get(
            f"{BASE_URL}/v1/query/video_generation",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"task_id": task_id},
            timeout=30
        )
        
        if response.status_code != 200:
            log(f"查询失败: {response.text}")
            time.sleep(interval)
            elapsed += interval
            continue
        
        result = response.json()
        status = result.get("status")
        
        if status == "Success":
            log(f"✅ 视频生成成功!")
            return result.get("file_id")
        elif status == "Fail":
            log(f"❌ 视频生成失败: {result.get('error_message', '未知错误')}")
            return None
        else:
            log(f"⏳ 视频生成中... ({elapsed}s)")
            time.sleep(interval)
            elapsed += interval
    
    log(f"⏰ 视频生成超时")
    return None

def download_video(file_id: str, output_path: str) -> bool:
    """下载生成的视频"""
    # 获取下载链接
    response = requests.get(
        f"{BASE_URL}/v1/files/retrieve",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"file_id": file_id},
        timeout=30
    )
    
    if response.status_code != 200:
        log(f"获取文件信息失败: {response.text}")
        return False
    
    result = response.json()
    download_url = result["file"]["download_url"]
    
    return download_file(download_url, output_path)

# ============== MiniMax TTS - 配音生成 ==============

def generate_tts(narration: str, output_path: str, voice_id: str = "audiobook_male_1") -> bool:
    """
    使用 MiniMax TTS 生成配音
    """
    log(f"🎙️ 生成配音: {narration[:30]}...")
    
    payload = {
        "model": "speech-2.8-hd",
        "text": narration,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1.0
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/t2a_async_v2",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=30
    )
    
    if response.status_code != 200:
        log(f"❌ TTS生成失败: {response.text}")
        return False
    
    result = response.json()
    task_id = result.get("task_id")
    
    # 轮询等待完成
    for _ in range(60): # 增加到2分钟
        time.sleep(2)
        status_resp = requests.get(
            f"{BASE_URL}/v1/query/t2a_async_query_v2",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"task_id": task_id},
            timeout=30
        )
        
        if status_resp.status_code == 200:
            status_data = status_resp.json()
            status = status_data.get("status", "").lower()
            if status == "success":
                # 获取音频文件
                file_id = status_data.get("file_id")
                file_resp = requests.get(
                    f"{BASE_URL}/v1/files/retrieve",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    params={"file_id": file_id},
                    timeout=30
                )
                if file_resp.status_code == 200:
                    file_data = file_resp.json()
                    download_url = file_data["file"]["download_url"]
                    return download_file(download_url, output_path)
            elif status == "fail":
                log(f"❌ TTS任务失败: {status_data.get('error_message')}")
                return False
    
    log(f"❌ TTS生成超时")
    return False

# ============== FFmpeg - 视频拼接 ==============

def add_subtitle_to_video(video_path: str, subtitle_text: str, output_path: str) -> bool:
    """给视频添加字幕"""
    # 创建临时字幕文件(SRT格式)
    subtitle_path = video_path + ".srt"
    
    # 简单处理：单行字幕
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:10,000\n")
        f.write(subtitle_text)
    
    # 烧录字幕 - 使用 [subtitles] 滤镜，注意路径转义
    # FFmpeg subtitles 滤镜路径中的冒号需要转义
    abs_subtitle_path = os.path.abspath(subtitle_path).replace("\\", "/").replace(":", "\\:")
    cmd = f'ffmpeg -y -i "{video_path}" -vf "subtitles=\'{abs_subtitle_path}\'" "{output_path}" -loglevel error'
    result = os.system(cmd)
    
    # 清理临时文件
    try:
        os.remove(subtitle_path)
    except:
        pass
    
    return result == 0

def concat_videos(video_paths: List[str], output_path: str) -> bool:
    """拼接多个视频片段"""
    if not video_paths:
        log("❌ 没有视频片段可拼接")
        return False
    
    if len(video_paths) == 1:
        # 只有一个视频，直接复制
        import shutil
        shutil.copy(video_paths[0], output_path)
        return True
    
    # 创建文件列表
    list_path = output_path + ".list.txt"
    with open(list_path, 'w') as f:
        for path in video_paths:
            f.write(f"file '{path}'\n")
    
    # 拼接
    cmd = f'ffmpeg -y -f concat -safe 0 -i "{list_path}" -c copy "{output_path}" -loglevel error'
    result = os.system(cmd)
    
    try:
        os.remove(list_path)
    except:
        pass
    
    return result == 0

def add_audio_to_video(video_path: str, audio_path: str, output_path: str, fade_duration: int = 1) -> bool:
    """给视频添加音频（BGM或配音）"""
    # 提取音频时长
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}" 2>/dev/null'
    audio_duration = float(os.popen(cmd).read().strip() or 0)
    
    # 获取视频时长
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}" 2>/dev/null'
    video_duration = float(os.popen(cmd).read().strip() or 0)
    
    # 如果音频不够长，循环
    if audio_duration < video_duration:
        loops = int(video_duration / audio_duration) + 1
        looped_audio = audio_path + ".looped.mp3"
        cmd = f'ffmpeg -y -streamloop {loops} -i "{audio_path}" -t {video_duration} "{looped_audio}" -loglevel error'
        os.system(cmd)
        audio_path = looped_audio
    
    # 混音
    cmd = f'ffmpeg -y -i "{video_path}" -i "{audio_path}" -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest[a]" -map 0:v -map "[a]" "{output_path}" -loglevel error'
    result = os.system(cmd)
    
    return result == 0

# ============== 主流程 ==============

def process_novel_to_video(
    chapter_text: str,
    chapter_title: str,
    output_dir: str,
    with_images: bool = True,
    parallel_scenes: int = 2
) -> Optional[str]:
    """
    小说章节转视频完整流程
    
    Args:
        chapter_text: 章节文本
        chapter_title: 章节标题
        output_dir: 输出目录
        with_images: 是否生成图片（ False=纯文生视频，True=图生视频）
        parallel_scenes: 并发生成视频的场景数
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    log(f"🚀 开始处理: {chapter_title}")
    
    # Step 1: 生成脚本
    script = generate_script_with_llm(chapter_text, chapter_title)
    
    # 保存脚本
    save_json(
        {
            "chapter_title": script.chapter_title,
            "total_duration": script.total_duration,
            "scenes": [
                {
                    "scene_id": s.scene_id,
                    "description": s.description,
                    "narration": s.narration,
                    "duration": s.duration
                }
                for s in script.scenes
            ]
        },
        output_path / "script.json"
    )
    
    # Step 2: 生成图片 + 视频 + 配音
    scene_data = []  # 存储每个场景的结果
    temp_dir = output_path / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    log(f"📽️ 开始生成 {len(script.scenes)} 个场景...")
    
    for i, scene in enumerate(script.scenes):
        scene_dir = temp_dir / f"scene_{scene.scene_id:02d}"
        scene_dir.mkdir(exist_ok=True)
        
        image_path = scene_dir / "image.jpg"
        video_path = scene_dir / "video.mp4"
        audio_path = scene_dir / "audio.mp3"
        
        scene_data.append({
            "scene_id": scene.scene_id,
            "description": scene.description,
            "narration": scene.narration,
            "duration": scene.duration,
            "image_path": str(image_path),
            "video_path": str(video_path),
            "audio_path": str(audio_path)
        })
        
        # 2a. 生成图片（用于图生视频模式）
        if with_images:
            generate_image_with_vl(scene.description, str(image_path))
            time.sleep(1)  # 避免请求过快
        
        # 2b. 生成配音
        generate_tts(scene.narration, str(audio_path))
        time.sleep(1)
        
        # 2c. 生成视频
        first_frame = str(image_path) if with_images and image_path.exists() else None
        task_id = generate_video_with_hailuo(
            prompt=scene.description,
            first_frame_image=first_frame,
            duration=scene.duration
        )
        
        if task_id:
            file_id = query_video_status(task_id)
            if file_id:
                download_video(file_id, str(video_path))
        
        log(f"✅ 场景 {scene.scene_id}/{len(script.scenes)} 完成")
    
    # Step 3: 收集有效视频
    video_paths = []
    audio_paths = []
    
    for data in scene_data:
        if Path(data["video_path"]).exists():
            video_paths.append(data["video_path"])
        if Path(data["audio_path"]).exists():
            audio_paths.append(data["audio_path"])
    
    if not video_paths:
        log("❌ 没有生成任何视频")
        return None
    
    # Step 4: 拼接视频
    final_video = output_path / "combined.mp4"
    concat_videos(video_paths, str(final_video))
    
    # Step 5: 添加配音（混合所有场景的配音）
    if audio_paths:
        # 先拼接所有配音
        combined_audio = temp_dir / "combined_audio.mp3"
        
        # 创建音频拼接列表
        audio_list = temp_dir / "audio_list.txt"
        with open(audio_list, 'w') as f:
            for ap in audio_paths:
                f.write(f"file '{ap}'\n")
        
        cmd = f'ffmpeg -y -f concat -safe 0 -i "{audio_list}" -c copy "{combined_audio}" -loglevel error'
        os.system(cmd)
        
        # 添加到视频
        output_final = output_path / f"{chapter_title}.mp4"
        add_audio_to_video(str(final_video), str(combined_audio), str(output_final))
        
        log(f"✅ 完成! 输出: {output_final}")
        return str(output_final)
    
    return str(final_video)


# ============== 批量处理 ==============

def batch_process(
    novel_dir: str,
    output_base: str,
    start_chapter: int = 1,
    end_chapter: int = None,
    with_images: bool = True
):
    """
    批量处理多章节
    
    Args:
        novel_dir: 小说文件夹（每行一个 .txt 文件）
        output_base: 输出基础目录
        start_chapter: 起始章节
        end_chapter: 结束章节（None=全部）
        with_images: 是否生成图片
    """
    novel_path = Path(novel_dir)
    txt_files = sorted(novel_path.glob("*.txt"))
    
    if end_chapter:
        txt_files = txt_files[start_chapter-1:end_chapter]
    else:
        txt_files = txt_files[start_chapter-1:]
    
    log(f"📚 发现 {len(txt_files)} 个章节待处理")
    
    results = []
    for i, txt_file in enumerate(txt_files):
        log(f"\n{'='*50}")
        log(f"处理进度: {i+1}/{len(txt_files)}")
        
        try:
            chapter_text = txt_file.read_text(encoding='utf-8')
            chapter_title = txt_file.stem  # 文件名作为标题
            
            output_dir = Path(output_base) / chapter_title
            
            result = process_novel_to_video(
                chapter_text=chapter_text,
                chapter_title=chapter_title,
                output_dir=str(output_dir),
                with_images=with_images
            )
            
            results.append({"chapter": chapter_title, "status": "success", "output": result})
            
        except Exception as e:
            log(f"❌ 处理失败: {e}")
            results.append({"chapter": txt_file.stem, "status": "failed", "error": str(e)})
    
    # 保存汇总
    summary_path = Path(output_base) / "batch_summary.json"
    save_json(results, str(summary_path))
    log(f"\n📊 批量处理完成，汇总: {summary_path}")
    
    return results


# ============== CLI 入口 ==============

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="小说转AI短剧 - MiniMax全链路")
    parser.add_argument("--input", "-i", required=True, help="输入小说文件或文件夹")
    parser.add_argument("--output", "-o", required=True, help="输出目录")
    parser.add_argument("--title", "-t", help="章节标题（单文件模式）")
    parser.add_argument("--no-images", action="store_true", help="跳过图片生成（文生视频模式，更快但质量略低）")
    parser.add_argument("--batch", action="store_true", help="批量处理文件夹模式")
    parser.add_argument("--start", type=int, default=1, help="起始章节（批量模式）")
    parser.add_argument("--end", type=int, help="结束章节（批量模式）")
    
    args = parser.parse_args()
    
    if args.batch:
        # 批量模式
        batch_process(
            novel_dir=args.input,
            output_base=args.output,
            start_chapter=args.start,
            end_chapter=args.end,
            with_images=not args.no_images
        )
    else:
        # 单文件模式
        chapter_text = Path(args.input).read_text(encoding='utf-8')
        chapter_title = args.title or Path(args.input).stem
        
        result = process_novel_to_video(
            chapter_text=chapter_text,
            chapter_title=chapter_title,
            output_dir=args.output,
            with_images=not args.no_images
        )
        
        if result:
            print(f"\n✅ 视频生成完成: {result}")
        else:
            print("\n❌ 生成失败")
            sys.exit(1)
