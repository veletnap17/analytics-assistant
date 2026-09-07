from src.llm import client
from src.services.knowledge_service import KnowledgeService
from src.services.sql_validator import validate_sql

knowledge = KnowledgeService()

def generate_sql(question: str) -> str:
    context = "\n\n".join(knowledge.search(question))

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PostgreSQL expert for a carsharing company. "
                    "Generate SQL using only the provided knowledge. "
                    "Do not invent tables or columns. "
                    "Unless the user explicitly asks for all rows, add LIMIT 1000 to row-level queries. "
                    "Do not add LIMIT to aggregate queries. "
                    "Return only SQL, without explanation.\n\n"
                    f"Knowledge:\n{context}"
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    sql = response.choices[0].message.content.strip()

    if not validate_sql(sql):
        return "SQL validation failed."

    return sql