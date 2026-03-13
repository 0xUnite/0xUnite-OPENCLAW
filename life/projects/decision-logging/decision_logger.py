#!/usr/bin/env python3
# ~/.openclaw/workspace/life/projects/decision-logging/decision_logger.py
# 决策日志记录器

import json
import os
from datetime import datetime
from pathlib import Path

class DecisionLogger:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.path.expanduser("~/.openclaw/workspace")
        self.decisions_dir = Path(self.workspace) / "life" / "decisions"
        self.index_file = self.decisions_dir / "index.json"
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_file.exists():
            self._save_index({"decisions": [], "stats": {}})
    
    def _save_index(self, data):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_index(self):
        with open(self.index_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def create_decision(self, title, description="", decision_type="general",
                        context="", options=None, selected=-1, reason="",
                        expected_outcome="", tags=None):
        """创建决策记录"""
        if options is None:
            options = []
        if tags is None:
            tags = []
        
        decision_id = f"dec-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        decision = {
            "id": decision_id,
            "title": title,
            "description": description,
            "type": decision_type,
            "context": context,
            "options": options,
            "selected": selected,
            "selected_option": options[selected] if selected >= 0 and selected < len(options) else None,
            "reason": reason,
            "expected_outcome": expected_outcome,
            "tags": tags,
            "created_at": datetime.now().isoformat(),
            "outcome": None,
            "reviewed": False
        }
        
        # 保存决策文件
        dec_file = self.decisions_dir / f"{decision_id}.json"
        with open(dec_file, "w", encoding="utf-8") as f:
            json.dump(decision, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        index = self._load_index()
        index["decisions"].append({
            "id": decision_id,
            "title": title,
            "type": decision_type,
            "created_at": decision["created_at"],
            "tags": tags
        })
        
        # 更新统计
        if decision_type not in index["stats"]:
            index["stats"][decision_type] = 0
        index["stats"][decision_type] += 1
        
        self._save_index(index)
        
        print(f"✅ 决策已记录: {decision_id}")
        return decision_id
    
    def get_decision(self, decision_id):
        """获取决策详情"""
        dec_file = self.decisions_dir / f"{decision_id}.json"
        if dec_file.exists():
            with open(dec_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def list_decisions(self, limit=20):
        """列出最近决策"""
        index = self._load_index()
        return index["decisions"][-limit:]
    
    def search_decisions(self, query):
        """搜索决策"""
        results = []
        for dec_file in self.decisions_dir.glob("dec-*.json"):
            with open(dec_file, "r", encoding="utf-8") as f:
                dec = json.load(f)
                if query.lower() in dec["title"].lower() or query.lower() in dec["context"].lower():
                    results.append(dec)
        return results
    
    def update_outcome(self, decision_id, outcome):
        """更新决策结果"""
        dec = self.get_decision(decision_id)
        if dec:
            dec["outcome"] = outcome
            dec["reviewed"] = True
            dec_file = self.decisions_dir / f"{decision_id}.json"
            with open(dec_file, "w", encoding="utf-8") as f:
                json.dump(dec, f, ensure_ascii=False, indent=2)
            print(f"✅ 决策结果已更新: {decision_id}")
    
    def get_stats(self):
        """获取统计信息"""
        return self._load_index()["stats"]


if __name__ == "__main__":
    import sys
    
    logger = DecisionLogger()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            for d in logger.list_decisions(10):
                print(f"[{d['created_at'][:10]}] {d['title']}")
        
        elif cmd == "stats":
            stats = logger.get_stats()
            for k, v in stats.items():
                print(f"{k}: {v}")
        
        elif cmd == "create" and len(sys.argv) > 2:
            title = sys.argv[2]
            logger.create_decision(title, context=" ".join(sys.argv[3:]) if len(sys.argv) > 3 else "")
        
        elif cmd == "get" and len(sys.argv) > 2:
            d = logger.get_decision(sys.argv[2])
            if d:
                print(json.dumps(d, ensure_ascii=False, indent=2))
        
        else:
            print("用法:")
            print("  python3 decision_logger.py list - 列出最近决策")
            print("  python3 decision_logger.py stats - 查看统计")
            print("  python3 decision_logger.py create '标题' '描述' - 创建决策")
            print("  python3 decision_logger.py get <id> - 查看决策详情")
    else:
        print("OpenClaw 决策日志系统")
        print("用法: python3 decision_logger.py <命令>")
