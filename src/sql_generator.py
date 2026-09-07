from src.llm import client
from src.services.knowledge_service import KnowledgeService
from src.services.sql_validator import validate_sql

knowledge = KnowledgeService()

def generate_sql(question: str, history: list[dict] | None = None, previous_sql: str | None = None) -> str:
    context = "\n\n".join(knowledge.search(question))
    history = history or []

    previous_context = ""
    if previous_sql:
        previous_context = (
            "\nPrevious SQL:\n"
            f"{previous_sql}\n"
            "For follow-up questions, preserve relevant filters and conditions from the previous SQL "
            "unless the user explicitly changes or removes them.\n"
        )

    messages = [{
        "role": "system",
        "content": (
            "You are a PostgreSQL expert for a carsharing company. "
            "Generate SQL using only the provided knowledge. "
            "Use conversation history and previous SQL to resolve follow-up questions. "
            "A phrase like 'them', 'those', 'these orders', etc. normally refers to the result of the previous query. "
            "Preserve previous filters when the user adds another condition. "
            "Do not invent tables or columns. "
            "Unless the user explicitly asks for all rows, add LIMIT 1000 to row-level queries. "
            "Do not add LIMIT to aggregate queries. "
            "Return only SQL, without explanation.\n\n"
            f"Knowledge:\n{context}\n"
            f"{previous_context}"
        )
    }]

    messages.extend(history)
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(model="gpt-5-mini", messages=messages)
    sql = response.choices[0].message.content.strip()

    if not validate_sql(sql):
        return "SQL validation failed."

    return sql