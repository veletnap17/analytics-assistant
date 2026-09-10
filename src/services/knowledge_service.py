import json
from pathlib import Path
from src.services.embedding_service import embed, cosine_similarity

class KnowledgeService:
    def __init__(self):
        self.index_path = Path("knowledge/index.json")

    def search(self, query: str, top_k: int = 3) -> list[str]:
        index = json.loads(self.index_path.read_text(encoding="utf-8"))
        query_embedding = embed(query)

        results = [
            (cosine_similarity(query_embedding, item["embedding"]), item["text"])
            for item in index
        ]

        results.sort(key=lambda x: x[0], reverse=True)
        return [text for _, text in results[:top_k]]