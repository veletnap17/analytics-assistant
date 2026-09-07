from src.llm import client

def explain_result(question: str, columns: list, rows: list, sql: str) -> str:
    preview = rows[:20]

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data analyst for a carsharing company. "
                    "Answer the user's question directly and briefly. "
                    "Do not mention database columns, preview rows, or technical details unless necessary. "
                    "If the SQL contains LIMIT, do not treat the number of returned rows as the total number of records. "
                    "If the result is limited, say that the table shows up to that limit instead of claiming it is the total. "
                    "Do not invent information. "
                    "Use 1-2 short sentences."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n"
                    f"SQL: {sql}\n"
                    f"Columns: {columns}\n"
                    f"Result preview: {preview}\n"
                    f"Returned rows: {len(rows)}"
                ),
            },
        ],
    )

    return response.choices[0].message.content