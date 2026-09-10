import json
from pathlib import Path
from src.services.embedding_service import embed

BASE_PATH = Path("knowledge")
INDEX_PATH = BASE_PATH / "index.json"

def build_index():
    items = []

    for path in BASE_PATH.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        vector = embed(f"{path.stem}\n{text}")

        items.append({
            "path": str(path),
            "text": text,
            "embedding": vector
        })

    INDEX_PATH.write_text(
        json.dumps(items, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Indexed {len(items)} files.")

if __name__ == "__main__":
    build_index()