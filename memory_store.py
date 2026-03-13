#!/usr/bin/env python3
"""
Memory Store with Sentence-Transformers + ChromaDB
使用 paraphrase-multilingual-MiniLM-L12-v2 模型实现记忆存储和搜索
"""

import os
import json
import glob
from datetime import datetime

# 导入向量数据库和模型
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# 配置
CHROMA_DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/chromadb")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "memories"


class MemoryStore:
    """基于向量数据库的记忆存储和搜索"""
    
    def __init__(self, db_path: str = CHROMA_DB_PATH, model_name: str = EMBEDDING_MODEL):
        self.db_path = db_path
        self.model_name = model_name
        self.model = None
        self.client = None
        self.collection = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库和模型"""
        # 确保目录存在
        os.makedirs(self.db_path, exist_ok=True)
        
        # 加载模型
        print(f"📦 加载模型: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        
        # 初始化 ChromaDB
        print(f"📦 初始化 ChromaDB: {self.db_path}")
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"model": self.model_name}
        )
        print(f"✅ MemoryStore 初始化完成")
    
    def add_memory(
        self,
        content: str,
        metadata: dict = None,
        mem_id: str = None,
        mem_type: str = "general"
    ) -> str:
        """
        添加记忆到向量数据库
        
        Args:
            content: 记忆内容（文本）
            metadata: 元数据（可选）
            mem_id: 自定义记忆 ID（可选）
            mem_type: 记忆类型（默认 "general"）
        
        Returns:
            记忆 ID
        """
        # 生成 ID
        if mem_id is None:
            mem_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # 准备元数据
        if metadata is None:
            metadata = {}
        metadata.update({
            "created_at": datetime.now().isoformat(),
            "type": mem_type
        })
        
        # 生成嵌入向量
        embedding = self.model.encode([content]).tolist()[0]
        
        # 添加到集合
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            ids=[mem_id],
            metadatas=[metadata]
        )
        
        print(f"✅ 记忆已添加: {mem_id} ({mem_type})")
        return mem_id
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: dict = None,
        where_document: dict = None
    ) -> dict:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            n_results: 返回结果数量
            where: 元数据过滤条件
            where_document: 文档内容过滤条件
        
        Returns:
            搜索结果字典
        """
        # 生成查询嵌入
        query_embedding = self.model.encode([query]).tolist()[0]
        
        # 执行搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=["documents", "metadatas", "distances"]
        )
        
        # 格式化结果
        formatted = {
            "query": query,
            "results": []
        }
        
        if results["ids"] and results["ids"][0]:
            for i, (doc_id, doc, metadata, distance) in enumerate(zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )):
                formatted["results"].append({
                    "id": doc_id,
                    "content": doc,
                    "metadata": metadata,
                    "score": 1 - distance,  # 转换为相似度
                    "rank": i + 1
                })
        
        return formatted
    
    def delete_memory(self, mem_id: str) -> bool:
        """删除记忆"""
        try:
            self.collection.delete(ids=[mem_id])
            print(f"🗑️ 记忆已删除: {mem_id}")
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def count_memories(self) -> int:
        """统计记忆数量"""
        return self.collection.count()
    
    def list_memories(self, limit: int = 100) -> list:
        """列出所有记忆"""
        results = self.collection.get(limit=limit)
        return results.get("ids", [])
    
    def clear_all(self):
        """清空所有记忆"""
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"model": self.model_name}
        )
        print("🗑️ 所有记忆已清空")


def import_from_memory_files(store: MemoryStore, memory_dir: str = None):
    """从 memory/*.md 文件导入到向量数据库"""
    if memory_dir is None:
        memory_dir = os.path.expanduser("~/.openclaw/workspace/memory")
    
    md_files = glob.glob(f"{memory_dir}/????-??-??.md")
    
    imported = 0
    for filepath in sorted(md_files, reverse=True):
        filename = os.path.basename(filepath)
        date = filename.replace(".md", "")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 按段落分割
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            
            for i, para in enumerate(paragraphs):
                if len(para) > 20:  # 跳过太短的段落
                    mem_id = f"mem_{date}_{i}"
                    store.add_memory(
                        content=para,
                        mem_id=mem_id,
                        mem_type="imported",
                        metadata={"source_file": filename}
                    )
                    imported += 1
        
        except Exception as e:
            print(f"⚠️ 导入失败 {filename}: {e}")
    
    print(f"📥 从 {len(md_files)} 个文件导入了 {imported} 条记忆")
    return imported


# ========== 示例用法 ==========
if __name__ == "__main__":
    # 初始化
    store = MemoryStore()
    
    # 1. 添加记忆
    print("\n📝 添加示例记忆...")
    store.add_memory(
        content="用户是管理学博士生，研究 AI 服务失误对消费者信任的影响",
        mem_type="user_info",
        metadata={"topic": "research"}
    )
    store.add_memory(
        content="2026-02-12: Nexus 节点多次掉线（17:48、19:19、19:32），已设置自动重启脚本",
        mem_type="event",
        metadata={"project": "nexus"}
    )
    store.add_memory(
        content="GPT Minting 今日完成 199 次，平均 3-5 分钟一次",
        mem_type="status",
        metadata={"project": "minting"}
    )
    
    # 2. 搜索记忆
    print("\n🔍 搜索示例...")
    
    results = store.search("Nexus 节点状态", n_results=3)
    print(f"\n搜索「Nexus 节点状态」:")
    for r in results["results"]:
        print(f"  [{r['rank']}] (相似度: {r['score']:.3f}) {r['content'][:50]}...")
    
    results = store.search("用户的研究方向", n_results=3)
    print(f"\n搜索「用户的研究方向」:")
    for r in results["results"]:
        print(f"  [{r['rank']}] (相似度: {r['score']:.3f}) {r['content'][:50]}...")
    
    # 3. 统计
    print(f"\n📊 当前记忆数量: {store.count_memories()}")
    
    # 4. 从文件导入（可选）
    print("\n💡 要从 memory/*.md 导入历史记录，运行:")
    print("   from memory_store import import_from_memory_files")
    print("   import_from_memory_files(store)")
