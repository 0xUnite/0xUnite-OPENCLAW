#!/usr/bin/env python3
# ~/.openclaw/workspace/life/projects/motivation/motivation_tracker.py
# 动机追踪系统 - 成就、连胜、里程碑

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class MotivationTracker:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.path.expanduser("~/.openclaw/workspace")
        self.base_dir = Path(self.workspace) / "life" / "motivation"
        self.achievements_file = self.base_dir / "achievements.json"
        self.streaks_file = self.base_dir / "streaks.json"
        self.milestones_file = self.base_dir / "milestones.json"
        self._ensure_files()
    
    def _ensure_files(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.achievements_file.exists():
            self._save_achievements({})
        if not self.streaks_file.exists():
            self._save_streaks({})
        if not self.milestones_file.exists():
            self._save_milestones({})
    
    def _load_achievements(self):
        with open(self.achievements_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_achievements(self, data):
        with open(self.achievements_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_streaks(self):
        with open(self.streaks_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_streaks(self, data):
        with open(self.streaks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_milestones(self):
        with open(self.milestones_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_milestones(self, data):
        with open(self.milestones_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record_activity(self, category):
        """记录活动，更新连胜"""
        streaks = self._load_streaks()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if category not in streaks:
            streaks[category] = {
                "current_streak": 0,
                "max_streak": 0,
                "last_activity": None,
                "history": []
            }
        
        last_date = streaks[category]["last_activity"]
        
        if last_date != today:
            if last_date:
                last_dt = datetime.strptime(last_date, "%Y-%m-%d")
                today_dt = datetime.strptime(today, "%Y-%m-%d")
                if (today_dt - last_dt).days == 1:
                    streaks[category]["current_streak"] += 1
                else:
                    streaks[category]["current_streak"] = 1
            else:
                streaks[category]["current_streak"] = 1
            
            streaks[category]["max_streak"] = max(
                streaks[category]["max_streak"],
                streaks[category]["current_streak"]
            )
            
            streaks[category]["last_activity"] = today
            streaks[category]["history"].append(today)
            
            # 检查新成就
            self._check_achievements(category, streaks[category])
        
        self._save_streaks(streaks)
        return streaks[category]
    
    def _check_achievements(self, category, streak_data):
        achievements = self._load_achievements()
        achievement_id = f"streak_{category}"
        
        milestones = {
            3: "🔥 三连冠",
            7: "🔥 一周霸榜",
            14: "🔥 两周王者",
            30: "🔥 月度传奇"
        }
        
        for days, name in milestones.items():
            if streak_data["current_streak"] >= days and achievement_id not in achievements:
                achievements[achievement_id] = {
                    "name": name,
                    "category": category,
                    "days": days,
                    "unlocked_at": datetime.now().isoformat()
                }
                print(f"🏆 成就解锁: {name}")
        
        self._save_achievements(achievements)
    
    def unlock_achievement(self, name, description=""):
        """手动解锁成就"""
        achievements = self._load_achievements()
        key = name.replace(" ", "_").lower()
        
        if key not in achievements:
            achievements[key] = {
                "name": name,
                "description": description,
                "unlocked_at": datetime.now().isoformat()
            }
            self._save_achievements(achievements)
            print(f"🏆 成就解锁: {name}")
            return True
        return False
    
    def record_milestone(self, category, value):
        """记录里程碑"""
        milestones = self._load_milestones()
        
        if category not in milestones:
            milestones[category] = {
                "current": value,
                "history": [],
                "targets": [10, 50, 100, 500, 1000]
            }
        
        milestones[category]["current"] = value
        milestones[category]["history"].append({
            "value": value,
            "at": datetime.now().isoformat()
        })
        
        self._save_milestones(milestones)
        return milestones[category]
    
    def get_report(self):
        """生成动机报告"""
        streaks = self._load_streaks()
        achievements = self._load_achievements()
        milestones = self._load_milestones()
        
        report = []
        report.append("🏆 动机报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        report.append("🔥 连胜记录")
        report.append("-" * 40)
        
        for cat, data in streaks.items():
            current = data["current_streak"]
            max_s = data["max_streak"]
            last = data["last_activity"] or "无"
            report.append(f"  {cat}: {current}天 (最高: {max_s}天, 上次: {last})")
        
        report.append("")
        report.append("🎯 成就解锁")
        report.append("-" * 40)
        
        if achievements:
            for key, ach in achievements.items():
                report.append(f"  🏆 {ach['name']} ({ach.get('days', '')}天)")
        else:
            report.append("  暂无成就，继续努力！")
        
        report.append("")
        report.append("📈 里程碑")
        report.append("-" * 40)
        
        for cat, data in milestones.items():
            current = data["current"]
            report.append(f"  {cat}: {current}")
            targets = data.get("targets", [])
            for target in targets:
                if current >= target:
                    report.append(f"    ✅ {target}")
                else:
                    report.append(f"    ⏳ {target}")
        
        return "\n".join(report)
    
    def run_daily_check(self):
        """每日检查 - 记录今日活动"""
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"📅 每日动机检查: {today}")
        
        # 这里可以添加自动检测逻辑
        # 例如检查今天的 memory 文件是否存在
        
        print(self.get_report())
        return True


if __name__ == "__main__":
    import sys
    
    tracker = MotivationTracker()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "report":
            print(tracker.get_report())
        
        elif cmd == "activity" and len(sys.argv) > 2:
            result = tracker.record_activity(sys.argv[2])
            print(f"✅ {sys.argv[2]}: {result['current_streak']}天连胜")
        
        elif cmd == "achievement" and len(sys.argv) > 2:
            name = sys.argv[2]
            desc = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            tracker.unlock_achievement(name, desc)
        
        elif cmd == "milestone" and len(sys.argv) > 3:
            tracker.record_milestone(sys.argv[2], int(sys.argv[3]))
        
        elif cmd == "daily":
            tracker.run_daily_check()
        
        else:
            print("用法:")
            print("  python3 motivation_tracker.py report - 查看报告")
            print("  python3 motivation_tracker.py activity <类别> - 记录活动")
            print("  python3 motivation_tracker.py achievement <名称> - 解锁成就")
            print("  python3 motivation_tracker.py milestone <类别> <值> - 记录里程碑")
            print("  python3 motivation_tracker.py daily - 每日检查")
    else:
        print(tracker.get_report())
