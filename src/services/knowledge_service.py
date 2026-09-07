from pathlib import Path

class KnowledgeService:
    def __init__(self):
        self.base_path = Path("knowledge")

    def load(self, relative_path: str) -> str:
        return (self.base_path / relative_path).read_text(encoding="utf-8")

    def search(self, query: str) -> list[str]:
        words = query.lower().split()
        matches = []

        for path in self.base_path.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            text_lower = text.lower()

            for word in words:
                word = word.strip(".,?!")
                variants = {word, word[:-1]} if word.endswith("s") and len(word) > 3 else {word}

                if any(v in text_lower for v in variants):
                    matches.append(text)
                    break

        return matches