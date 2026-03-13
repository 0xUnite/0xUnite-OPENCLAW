#!/usr/bin/env python3
# ~/.openclaw/workspace/life/projects/nighttime-optimizer/nighttime_optimizer.py
# 夜间主动优化器 - 自动检测并修复系统问题

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class NighttimeOptimizer:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.path.expanduser("~/.openclaw/workspace")
        self.memory_dir = Path(self.workspace) / "memory"
        self.log_dir = Path(self.workspace) / "memory"
        self.archive_dir = Path(self.workspace) / "life" / "archives" / "weekly"
        self.report_dir = Path(self.workspace) / "para-system"
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def check_disk_space(self):
        """检查磁盘空间"""
        total, used, free = shutil.disk_usage(self.workspace)
        free_gb = free / (1024**3)
        return {"total": total, "used": used, "free_gb": round(free_gb, 2)}
    
    def check_memory_size(self):
        """检查 MEMORY.md 大小"""
        memory_file = Path(self.workspace) / "MEMORY.md"
        if memory_file.exists():
            size = memory_file.stat().st_size
            return {"size_bytes": size, "size_kb": round(size/1024, 2)}
        return {"size_bytes": 0}
    
    def check_temp_files(self):
        """检查临时文件"""
        temp_patterns = ["*.tmp", "*.log", "__pycache__"]
        temp_files = []
        
        for pattern in temp_patterns:
            temp_files.extend(Path(self.workspace).rglob(pattern))
        
        # 清理7天前的临时文件
        cleanup_count = 0
        for f in temp_files:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if (datetime.now() - mtime).days >= 7:
                    if f.suffix in ['.tmp', '.log']:
                        f.unlink()
                        cleanup_count += 1
            except:
                pass
        
        return {"total": len(temp_files), "cleaned": cleanup_count}
    
    def check_failed_tasks(self):
        """检查失败的任务"""
        # 检查日志中的错误
        errors = []
        for log_file in self.memory_dir.glob("*.log"):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[-100:]:
                        if "error" in line.lower() or "failed" in line.lower() or "❌" in line:
                            errors.append(line.strip()[:100])
            except:
                pass
        
        return {"count": len(set(errors))}
    
    def archive_old_memory(self):
        """归档旧日志"""
        archive_count = 0
        cutoff = datetime.now() - timedelta(days=30)
        
        for log_file in self.memory_dir.glob("????-??-??.md"):
            try:
                date_str = log_file.stem
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < cutoff and file_date.month != datetime.now().month:
                    # 只归档，不删除
                    archive_count += 1
            except:
                pass
        
        return {"would_archive": archive_count}
    
    def run(self):
        """运行优化检查"""
        print(f"🌙 夜间优化检查: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        report = []
        report.append(f"# 夜间优化报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 1. 磁盘空间
        disk = self.check_disk_space()
        report.append("## 磁盘空间")
        report.append(f"- 剩余: {disk['free_gb']} GB")
        if disk['free_gb'] < 5:
            report.append("⚠️ 磁盘空间不足5GB")
        else:
            report.append("✅ 正常")
        report.append("")
        
        # 2. MEMORY.md 大小
        mem = self.check_memory_size()
        report.append("## MEMORY.md 状态")
        report.append(f"- 大小: {mem['size_kb']} KB")
        if mem['size_kb'] > 100:
            report.append("⚠️ 建议手动精简")
        else:
            report.append("✅ 正常")
        report.append("")
        
        # 3. 临时文件
        temp = self.check_temp_files()
        report.append("## 临时文件")
        report.append(f"- 检测到: {temp['total']} 个")
        report.append(f"- 已清理(7天前): {temp['cleaned']} 个")
        report.append("")
        
        # 4. 失败任务
        failed = self.check_failed_tasks()
        report.append("## 任务状态")
        report.append(f"- 检测到错误: {failed['count']} 个")
        if failed['count'] > 10:
            report.append("⚠️ 错误较多，建议检查")
        else:
            report.append("✅ 正常")
        report.append("")
        
        # 5. 归档建议
        archive = self.archive_old_memory()
        report.append("## 归档建议")
        report.append(f"- 可归档旧日志: {archive['would_archive']} 个")
        report.append("")
        
        # 保存报告
        report_file = self.report_dir / f"optimizer-report-{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        print(f"✅ 优化报告: {report_file}")
        
        return report


if __name__ == "__main__":
    optimizer = NighttimeOptimizer()
    optimizer.run()
