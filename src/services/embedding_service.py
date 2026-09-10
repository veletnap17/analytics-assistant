import math
from src.llm import client

MODEL = "text-embedding-3-small"

def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=MODEL, input=text)
    return response.data[0].embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)