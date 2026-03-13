#!/usr/bin/env python3
# ~/.openclaw/workspace/life/projects/pattern-extraction/weekly_pattern_extractor.py
# 每周模式提取器

import os
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

class WeeklyPatternExtractor:
    def __init__(self, workspace=None, days=7):
        self.workspace = workspace or os.path.expanduser("~/.openclaw/workspace")
        self.memory_dir = Path(self.workspace) / "memory"
        self.output_dir = Path(self.workspace) / "life" / "archives" / "weekly"
        self.days = days
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_from_files(self):
        """从日志文件提取模式"""
        patterns = {
            "topics": Counter(),
            "tools": Counter(),
            "errors": Counter(),
            "decisions": [],
            "achievements": [],
            "time_distribution": Counter()
        }
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.days)
        
        # 读取日志文件
        for log_file in sorted(self.memory_dir.glob("????-??-??.md"), reverse=True):
            date_str = log_file.stem
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < start_date:
                    continue
                
                with open(log_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 提取主题标签
                topics = re.findall(r"#(\w+)", content)
                patterns["topics"].update(topics)
                
                # 提取工具使用
                tools = re.findall(r'(?:使用|运行|执行|call|exec|tool).*?([A-Z][a-zA-Z]+)', content)
                patterns["tools"].update([t for t in tools if len(t) > 2])
                
                # 提取错误
                errors = re.findall(r"(?:错误|error|失败|failed|Exception)[^。]*", content)
                patterns["errors"].update([e.strip()[:50] for e in errors[:5]])
                
                # 提取时间分布
                hours = re.findall(r"(\d{2}):\d{2}", content)
                patterns["time_distribution"].update(hours)
                
            except Exception as e:
                continue
        
        return patterns
    
    def generate_report(self, patterns):
        """生成周报"""
        report = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        report.append(f"# 周报 - {today}")
        report.append(f"分析周期: 过去 {self.days} 天")
        report.append("")
        
        # 热门主题
        report.append("## 热门主题 TOP 10")
        report.append("-" * 40)
        for topic, count in patterns["topics"].most_common(10):
            report.append(f"- #{topic}: {count}次")
        if not patterns["topics"]:
            report.append("无数据")
        report.append("")
        
        # 工具使用
        report.append("## 工具使用频率")
        report.append("-" * 40)
        for tool, count in patterns["tools"].most_common(10):
            report.append(f"- {tool}: {count}次")
        if not patterns["tools"]:
            report.append("无数据")
        report.append("")
        
        # 时间分布
        report.append("## 活跃时间段")
        report.append("-" * 40)
        time_dist = sorted(patterns["time_distribution"].items())
        if time_dist:
            hours = [int(h) for h, _ in time_dist]
            if hours:
                peak_hour = max(set(hours), key=hours.count)
                report.append(f"最活跃时段: {peak_hour}:00 - {peak_hour+1}:00")
        else:
            report.append("无数据")
        report.append("")
        
        # 常见错误
        if patterns["errors"]:
            report.append("## 需要关注的错误")
            report.append("-" * 40)
            for error, count in patterns["errors"].most_common(5):
                report.append(f"- {error} ({count}次)")
            report.append("")
        
        # 建议
        report.append("## 改进建议")
        report.append("-" * 40)
        
        if patterns["topics"]:
            top_topic = patterns["topics"].most_common(1)[0][0]
            report.append(f"- 重点关注 #{top_topic}")
        
        if patterns["tools"]:
            top_tool = patterns["tools"].most_common(1)[0][0]
            report.append(f"- 常用工具: {top_tool}")
        
        if patterns["errors"]:
            report.append(f"- 解决 {len(patterns['errors'])} 个错误")
        
        report.append("")
        report.append("---")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report)
    
    def run(self):
        """运行模式提取"""
        print(f"📊 开始周模式分析（过去{self.days}天）...")
        
        patterns = self.extract_from_files()
        report = self.generate_report(patterns)
        
        # 保存报告
        output_file = self.output_dir / f"weekly-report-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ 周报已生成: {output_file}")
        print(f"📊 热门主题: {', '.join([t for t,_ in patterns['topics'].most_common(3)])}")
        print(f"🔧 常用工具: {', '.join([t for t,_ in patterns['tools'].most_common(3)])}")
        
        return output_file


if __name__ == "__main__":
    import sys
    
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    extractor = WeeklyPatternExtractor(days=days)
    extractor.run()
